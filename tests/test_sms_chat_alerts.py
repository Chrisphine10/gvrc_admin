"""Chat alerts by SMS (Bonga) and the check_data report."""

import json
from io import StringIO
from unittest import mock

import pytest
import requests
from django.core.management import call_command
from django.test import Client, override_settings
from django.utils import timezone

from apps.chat.models import Conversation
from apps.chat.services import ConversationService, MessageService
from apps.sms.forms import SmsSettingsForm
from apps.sms.models import SmsNotification, SmsSettings
from tests.conftest import make_user

pytestmark = pytest.mark.django_db

CREDS = {"client_id": "cid", "api_key": "key", "api_secret": "secret", "service_id": "sid"}
ON_CALL = "0711000001, 0722000002"


def configure(**extra):
    obj = SmsSettings.get_solo()
    for k, v in (CREDS | {"alert_numbers": ON_CALL} | extra).items():
        setattr(obj, k, v)
    obj.save()
    return obj


def bonga(status=222):
    resp = mock.Mock(ok=True, status_code=200, reason="OK", text="")
    resp.json.return_value = {"status": status, "status_message": "Success", "unique_id": 1}
    return resp


@pytest.fixture
def post():
    with override_settings(SMS_NETWORK_ENABLED=True), \
            mock.patch("apps.sms.services.requests.post", return_value=bonga()) as p:
        yield p


def sent_to(post_mock):
    return [c.kwargs["files"]["MSISDN"][1] for c in post_mock.call_args_list]


def texts(post_mock):
    return [c.kwargs["files"]["txtMessage"][1] for c in post_mock.call_args_list]


def start_chat(mobile_session, django_capture_on_commit_callbacks, subject="Help me please"):
    with django_capture_on_commit_callbacks(execute=True):
        conv = ConversationService.get_or_create_conversation(mobile_session, subject)
        ConversationService.auto_assign_conversation(conv)
    return conv


def test_new_chat_texts_on_call_and_assigned_staff(mobile_session, post, django_capture_on_commit_callbacks):
    configure()
    staff = make_user(is_staff=True, phone_number="0733000003")
    conv = start_chat(mobile_session, django_capture_on_commit_callbacks)

    assert sorted(sent_to(post)) == ["254711000001", "254722000002", "254733000003"]
    kinds = dict(SmsNotification.objects.values_list("phone", "kind"))
    assert kinds["254733000003"] == SmsNotification.KIND_ASSIGNED
    assert kinds["254711000001"] == SmsNotification.KIND_NEW_CHAT
    assert all(n.status == SmsNotification.STATUS_SENT for n in SmsNotification.objects.all())
    for body in texts(post):
        assert f"/chat/conversation/{conv.pk}/" in body
        assert "Help me please" not in body  # never what the person wrote
    assert conv.assigned_admin == staff


def test_assigned_staff_on_call_list_gets_one_text(mobile_session, post, django_capture_on_commit_callbacks):
    configure(alert_numbers="0733000003, 0711000001")
    make_user(is_staff=True, phone_number="+254733000003")
    start_chat(mobile_session, django_capture_on_commit_callbacks)
    assert sorted(sent_to(post)) == ["254711000001", "254733000003"]


def test_reassigning_same_person_does_not_text_twice(mobile_session, post, django_capture_on_commit_callbacks):
    configure(alert_numbers="")
    staff = make_user(is_staff=True, phone_number="0733000003")
    conv = start_chat(mobile_session, django_capture_on_commit_callbacks)
    with django_capture_on_commit_callbacks(execute=True):
        ConversationService.assign_admin_to_conversation(conv, staff)
    assert sent_to(post) == ["254733000003"]


