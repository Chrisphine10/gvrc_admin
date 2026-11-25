from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from apps.authentication.permissions import has_permission, permission_required

from . import services
from .forms import BroadcastForm, SmsSettingsForm, TestSmsForm
from .models import SmsBroadcast, SmsRecipient, SmsSettings


def _account_status():
    sms_settings = SmsSettings.get_solo()
    creds = services.resolve_credentials(sms_settings)
    missing = services.missing_credentials(creds)
    return {
        "sms_settings": sms_settings,
        "sms_ready": sms_settings.enabled and not missing and services.network_enabled(),
        "sms_missing": missing,
        "sms_network": services.network_enabled(),
    }


@login_required
@permission_required("view_sms")
def broadcast_list(request):
    qs = SmsBroadcast.objects.select_related("created_by")
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    totals = SmsBroadcast.objects.aggregate(
        sent=Sum("sent_count"), failed=Sum("failed_count"), recipients=Sum("total_recipients"),
    )
    context = {
        "segment": "sms",
        "page_obj": page,
        "broadcasts": page.object_list,
        "status_filter": status or "",
        "status_choices": SmsBroadcast.STATUS_CHOICES,
        "totals": {k: v or 0 for k, v in totals.items()},
        "can_send": has_permission(request.user, "send_sms"),
        "can_configure": has_permission(request.user, "change_sms"),
        **_account_status(),
    }
    return render(request, "sms/broadcast_list.html", context)


@login_required
@permission_required("send_sms")
def broadcast_compose(request):
    form = BroadcastForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        spec = form.audience_spec()
        audience = services.build_audience(spec)
        if not audience.recipients:
            messages.error(request, "None of the chosen recipients has a valid Kenyan mobile number. Nothing was sent.")
        else:
            broadcast = services.create_broadcast(
                title=form.cleaned_data["title"], message=form.cleaned_data["message"],
                audience=audience, spec=spec, user=request.user,
            )
            services.start_sending(broadcast.pk)
            note = f"Sending to {len(audience.recipients)} number(s)."
            if audience.invalid:
                note += f" {len(audience.invalid)} invalid number(s) skipped."
            messages.success(request, note)
            return redirect("sms:broadcast_detail", broadcast_id=broadcast.pk)
    context = {"segment": "sms", "form": form, **_account_status()}
    return render(request, "sms/broadcast_compose.html", context)


@login_required
@permission_required("send_sms")
@require_POST
def audience_preview(request):
    """Live recipient count for the compose page (no message is sent)."""
    form = BroadcastForm(request.POST)
    form.is_valid()  # partial data is fine for a preview
    data = getattr(form, "cleaned_data", {})
    spec = {
        "facilities": bool(data.get("facilities")),
        "county": data["county"].pk if data.get("county") else None,
        "constituency": data["constituency"].pk if data.get("constituency") else None,
        "ward": data["ward"].pk if data.get("ward") else None,
        "gbv_category": data["gbv_category"].pk if data.get("gbv_category") else None,
        "primary_only": bool(data.get("primary_only")),
        "staff": bool(data.get("staff")),
        "role": data["role"].pk if data.get("role") else None,
        "custom_numbers": request.POST.get("custom_numbers", ""),
    }
    audience = services.build_audience(spec)
    by_source = {}
    for _name, source in audience.recipients.values():
        by_source[source] = by_source.get(source, 0) + 1
    message = request.POST.get("message", "")
    parts = services.sms_parts(services.render_message(message, "Wanjiku")) if message else 0
    return JsonResponse({
        "recipients": len(audience.recipients),
        "invalid": len(audience.invalid),
        "by_source": by_source,
        "parts_per_message": parts,
        "estimated_sms": parts * len(audience.recipients),
        "sample": [
            {"phone": phone[:6] + "***" + phone[-2:], "name": name}
            for phone, (name, _s) in list(audience.recipients.items())[:5]
        ],
    })


@login_required
@permission_required("view_sms")
def broadcast_detail(request, broadcast_id):
    broadcast = get_object_or_404(SmsBroadcast.objects.select_related("created_by"), pk=broadcast_id)
    recipients = broadcast.recipients.all()
    status = request.GET.get("status")
    if status:
        recipients = recipients.filter(status=status)
    page = Paginator(recipients, 50).get_page(request.GET.get("page"))
    context = {
        "segment": "sms",
        "broadcast": broadcast,
        "page_obj": page,
        "recipients": page.object_list,
        "status_filter": status or "",
        "recipient_status_choices": SmsRecipient.STATUS_CHOICES,
        "parts": services.sms_parts(broadcast.message),
        "can_send": has_permission(request.user, "send_sms"),
        **_account_status(),
    }
    return render(request, "sms/broadcast_detail.html", context)


