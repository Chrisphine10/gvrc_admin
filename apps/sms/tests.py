"""Bulk SMS: phone handling, the Bonga client, audiences, broadcasts, pages."""

from unittest import mock

import pytest
import requests
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from apps.sms import services
from apps.sms.models import SmsBroadcast, SmsRecipient, SmsSettings

CREDS = {"client_id": "cid", "api_key": "key", "api_secret": "secret", "service_id": "sid"}


def _configure(**extra):
    obj = SmsSettings.get_solo()
    for k, v in (CREDS | extra).items():
        setattr(obj, k, v)
    obj.save()
    return obj


def _bonga_response(status=222, http=200, message="Success", unique_id=12345, json_ok=True):
    resp = mock.Mock()
    resp.ok = 200 <= http < 300
    resp.status_code = http
    resp.reason = "OK" if resp.ok else "Error"
    resp.text = "not json"
    if json_ok:
        resp.json.return_value = {"status": status, "status_message": message, "unique_id": unique_id}
    else:
        resp.json.side_effect = ValueError("no json")
    return resp


# --------------------------------------------------------------------- phones

@pytest.mark.parametrize("raw,expected", [
    ("0712345678", "254712345678"),
    ("+254 712 345 678", "254712345678"),
    ("712345678", "254712345678"),
    ("0112345678", "254112345678"),
    ("254712345678", "254712345678"),
    ("+254 0712345678", "254712345678"),
])
def test_normalize_phone(raw, expected):
    assert services.normalize_phone(raw) == expected
    assert services.is_sendable_phone(raw)


@pytest.mark.parametrize("raw", ["", "020 2222222", "12345", "0812345678", "+1 202 555 0101", "abc", "07123456789"])
def test_unsendable_numbers(raw):
    assert not services.is_sendable_phone(raw)


def test_split_phone_values_ignores_email_and_splits_multiples():
    assert services.split_phone_values("info@clinic.org") == []
    assert services.split_phone_values("0712 345678 / 0733 111222") == ["0712 345678", "0733 111222"]


def test_parse_custom_numbers_with_names():
    entries = services.parse_custom_numbers("0712345678, Jane Wanjiku\n0722000111,0733000222\n\n254744000333")
    assert ("0712345678", "Jane Wanjiku") in entries
    assert ("0722000111", "") in entries and ("0733000222", "") in entries
    assert ("254744000333", "") in entries


# ------------------------------------------------------------------- messages

def test_sms_parts_counts_gsm_and_unicode():
    assert services.sms_parts("") == 0
    assert services.sms_parts("a" * 160) == 1
    assert services.sms_parts("a" * 161) == 2
    assert services.sms_parts("a" * 306) == 2
    assert services.sms_parts("a" * 307) == 3
    assert services.sms_parts("Habari 😊") == 1
    assert services.sms_parts("😊" * 71) == 2


def test_render_message_name_and_blank_name():
    assert services.render_message("Hello {name}, meeting at 10.", "Jane Wanjiku") == "Hello Jane, meeting at 10."
    assert services.render_message("Hello {name}, meeting at 10.", "") == "Hello, meeting at 10."


# ---------------------------------------------------------------- credentials

