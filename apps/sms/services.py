"""
Sending SMS through Bonga (the Intelli-Wealth account), the same way
IntelliCash does it.

Bonga takes one recipient per request and answers ``status: 222`` when it has
accepted a message. A broadcast is therefore a loop of single sends, run
outside the web request (a background thread, resumable by the
``send_sms_broadcasts`` management command), so a long list never holds a
gunicorn worker past its timeout.

Safety rules carried over from IntelliCash:

* Tests never reach the provider (SMS_NETWORK_ENABLED is False in test
  settings, whatever .env says).
* A number that cannot be a Kenyan mobile is never sent; it is recorded as
  skipped so staff can see and fix it.
* Each recipient is claimed with a conditional UPDATE before sending, so two
  workers can never text the same person twice.
"""

from __future__ import annotations

import logging
import math
import os
import re
import threading
from dataclasses import dataclass, field

import requests
from django.conf import settings
from django.db import close_old_connections, transaction
from django.db.models import F, Q
from django.utils import timezone

from .models import SmsBroadcast, SmsRecipient, SmsSettings

logger = logging.getLogger(__name__)

BONGA_SUCCESS_STATUS = 222
REQUEST_TIMEOUT_SECONDS = 20
MAX_MESSAGE_LENGTH = 918  # 6 concatenated GSM-7 parts
STALE_SENDING_MINUTES = 15

CREDENTIAL_ENV = {
    "client_id": "BONGA_SMS_CLIENT_ID",
    "api_key": "BONGA_SMS_API_KEY",
    "api_secret": "BONGA_SMS_API_SECRET",
    "service_id": "BONGA_SMS_SERVICE_ID",
    "endpoint": "BONGA_SMS_ENDPOINT",
}
REQUIRED_CREDENTIALS = ("client_id", "api_key", "api_secret", "service_id")


# --------------------------------------------------------------------------
# Phone numbers
# --------------------------------------------------------------------------

def normalize_phone(raw: str) -> str:
    """Return a Kenyan number as 2547XXXXXXXX / 2541XXXXXXXX where possible.

    Anything that does not match a known shape comes back as its digits, and
    ``is_sendable_phone`` then rejects it.
    """
    digits = re.sub(r"\D", "", raw or "")
    if re.fullmatch(r"0[17]\d{8}", digits):
        return "254" + digits[1:]
    if re.fullmatch(r"[17]\d{8}", digits):
        return "254" + digits
    if re.fullmatch(r"2540[17]\d{8}", digits):  # +254 0712... typed with the 0
        return "254" + digits[4:]
    return digits


def is_sendable_phone(raw: str) -> bool:
    return bool(re.fullmatch(r"254[17]\d{8}", normalize_phone(raw)))


def split_phone_values(value: str) -> list[str]:
    """A contact field sometimes holds two numbers: "0712 345678 / 0733 111222"."""
    if not value or "@" in value:
        return []
    return [part.strip() for part in re.split(r"[/,;|\n]+", value) if part.strip()]


# --------------------------------------------------------------------------
# Message helpers
# --------------------------------------------------------------------------

_GSM7 = set(
    "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ ÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
    "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà"
    "^{}\\[~]|€"
)


def sms_parts(message: str) -> int:
    """How many SMS a message costs (GSM-7: 160/153, otherwise UCS-2: 70/67)."""
    if not message:
        return 0
    gsm = all(ch in _GSM7 for ch in message)
    single, multi = (160, 153) if gsm else (70, 67)
    length = len(message)
    return 1 if length <= single else math.ceil(length / multi)


def render_message(template: str, name: str = "") -> str:
    first = (name or "").strip().split(" ")[0] if name else ""
    text = template.replace("{name}", first).replace("{NAME}", first)
    # "Hello {name}, ..." with no name should read "Hello, ..." not "Hello , ...".
    text = re.sub(r"[ \t]+([,.!?])", r"\1", text)
    return re.sub(r"[ \t]{2,}", " ", text).strip()


# --------------------------------------------------------------------------
# Credentials and the Bonga client
# --------------------------------------------------------------------------

def network_enabled() -> bool:
    return bool(getattr(settings, "SMS_NETWORK_ENABLED", True))


def resolve_credentials(sms_settings: SmsSettings | None = None) -> dict:
    """Saved values first, then BONGA_SMS_* environment variables."""
    sms_settings = sms_settings or SmsSettings.get_solo()
    creds = {}
    for attr, env_name in CREDENTIAL_ENV.items():
        value = (getattr(sms_settings, attr, "") or "").strip() or os.getenv(env_name, "").strip()
        creds[attr] = value
    creds["endpoint"] = creds["endpoint"] or SmsSettings.DEFAULT_ENDPOINT
    return creds