def test_urgent_mobile_message_alerts_once_per_chat(mobile_session, post, django_capture_on_commit_callbacks):
    configure(notify_new_chats=False, notify_assigned_staff=False)
    conv = start_chat(mobile_session, django_capture_on_commit_callbacks)
    assert post.call_count == 0
    for _ in range(2):
        with django_capture_on_commit_callbacks(execute=True):
            MessageService.create_mobile_message(conv, "they are here", is_urgent=True)
    assert sorted(sent_to(post)) == ["254711000001", "254722000002"]
    assert all("URGENT" in t and "they are here" not in t for t in texts(post))


def test_normal_mobile_message_sends_nothing(mobile_session, post, django_capture_on_commit_callbacks):
    configure(notify_new_chats=False, notify_assigned_staff=False)
    conv = start_chat(mobile_session, django_capture_on_commit_callbacks)
    with django_capture_on_commit_callbacks(execute=True):
        MessageService.create_mobile_message(conv, "hello")
    assert post.call_count == 0


def test_switches_off_send_nothing(mobile_session, post, django_capture_on_commit_callbacks):
    configure(notify_new_chats=False, notify_assigned_staff=False, notify_urgent_messages=False)
    make_user(is_staff=True, phone_number="0733000003")
    start_chat(mobile_session, django_capture_on_commit_callbacks)
    assert post.call_count == 0 and not SmsNotification.objects.exists()


def test_sending_switched_off_sends_nothing(mobile_session, post, django_capture_on_commit_callbacks):
    configure(enabled=False)
    make_user(is_staff=True, phone_number="0733000003")
    start_chat(mobile_session, django_capture_on_commit_callbacks)
    assert post.call_count == 0


def test_unconfigured_account_records_not_sent(mobile_session, post, django_capture_on_commit_callbacks, monkeypatch):
    for env in ("BONGA_SMS_CLIENT_ID", "BONGA_SMS_API_KEY", "BONGA_SMS_API_SECRET", "BONGA_SMS_SERVICE_ID"):
        monkeypatch.delenv(env, raising=False)
    SmsSettings.objects.update_or_create(pk=SmsSettings.get_solo().pk, defaults={"alert_numbers": ON_CALL})
    start_chat(mobile_session, django_capture_on_commit_callbacks)
    assert post.call_count == 0
    assert set(SmsNotification.objects.values_list("status", flat=True)) == {SmsNotification.STATUS_NOT_SENT}


def test_provider_down_never_breaks_the_chat(mobile_session, django_capture_on_commit_callbacks):
    configure()
    make_user(is_staff=True, phone_number="0733000003")
    with override_settings(SMS_NETWORK_ENABLED=True), \
            mock.patch("apps.sms.services.requests.post", side_effect=requests.ConnectionError):
        conv = start_chat(mobile_session, django_capture_on_commit_callbacks)
    assert Conversation.objects.filter(pk=conv.pk).exists()
    assert set(SmsNotification.objects.values_list("status", flat=True)) == {SmsNotification.STATUS_FAILED}


def test_mobile_api_start_sends_alert(post, django_capture_on_commit_callbacks):
    configure(alert_numbers="0711000001")
    api = Client()
    r = api.post("/mobile/sessions/create/", {"device_id": "alert-device"}, content_type="application/json")
    assert r.status_code == 201
    with django_capture_on_commit_callbacks(execute=True):
        r = api.post("/mobile/chat/start/", json.dumps({"subject": "x", "device_id": "alert-device"}),
                     content_type="application/json")
    assert r.status_code == 201, r.content
    assert sent_to(post) == ["254711000001"]


# --------------------------------------------------------------- settings page

def test_alert_numbers_validated_and_normalised():
    obj = SmsSettings.get_solo()
    base = {"cfg-enabled": "on", "cfg-provider_name": "x", "cfg-sender_id": "INTELLIWLTH"}
    bad = SmsSettingsForm({**base, "cfg-alert_numbers": "0711000001, 020123456"}, instance=obj, prefix="cfg")
    assert not bad.is_valid() and "020123456" in str(bad.errors["alert_numbers"])
    good = SmsSettingsForm({**base, "cfg-alert_numbers": "0711000001\n+254 711 000 001\r\n0722000002"},
                           instance=obj, prefix="cfg")
    assert good.is_valid(), good.errors
    assert good.cleaned_data["alert_numbers"] == "254711000001, 254722000002"