@pytest.mark.django_db
def test_credentials_saved_values_win_over_environment(monkeypatch):
    # The server's own .env may hold real values; this test needs them absent.
    for name in ("BONGA_SMS_API_SECRET", "BONGA_SMS_SERVICE_ID", "BONGA_SMS_ENDPOINT"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("BONGA_SMS_CLIENT_ID", "env-cid")
    monkeypatch.setenv("BONGA_SMS_API_KEY", "env-key")
    obj = SmsSettings.get_solo()
    obj.client_id = "saved-cid"
    obj.save()
    creds = services.resolve_credentials(obj)
    assert creds["client_id"] == "saved-cid"
    assert creds["api_key"] == "env-key"
    assert creds["endpoint"] == SmsSettings.DEFAULT_ENDPOINT
    assert "BONGA_SMS_API_SECRET" in services.missing_credentials(creds)
    sources = services.credential_sources(obj)
    assert sources["client_id"] == "saved" and sources["api_key"] == "environment"
    assert sources["api_secret"] == "missing" and sources["endpoint"] == "default"


# ---------------------------------------------------------------- Bonga client

@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
def test_send_sms_success_posts_bonga_form():
    _configure()
    with mock.patch("apps.sms.services.requests.post", return_value=_bonga_response()) as post:
        result = services.send_sms("0712345678", "Hi")
    assert result.ok and result.status == "222" and result.reference == "12345"
    args, kwargs = post.call_args
    assert args[0] == SmsSettings.DEFAULT_ENDPOINT
    sent = {k: v[1] for k, v in kwargs["files"].items()}
    assert sent == {"apiClientID": "cid", "key": "key", "secret": "secret", "txtMessage": "Hi",
                    "MSISDN": "254712345678", "serviceID": "sid"}
    assert kwargs["timeout"] == services.REQUEST_TIMEOUT_SECONDS


@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
@pytest.mark.parametrize("resp", [
    _bonga_response(status=666, message="Invalid MSISDN"),
    _bonga_response(http=500, status=222),
    _bonga_response(json_ok=False, http=502),
])
def test_send_sms_provider_failures(resp):
    _configure()
    with mock.patch("apps.sms.services.requests.post", return_value=resp):
        result = services.send_sms("0712345678", "Hi")
    assert not result.ok and not result.queued_only


@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
def test_send_sms_network_error_never_raises():
    _configure()
    with mock.patch("apps.sms.services.requests.post", side_effect=requests.ConnectionError("down")):
        result = services.send_sms("0712345678", "Hi")
    assert not result.ok and "ConnectionError" in result.message


@pytest.mark.django_db
def test_send_sms_never_calls_network_in_tests_or_when_unconfigured():
    with mock.patch("apps.sms.services.requests.post") as post:
        assert services.send_sms("0712345678", "Hi").queued_only  # not configured
        _configure()
        assert services.send_sms("0712345678", "Hi").queued_only  # SMS_NETWORK_ENABLED False in tests
        with override_settings(SMS_NETWORK_ENABLED=True):
            obj = SmsSettings.get_solo()
            obj.enabled = False
            obj.save()
            assert services.send_sms("0712345678", "Hi").queued_only  # switched off
    post.assert_not_called()


@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
def test_send_sms_rejects_invalid_number_without_request():
    _configure()
    with mock.patch("apps.sms.services.requests.post") as post:
        result = services.send_sms("020 222 2222", "Hi")
    assert not result.ok and not result.queued_only
    post.assert_not_called()


# ------------------------------------------------------------------ audiences

@pytest.fixture
def contact_type(db):
    from apps.lookups.models import ContactType
    return ContactType.objects.create(type_name="Phone")


@pytest.fixture
def facility_factory(db, ward, operational_status, superuser):
    from apps.facilities.models import Facility

    def make(name, **kw):
        return Facility.objects.create(
            facility_name=name, registration_number=f"REG-{name}", facility_code=f"C-{name}",
            operational_status=operational_status, ward=kw.pop("ward", ward), created_by=superuser, **kw,
        )
    return make


def _contact(facility, ctype, value, user, **kw):
    from apps.facilities.models import FacilityContact
    return FacilityContact.objects.create(facility=facility, contact_type=ctype, contact_value=value,
                                          created_by=user, **kw)


@pytest.mark.django_db
def test_audience_facilities_staff_custom_dedup(facility_factory, contact_type, superuser):
    f1 = facility_factory("Alpha")
    f2 = facility_factory("Beta", is_active=False)
    _contact(f1, contact_type, "0712 000111 / 020 3333333", superuser, contact_person_name="Mary Atieno")
    _contact(f1, contact_type, "alpha@example.org", superuser)
    _contact(f2, contact_type, "0712000222", superuser)  # inactive facility: excluded
    get_user_model().objects.create_user(email="s@x.ke", full_name="Staff One", phone_number="0722000333",
                                         password="x")
    spec = {"facilities": True, "staff": True, "custom_numbers": "0712000111\n0733000444, Ann\nnot-a-number"}
    audience = services.build_audience(spec)
    phones = set(audience.recipients)
    assert "254712000111" in phones            # facility contact, also typed: once
    assert "254722000333" in phones            # staff
    assert "254733000444" in phones            # typed with name
    assert "254712000222" not in phones        # inactive facility
    assert audience.recipients["254712000111"] == ("Mary Atieno", SmsRecipient.SOURCE_FACILITY)
    assert [i[0] for i in audience.invalid] == ["not-a-number"]


@pytest.mark.django_db
def test_audience_filters_by_county(facility_factory, contact_type, superuser, county):
    from apps.geography.models import Constituency, County, Ward
    other_county = County.objects.create(county_name="Other", county_code="OT1")
    other_ward = Ward.objects.create(
        ward_name="W2", ward_code="W2",
        constituency=Constituency.objects.create(constituency_name="C2", constituency_code="C2", county=other_county))
    _contact(facility_factory("Here"), contact_type, "0712000001", superuser)
    _contact(facility_factory("There", ward=other_ward), contact_type, "0712000002", superuser)
    audience = services.build_audience({"facilities": True, "county": county.pk})
    assert set(audience.recipients) == {"254712000001"}


# ----------------------------------------------------------------- broadcasts

def _audience(*phones):
    a = services.Audience()
    for p in phones:
        a.add(p, "Name " + p[-3:], SmsRecipient.SOURCE_CUSTOM)
    return a


@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
def test_broadcast_sends_each_recipient_once(superuser):
    _configure()
    audience = _audience("0712000001", "0712000002", "0712000003")
    audience.add("bad", "", SmsRecipient.SOURCE_CUSTOM)
    b = services.create_broadcast(title="T", message="Hello {name}", audience=audience, spec={}, user=superuser)
    assert b.total_recipients == 4 and b.skipped_count == 1
    responses = [_bonga_response(), _bonga_response(status=666, message="Rejected"), _bonga_response()]
    with mock.patch("apps.sms.services.requests.post", side_effect=responses) as post:
        result = services.process_broadcast(b.pk)
        services.process_broadcast(b.pk)  # second run: nothing left to send
    assert post.call_count == 3
    assert result == {"sent": 2, "failed": 1, "waiting": 0}
    b.refresh_from_db()
    assert b.status == SmsBroadcast.STATUS_COMPLETED and b.completed_at
    assert (b.sent_count, b.failed_count, b.skipped_count) == (2, 1, 1)
    first = post.call_args_list[0].kwargs["files"]["txtMessage"][1]
    assert first == "Hello Name"


@pytest.mark.django_db
def test_broadcast_waits_when_not_configured_then_sends(superuser):
    b = services.create_broadcast(title="T", message="Hi", audience=_audience("0712000001"), spec={}, user=superuser)
    with mock.patch("apps.sms.services.requests.post") as post:
        result = services.process_broadcast(b.pk)
    post.assert_not_called()
    assert result["waiting"] == 1
    b.refresh_from_db()
    assert b.status == SmsBroadcast.STATUS_QUEUED
    r = b.recipients.get()
    assert r.status == SmsRecipient.STATUS_QUEUED and r.attempts == 0

    _configure()
    with override_settings(SMS_NETWORK_ENABLED=True), \
            mock.patch("apps.sms.services.requests.post", return_value=_bonga_response()):
        totals = services.process_pending_broadcasts()
    assert totals["sent"] == 1
    b.refresh_from_db()
    assert b.status == SmsBroadcast.STATUS_COMPLETED


@pytest.mark.django_db
def test_stale_sending_rows_become_failed_not_resent(superuser):
    b = services.create_broadcast(title="T", message="Hi", audience=_audience("0712000001"), spec={}, user=superuser)
    SmsRecipient.objects.filter(broadcast=b).update(
        status=SmsRecipient.STATUS_SENDING, claimed_at=timezone.now() - timezone.timedelta(hours=1))
    _configure()
    with override_settings(SMS_NETWORK_ENABLED=True), mock.patch("apps.sms.services.requests.post") as post:
        services.process_broadcast(b.pk)
    post.assert_not_called()
    assert b.recipients.get().status == SmsRecipient.STATUS_FAILED


@pytest.mark.django_db
def test_cancelled_broadcast_is_not_processed(superuser):
    b = services.create_broadcast(title="T", message="Hi", audience=_audience("0712000001"), spec={}, user=superuser)
    SmsBroadcast.objects.filter(pk=b.pk).update(status=SmsBroadcast.STATUS_CANCELLED)
    _configure()
    with override_settings(SMS_NETWORK_ENABLED=True), mock.patch("apps.sms.services.requests.post") as post:
        services.process_broadcast(b.pk)
    post.assert_not_called()


def test_management_command_runs(db, capsys):
    from django.core.management import call_command
    call_command("send_sms_broadcasts")
    assert "broadcasts=0" in capsys.readouterr().out


# ---------------------------------------------------------------------- pages

@pytest.fixture
def plain_user(db):
    return get_user_model().objects.create_user(email="plain@x.ke", full_name="Plain", phone_number="0700000099",
                                                password="pass12345")


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["sms:broadcast_list", "sms:broadcast_compose", "sms:settings"])
def test_pages_require_login_and_permission(client, plain_user, name):
    url = reverse(name)
    resp = client.get(url)
    assert resp.status_code == 302 and ("/login/" in resp.url or "/dashboard/" in resp.url)
    client.force_login(plain_user)
    resp = client.get(url)
    assert resp.status_code == 302 and resp.url == "/dashboard/"


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["sms:broadcast_list", "sms:broadcast_compose", "sms:settings"])
def test_pages_render_for_superuser(client, superuser, name):
    client.force_login(superuser)
    resp = client.get(reverse(name))
    assert resp.status_code == 200
    assert b"SMS" in resp.content