def missing_credentials(creds: dict) -> list[str]:
    return [CREDENTIAL_ENV[k] for k in REQUIRED_CREDENTIALS if not creds.get(k)]


def credential_sources(sms_settings: SmsSettings | None = None) -> dict:
    """For the settings page: where each value comes from (never the value)."""
    sms_settings = sms_settings or SmsSettings.get_solo()
    out = {}
    for attr, env_name in CREDENTIAL_ENV.items():
        if (getattr(sms_settings, attr, "") or "").strip():
            out[attr] = "saved"
        elif os.getenv(env_name, "").strip():
            out[attr] = "environment"
        else:
            out[attr] = "default" if attr == "endpoint" else "missing"
    return out


@dataclass
class SendResult:
    ok: bool
    status: str = ""
    message: str = ""
    reference: str = ""
    queued_only: bool = False  # nothing left the server (disabled / not configured)
    raw: dict = field(default_factory=dict)


def send_sms(phone: str, message: str, creds: dict | None = None, sms_settings: SmsSettings | None = None) -> SendResult:
    """Send one SMS. Never raises for provider/network problems."""
    sms_settings = sms_settings or SmsSettings.get_solo()
    creds = creds or resolve_credentials(sms_settings)

    if not sms_settings.enabled:
        return SendResult(ok=False, message="SMS sending is switched off in SMS settings.", queued_only=True)
    missing = missing_credentials(creds)
    if missing:
        return SendResult(ok=False, message="SMS account not configured: " + ", ".join(missing), queued_only=True)
    if not network_enabled():
        return SendResult(ok=False, message="SMS network delivery is disabled on this server.", queued_only=True)
    if not is_sendable_phone(phone):
        return SendResult(ok=False, message="Not a valid Kenyan mobile number.")

    form = {
        "apiClientID": creds["client_id"],
        "key": creds["api_key"],
        "secret": creds["api_secret"],
        "txtMessage": message,
        "MSISDN": normalize_phone(phone),
        "serviceID": creds["service_id"],
    }
    try:
        # multipart/form-data, the shape Bonga documents and IntelliCash sends.
        response = requests.post(
            creds["endpoint"],
            files={k: (None, str(v)) for k, v in form.items()},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        logger.warning("Bonga SMS request failed: %s", exc.__class__.__name__)
        return SendResult(ok=False, message=f"Could not reach the SMS provider ({exc.__class__.__name__}).")

    try:
        body = response.json()
        if not isinstance(body, dict):
            body = {"status_message": str(body)}
    except ValueError:
        body = {"status": response.status_code, "status_message": (response.text or "")[:300]}

    provider_status = body.get("status", response.status_code)
    try:
        accepted = response.ok and int(provider_status) == BONGA_SUCCESS_STATUS
    except (TypeError, ValueError):
        accepted = False

    return SendResult(
        ok=accepted,
        status=str(provider_status)[:50],
        message=str(body.get("status_message") or response.reason or "")[:500],
        reference=str(body.get("unique_id") or "")[:100],
        raw=body,
    )


# --------------------------------------------------------------------------
# Audiences
# --------------------------------------------------------------------------

@dataclass
class Audience:
    recipients: dict = field(default_factory=dict)   # phone -> (name, source)
    invalid: list = field(default_factory=list)      # (raw, name, source)

    def add(self, raw: str, name: str, source: str):
        phone = normalize_phone(raw)
        if not is_sendable_phone(phone):
            self.invalid.append((raw.strip()[:20], name, source))
            return
        self.recipients.setdefault(phone, (name, source))


def facility_contact_queryset(county_id=None, constituency_id=None, ward_id=None,
                              gbv_category_id=None, primary_only=False):
    from apps.facilities.models import FacilityContact

    qs = FacilityContact.objects.select_related("facility", "contact_type").filter(
        is_active=True, facility__is_active=True,
    ).exclude(contact_value__contains="@")
    if ward_id:
        qs = qs.filter(facility__ward_id=ward_id)
    elif constituency_id:
        qs = qs.filter(facility__ward__constituency_id=constituency_id)
    elif county_id:
        qs = qs.filter(facility__ward__constituency__county_id=county_id)
    if gbv_category_id:
        qs = qs.filter(facility__facilitygbvcategory__gbv_category_id=gbv_category_id).distinct()
    if primary_only:
        qs = qs.filter(is_primary=True)
    return qs


def staff_queryset(role_id=None):
    from django.contrib.auth import get_user_model

    qs = get_user_model().objects.filter(is_active=True).exclude(phone_number="")
    if role_id:
        qs = qs.filter(userroleassignment__role_id=role_id).distinct()
    return qs


def parse_custom_numbers(text: str) -> list[tuple[str, str]]:
    """One number per line or comma-separated; "0712345678, Jane Doe" names it."""
    entries = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        # "number, name" on its own line, or a comma-separated list of numbers.
        parts = [p.strip() for p in line.split(",") if p.strip()]
        if len(parts) == 2 and not re.search(r"\d{6,}", parts[1]):
            entries.append((parts[0], parts[1]))
        else:
            entries.extend((p, "") for p in parts)
    return entries


def build_audience(spec: dict) -> Audience:
    """spec is the cleaned compose form (see forms.BroadcastForm.audience_spec)."""
    audience = Audience()
    if spec.get("facilities"):
        qs = facility_contact_queryset(
            county_id=spec.get("county"), constituency_id=spec.get("constituency"),
            ward_id=spec.get("ward"), gbv_category_id=spec.get("gbv_category"),
            primary_only=spec.get("primary_only", False),
        )
        for contact in qs.iterator():
            name = contact.contact_person_name or contact.facility.facility_name
            for value in split_phone_values(contact.contact_value):
                # Free-text facility fields hold landlines and extensions; only
                # mobiles are worth a request, and the rest are not "errors".
                if is_sendable_phone(value):
                    audience.add(value, name, SmsRecipient.SOURCE_FACILITY)
    if spec.get("staff"):
        for user in staff_queryset(spec.get("role")).iterator():
            audience.add(user.phone_number, user.full_name, SmsRecipient.SOURCE_STAFF)
    for raw, name in parse_custom_numbers(spec.get("custom_numbers", "")):
        audience.add(raw, name, SmsRecipient.SOURCE_CUSTOM)
    return audience


# --------------------------------------------------------------------------
# Broadcasts
# --------------------------------------------------------------------------

@transaction.atomic
def create_broadcast(*, title: str, message: str, audience: Audience, spec: dict, user=None) -> SmsBroadcast:
    broadcast = SmsBroadcast.objects.create(
        title=title, message=message, created_by=user,
        audience={k: v for k, v in spec.items() if k != "custom_numbers"} | {
            "custom_count": len(parse_custom_numbers(spec.get("custom_numbers", ""))),
        },
        status=SmsBroadcast.STATUS_QUEUED,
    )
    rows = [
        SmsRecipient(broadcast=broadcast, phone=phone, name=(name or "")[:200], source=source)
        for phone, (name, source) in audience.recipients.items()
    ]
    seen_invalid = set()
    for raw, name, source in audience.invalid:
        key = raw or "(blank)"
        if key in seen_invalid or key in audience.recipients:
            continue
        seen_invalid.add(key)
        rows.append(SmsRecipient(
            broadcast=broadcast, phone=key[:20], name=(name or "")[:200], source=source,
            status=SmsRecipient.STATUS_SKIPPED, provider_message="Not a valid Kenyan mobile number.",
        ))
    SmsRecipient.objects.bulk_create(rows)
    broadcast.refresh_counts()
    return broadcast


def _recover_stale(broadcast: SmsBroadcast):
    """A worker that died mid-send leaves rows in 'sending'. Whether that SMS
    left is unknown, so they are marked failed (staff can retry) rather than
    resent automatically — a duplicate text to a GBV survivor's phone is worse
    than a missing one."""
    cutoff = timezone.now() - timezone.timedelta(minutes=STALE_SENDING_MINUTES)
    broadcast.recipients.filter(status=SmsRecipient.STATUS_SENDING).filter(
        Q(claimed_at__lt=cutoff) | Q(claimed_at__isnull=True)
    ).update(
        status=SmsRecipient.STATUS_FAILED,
        provider_message="Interrupted while sending; delivery unknown. Retry if needed.",
    )


def process_broadcast(broadcast_id: int, limit: int | None = None) -> dict:
    """Send every queued recipient of one broadcast. Safe to run concurrently."""
    try:
        broadcast = SmsBroadcast.objects.get(pk=broadcast_id)
    except SmsBroadcast.DoesNotExist:
        return {"sent": 0, "failed": 0, "waiting": 0}
    if broadcast.status in (SmsBroadcast.STATUS_CANCELLED, SmsBroadcast.STATUS_DRAFT):
        return {"sent": 0, "failed": 0, "waiting": 0}

    sms_settings = SmsSettings.get_solo()
    creds = resolve_credentials(sms_settings)
    _recover_stale(broadcast)

    if broadcast.status == SmsBroadcast.STATUS_QUEUED:
        SmsBroadcast.objects.filter(pk=broadcast.pk).update(
            status=SmsBroadcast.STATUS_SENDING, started_at=broadcast.started_at or timezone.now(),
        )

    sent = failed = waiting = 0
    queued_ids = list(
        broadcast.recipients.filter(status=SmsRecipient.STATUS_QUEUED).values_list("id", flat=True)
    )
    if limit:
        queued_ids = queued_ids[:limit]

    for rid in queued_ids:
        broadcast.refresh_from_db(fields=["status"])
        if broadcast.status == SmsBroadcast.STATUS_CANCELLED:
            break
        claimed = SmsRecipient.objects.filter(pk=rid, status=SmsRecipient.STATUS_QUEUED).update(
            status=SmsRecipient.STATUS_SENDING, attempts=F("attempts") + 1, claimed_at=timezone.now(),
        )
        if not claimed:
            continue
        recipient = SmsRecipient.objects.get(pk=rid)
        result = send_sms(recipient.phone, render_message(broadcast.message, recipient.name),
                          creds=creds, sms_settings=sms_settings)
        if result.queued_only:
            # Switched off or not configured: put it back and stop; nothing was sent.
            SmsRecipient.objects.filter(pk=rid).update(
                status=SmsRecipient.STATUS_QUEUED, attempts=F("attempts") - 1,
                provider_message=result.message[:500],
            )
            waiting += 1
            break
        SmsRecipient.objects.filter(pk=rid).update(
            status=SmsRecipient.STATUS_SENT if result.ok else SmsRecipient.STATUS_FAILED,
            provider_status=result.status, provider_message=result.message,
            provider_reference=result.reference,
            sent_at=timezone.now() if result.ok else None,
        )
        if result.ok:
            sent += 1
        else:
            failed += 1

    broadcast.refresh_from_db()
    broadcast.refresh_counts()
    still_open = broadcast.recipients.filter(
        status__in=[SmsRecipient.STATUS_QUEUED, SmsRecipient.STATUS_SENDING]
    ).exists()
    if not still_open and broadcast.status != SmsBroadcast.STATUS_CANCELLED:
        SmsBroadcast.objects.filter(pk=broadcast.pk).update(
            status=SmsBroadcast.STATUS_COMPLETED, completed_at=timezone.now(),
        )
    elif waiting and broadcast.status == SmsBroadcast.STATUS_SENDING:
        SmsBroadcast.objects.filter(pk=broadcast.pk).update(status=SmsBroadcast.STATUS_QUEUED)
    return {"sent": sent, "failed": failed, "waiting": waiting}


def process_pending_broadcasts() -> dict:
    totals = {"broadcasts": 0, "sent": 0, "failed": 0}
    open_ids = SmsBroadcast.objects.filter(
        status__in=[SmsBroadcast.STATUS_QUEUED, SmsBroadcast.STATUS_SENDING]
    ).order_by("created_at").values_list("id", flat=True)
    for bid in list(open_ids):
        result = process_broadcast(bid)
        totals["broadcasts"] += 1
        totals["sent"] += result["sent"]
        totals["failed"] += result["failed"]
    return totals


def start_sending(broadcast_id: int):
    """Kick off sending after the request commits.

    In production a daemon thread does the work so the page returns at once.
    The ``send_sms_broadcasts`` command (run from cron/systemd timer) picks up
    anything a restarted worker left behind. Tests set
    SMS_SEND_IN_BACKGROUND = False and send inline.
    """
    def run():
        try:
            close_old_connections()
            process_broadcast(broadcast_id)
        except Exception:  # pragma: no cover - logged, never crashes the worker
            logger.exception("SMS broadcast %s failed while sending", broadcast_id)
        finally:
            close_old_connections()

    if not getattr(settings, "SMS_SEND_IN_BACKGROUND", True):
        transaction.on_commit(lambda: process_broadcast(broadcast_id))
        return
    transaction.on_commit(lambda: threading.Thread(target=run, name=f"sms-{broadcast_id}", daemon=True).start())