def test_settings_page_saves_switches_and_lists_alerts(admin_client_):
    SmsNotification.objects.create(kind="new_chat", conversation_id=7, phone="254711000001",
                                   message="m", status="sent")
    r = admin_client_.get("/sms/settings/")
    assert r.status_code == 200
    body = r.content.decode()
    assert "Chat alerts" in body and "New chat #7" in body and "254711000001" not in body  # masked
    r = admin_client_.post("/sms/settings/", {
        "cfg-enabled": "on", "cfg-provider_name": "Intelli-Wealth (Bonga SMS)", "cfg-sender_id": "INTELLIWLTH",
        "cfg-notify_urgent_messages": "on", "cfg-alert_numbers": "0711000001",
    })
    assert r.status_code == 302
    s = SmsSettings.get_solo()
    assert s.notify_urgent_messages and not s.notify_new_chats and not s.notify_assigned_staff
    assert s.alert_numbers == "254711000001"


# ------------------------------------------------------------------ check_data

def test_check_data_reports(world):
    from apps.facilities.models import Facility, FacilityCoordinate

    fac = Facility.objects.first()
    FacilityCoordinate.objects.filter(facility=fac).delete()
    FacilityCoordinate.objects.create(facility=fac, latitude=0, longitude=0, collection_date=timezone.now().date())
    out = StringIO()
    call_command("check_data", stdout=out)
    text = out.getvalue()
    assert "locations are 0,0" in text
    assert "Summary:" in text
    with pytest.raises(SystemExit):
        call_command("check_data", "--strict", stdout=StringIO())


def test_check_data_clean_database_has_no_errors(db):
    out = StringIO()
    call_command("check_data", "--strict", stdout=out)
    assert "0 error(s)" in out.getvalue()


# ------------------------------------------------------- password reset by SMS

@pytest.fixture
def no_cache():
    from django.core.cache import cache
    cache.clear()
    yield
    cache.clear()


def test_password_reset_link_also_goes_by_sms(client, post, mailoutbox, no_cache):
    configure()
    user = make_user(phone_number="0733000009")
    r = client.post("/password-reset/", {"email": user.email})
    assert r.status_code == 302
    assert sent_to(post) == ["254733000009"]
    body = texts(post)[0]
    assert "/password-reset/confirm/" in body and body.split("/password-reset/confirm/")[1].split("/")[0] in mailoutbox[0].body
    # The link in the SMS works.
    import re
    path = re.search(r"/password-reset/confirm/[^/\s]+/", body).group(0)
    assert client.get(path).status_code == 200


def test_password_reset_sms_is_rate_limited(client, post, no_cache):
    configure()
    user = make_user(phone_number="0733000009")
    for _ in range(3):
        client.post("/password-reset/", {"email": user.email})
    assert post.call_count == 1


def test_password_reset_unknown_email_sends_no_sms(client, post, no_cache):
    configure()
    client.post("/password-reset/", {"email": "ghost@example.com"})
    assert post.call_count == 0


def test_prod_discards_mail_when_no_mail_server(monkeypatch):
    from tests.test_security import load_prod_settings
    prod = load_prod_settings(monkeypatch, SECRET_KEY="k" * 50, EMAIL_HOST="")
    assert prod.MAILERS["default"]["BACKEND"].endswith("dummy.EmailBackend")
    assert "mail.E001" in prod.SILENCED_SYSTEM_CHECKS
    prod = load_prod_settings(monkeypatch, SECRET_KEY="k" * 50, EMAIL_HOST="smtp.example.org")
    assert prod.MAILERS["default"]["BACKEND"].endswith("smtp.EmailBackend")