@pytest.mark.django_db
def test_permission_seed_grants_system_administrator(db):
    from apps.authentication.models import Permission
    names = set(Permission.objects.filter(resource_name="sms").values_list("permission_name", flat=True))
    assert names == {"view_sms", "send_sms", "change_sms"}


@pytest.mark.django_db
def test_role_with_send_permission_can_compose(client, plain_user, superuser):
    from apps.authentication.models import Permission, RolePermission, UserRole, UserRoleAssignment
    role = UserRole.objects.create(role_name="SMS Officer", description="x")
    for name in ("view_sms", "send_sms"):
        RolePermission.objects.create(role=role, permission=Permission.objects.get(permission_name=name),
                                      granted_by=superuser)
    UserRoleAssignment.objects.create(user=plain_user, role=role, assigned_by=superuser)
    client.force_login(plain_user)
    assert client.get(reverse("sms:broadcast_compose")).status_code == 200
    assert client.get(reverse("sms:settings")).status_code == 302  # no change_sms


@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
def test_compose_creates_and_sends_broadcast(client, superuser, django_capture_on_commit_callbacks):
    _configure()
    client.force_login(superuser)
    with mock.patch("apps.sms.services.requests.post", return_value=_bonga_response()) as post, \
            django_capture_on_commit_callbacks(execute=True):
        resp = client.post(reverse("sms:broadcast_compose"), {
            "title": "Test run", "message": "Hello {name}",
            "custom_numbers": "0712000001, Jane\n0712000002\n12",
        })
    b = SmsBroadcast.objects.get(title="Test run")
    assert resp.status_code == 302 and resp.url == reverse("sms:broadcast_detail", args=[b.pk])
    assert post.call_count == 2
    b.refresh_from_db()
    assert (b.sent_count, b.skipped_count, b.status) == (2, 1, SmsBroadcast.STATUS_COMPLETED)
    detail = client.get(resp.url)
    assert detail.status_code == 200 and b"254712000001" in detail.content


