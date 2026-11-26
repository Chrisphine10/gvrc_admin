"""Administrators add users; the new person sets their own password via a link."""

import re
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings

from apps.sms.models import SmsSettings
from tests.conftest import grant, logged_in_client, make_user

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def bonga():
    s = SmsSettings.get_solo()
    s.client_id, s.api_key, s.api_secret, s.service_id = "cid", "key", "secret", "sid"
    s.save()
    resp = mock.Mock(ok=True, status_code=200, reason="OK", text="")
    resp.json.return_value = {"status": 222, "status_message": "Success", "unique_id": 1}
    with override_settings(SMS_NETWORK_ENABLED=True), mock.patch("apps.sms.services.requests.post", return_value=resp) as p:
        yield p


@pytest.fixture
def no_cache():
    from django.core.cache import cache
    cache.clear()
    yield
    cache.clear()


def payload(**kw):
    data = {"full_name": "Amina Otieno", "email": "Amina@Example.com", "phone_number": "0711222333", "is_staff": "on"}
    data.update(kw)
    return data


def test_needs_add_users_permission():
    viewer = make_user(is_staff=True)
    grant(viewer, "view_users")
    c = logged_in_client(viewer)
    assert c.get("/users/new/").status_code in (302, 403)
    c.post("/users/new/", payload())
    assert not User.objects.filter(email="amina@example.com").exists()


def test_user_list_shows_add_button_only_with_permission(admin_client_):
    viewer = make_user(is_staff=True)
    grant(viewer, "view_users")
    assert b"/users/new/" not in logged_in_client(viewer).get("/users/").content
    assert b"/users/new/" in admin_client_.get("/users/").content


def test_admin_adds_user_with_role_and_link(admin_client_, admin_user, bonga, mailoutbox, no_cache):
    from apps.authentication.models import UserRole, UserRoleAssignment
    role = UserRole.objects.create(role_name="Case Worker")
    r = admin_client_.post("/users/new/", payload(role=role.pk))
    assert r.status_code == 302, r.content
    u = User.objects.get(email="amina@example.com")
    assert u.is_staff and not u.has_usable_password() and u.phone_number == "+254711222333"
    assert UserRoleAssignment.objects.filter(user=u, role=role, assigned_by=admin_user).exists()
    # email and SMS both carry the same one-time link
    assert mailoutbox[0].to == ["amina@example.com"] and "account" in mailoutbox[0].subject.lower()
    sms = bonga.call_args.kwargs["files"]["txtMessage"][1]
    assert "account was created" in sms
    path = re.search(r"/password-reset/confirm/[^/\s]+/", sms).group(0)
    assert path in mailoutbox[0].body
    # the link lets them choose a password, once
    c = logged_in_client(make_user())
    c.logout()
    assert c.post(path, {"password1": "Fresh-Pass-2026x", "password2": "Fresh-Pass-2026x"}).status_code == 302
    u.refresh_from_db()
    assert u.check_password("Fresh-Pass-2026x")


@pytest.mark.parametrize("field,value,message", [
    ("phone_number", "020123456", "Kenyan mobile"),
    ("email", "not-an-email", "valid email"),
])
def test_bad_input_is_rejected(admin_client_, field, value, message):
    r = admin_client_.post("/users/new/", payload(**{field: value}))
    assert r.status_code == 200 and message.encode() in r.content
    assert User.objects.count() == 1  # only the admin


def test_duplicate_email_and_phone_rejected(admin_client_, admin_user):
    r = admin_client_.post("/users/new/", payload(email=admin_user.email.upper()))
    assert b"already exists" in r.content
    r = admin_client_.post("/users/new/", payload(phone_number="0799999999"))  # admin's +254799999999
    assert b"already exists" in r.content
    assert User.objects.count() == 1