@login_required
@permission_required("view_sms")
@require_GET
def broadcast_progress(request, broadcast_id):
    broadcast = get_object_or_404(SmsBroadcast, pk=broadcast_id)
    broadcast.refresh_counts()
    return JsonResponse({
        "status": broadcast.status,
        "status_display": broadcast.get_status_display(),
        "total": broadcast.total_recipients,
        "sent": broadcast.sent_count,
        "failed": broadcast.failed_count,
        "skipped": broadcast.skipped_count,
        "pending": broadcast.pending_count,
        "progress": broadcast.progress_percent,
    })


@login_required
@permission_required("send_sms")
@require_POST
def broadcast_retry(request, broadcast_id):
    broadcast = get_object_or_404(SmsBroadcast, pk=broadcast_id)
    if broadcast.status == SmsBroadcast.STATUS_CANCELLED:
        messages.error(request, "This broadcast was cancelled.")
        return redirect("sms:broadcast_detail", broadcast_id=broadcast.pk)
    n = broadcast.recipients.filter(status=SmsRecipient.STATUS_FAILED).update(
        status=SmsRecipient.STATUS_QUEUED, provider_message="", claimed_at=None,
    )
    if n or broadcast.recipients.filter(status=SmsRecipient.STATUS_QUEUED).exists():
        SmsBroadcast.objects.filter(pk=broadcast.pk).update(status=SmsBroadcast.STATUS_QUEUED, completed_at=None)
        services.start_sending(broadcast.pk)
        messages.success(request, f"Retrying {n} failed and any waiting message(s).")
    else:
        messages.info(request, "Nothing to retry.")
    return redirect("sms:broadcast_detail", broadcast_id=broadcast.pk)


@login_required
@permission_required("send_sms")
@require_POST
def broadcast_cancel(request, broadcast_id):
    broadcast = get_object_or_404(SmsBroadcast, pk=broadcast_id)
    if broadcast.status in (SmsBroadcast.STATUS_COMPLETED, SmsBroadcast.STATUS_CANCELLED):
        messages.info(request, "This broadcast has already finished.")
    else:
        SmsBroadcast.objects.filter(pk=broadcast.pk).update(
            status=SmsBroadcast.STATUS_CANCELLED, completed_at=timezone.now(),
        )
        skipped = broadcast.recipients.filter(status=SmsRecipient.STATUS_QUEUED).update(
            status=SmsRecipient.STATUS_SKIPPED, provider_message="Cancelled before sending.",
        )
        broadcast.refresh_counts()
        messages.success(request, f"Cancelled. {skipped} message(s) will not be sent.")
    return redirect("sms:broadcast_detail", broadcast_id=broadcast.pk)


@login_required
@permission_required("change_sms")
def sms_settings(request):
    obj = SmsSettings.get_solo()
    form = SmsSettingsForm(request.POST or None, instance=obj, prefix="cfg")
    test_form = TestSmsForm(prefix="test")
    if request.method == "POST" and form.is_valid():
        saved = form.save(commit=False)
        saved.updated_by = request.user
        saved.save()
        messages.success(request, "SMS settings saved.")
        return redirect("sms:settings")
    context = {
        "segment": "sms_settings",
        "form": form,
        "test_form": test_form,
        "credential_rows": [
            (form[name], src) for name, src in services.credential_sources(obj).items()
        ],
        **_account_status(),
    }
    return render(request, "sms/settings.html", context)


@login_required
@permission_required("change_sms")
@require_POST
def sms_test(request):
    form = TestSmsForm(request.POST, prefix="test")
    if not form.is_valid():
        for errors in form.errors.values():
            for e in errors:
                messages.error(request, e)
        return redirect("sms:settings")
    result = services.send_sms(form.cleaned_data["phone"], form.cleaned_data["message"])
    # Keep a record, like any other send.
    broadcast = SmsBroadcast.objects.create(
        title="Test message", message=form.cleaned_data["message"], created_by=request.user,
        audience={"test": True}, status=SmsBroadcast.STATUS_COMPLETED,
        started_at=timezone.now(), completed_at=timezone.now(),
    )
    SmsRecipient.objects.create(
        broadcast=broadcast, phone=services.normalize_phone(form.cleaned_data["phone"]),
        source=SmsRecipient.SOURCE_TEST, attempts=1,
        status=SmsRecipient.STATUS_SENT if result.ok else SmsRecipient.STATUS_FAILED,
        provider_status=result.status, provider_message=result.message, provider_reference=result.reference,
        sent_at=timezone.now() if result.ok else None,
    )
    broadcast.refresh_counts()
    if result.ok:
        messages.success(request, f"Test SMS accepted by the provider (status {result.status}).")
    else:
        messages.error(request, f"Test SMS not sent: {result.message or result.status}")
    return redirect("sms:settings")