@pytest.mark.django_db
def test_compose_requires_some_recipients(client, superuser):
    client.force_login(superuser)
    resp = client.post(reverse("sms:broadcast_compose"), {"title": "x", "message": "y"})
    assert resp.status_code == 200
    assert SmsBroadcast.objects.count() == 0
    assert b"Choose at least one group" in resp.content


@pytest.mark.django_db
def test_audience_preview_json(client, superuser):
    client.force_login(superuser)
    resp = client.post(reverse("sms:audience_preview"), {"custom_numbers": "0712000001\nbad", "message": "a" * 161})
    data = resp.json()
    assert data["recipients"] == 1 and data["invalid"] == 1
    assert data["parts_per_message"] == 2 and data["estimated_sms"] == 2
    assert "***" in data["sample"][0]["phone"]  # numbers are masked in the preview


@pytest.mark.django_db
def test_retry_and_cancel(client, superuser, django_capture_on_commit_callbacks):
    b = services.create_broadcast(title="T", message="Hi", audience=_audience("0712000001", "0712000002"),
                                  spec={}, user=superuser)
    SmsRecipient.objects.filter(broadcast=b, phone="254712000001").update(status=SmsRecipient.STATUS_FAILED)
    client.force_login(superuser)
    with django_capture_on_commit_callbacks(execute=True):
        resp = client.post(reverse("sms:broadcast_retry", args=[b.pk]))
    assert resp.status_code == 302
    assert b.recipients.filter(status=SmsRecipient.STATUS_QUEUED).count() == 2  # unconfigured: back in the queue
    resp = client.post(reverse("sms:broadcast_cancel", args=[b.pk]))
    b.refresh_from_db()
    assert b.status == SmsBroadcast.STATUS_CANCELLED
    assert b.recipients.filter(status=SmsRecipient.STATUS_SKIPPED).count() == 2
    assert client.get(reverse("sms:broadcast_retry", args=[b.pk])).status_code == 405


@pytest.mark.django_db
def test_progress_endpoint(client, superuser):
    b = services.create_broadcast(title="T", message="Hi", audience=_audience("0712000001"), spec={}, user=superuser)
    client.force_login(superuser)
    data = client.get(reverse("sms:broadcast_progress", args=[b.pk])).json()
    assert data["total"] == 1 and data["pending"] == 1 and data["progress"] == 0


@pytest.mark.django_db
def test_settings_secrets_are_write_only(client, superuser):
    _configure(api_secret="super-secret-value")
    client.force_login(superuser)
    page = client.get(reverse("sms:settings"))
    assert b"super-secret-value" not in page.content
    # Saving with empty secret boxes keeps the saved secrets.
    resp = client.post(reverse("sms:settings"), {
        "cfg-enabled": "on", "cfg-provider_name": "Intelli-Wealth", "cfg-sender_id": "INTELLIWLTH",
        "cfg-client_id": "", "cfg-api_key": "", "cfg-api_secret": "", "cfg-service_id": "new-sid", "cfg-endpoint": "",
    })
    assert resp.status_code == 302
    obj = SmsSettings.get_solo()
    assert obj.api_secret == "super-secret-value" and obj.service_id == "new-sid"
    client.post(reverse("sms:settings"), {"cfg-provider_name": "x", "cfg-clear_saved_credentials": "on"})
    obj.refresh_from_db()
    assert obj.api_secret == "" and obj.client_id == "" and obj.enabled is False


@pytest.mark.django_db
@override_settings(SMS_NETWORK_ENABLED=True)
def test_test_sms_records_result(client, superuser):
    _configure()
    client.force_login(superuser)
    with mock.patch("apps.sms.services.requests.post", return_value=_bonga_response()):
        resp = client.post(reverse("sms:test"), {"test-phone": "0712000001", "test-message": "ping"})
    assert resp.status_code == 302
    r = SmsRecipient.objects.get(source=SmsRecipient.SOURCE_TEST)
    assert r.status == SmsRecipient.STATUS_SENT and r.phone == "254712000001"
    resp = client.post(reverse("sms:test"), {"test-phone": "123", "test-message": "ping"})
    assert SmsRecipient.objects.filter(source=SmsRecipient.SOURCE_TEST).count() == 1


@pytest.mark.django_db
def test_django_admin_hides_credentials(client, superuser):
    _configure(api_key="hidden-key")
    client.force_login(superuser)
    obj = SmsSettings.get_solo()
    resp = client.get(reverse("admin:sms_smssettings_change", args=[obj.pk]))
    assert resp.status_code == 200 and b"hidden-key" not in resp.content
