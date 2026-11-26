"""
Model methods, managers and string representations not covered by the
feature tests.
"""

import datetime

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.authentication.backends import CustomTokenAuthentication, CustomUserBackend
from apps.authentication.models import (
    ApiToken, CustomToken, Permission, UserProfile, UserRole, UserSession,
)
from tests.conftest import make_user

pytestmark = pytest.mark.django_db
User = get_user_model()


class TestUserManager:
    def test_create_user_sets_username_and_profile(self):
        u = User.objects.create_user("Mixed@EXAMPLE.com", "Jane Doe", "+254700123123", "pw-12345")
        assert u.email == "Mixed@example.com"          # domain normalised
        assert u.username == u.email
        assert u.check_password("pw-12345")
        assert UserProfile.objects.filter(user=u).exists()
        assert not u.is_staff and not u.is_superuser and not u.verified

    @pytest.mark.parametrize("args", [
        ("", "Name", "+254700000010"), ("a@b.co", "", "+254700000011"), ("a@b.co", "Name", ""),
    ])
    def test_create_user_requires_email_name_phone(self, args):
        with pytest.raises(ValueError):
            User.objects.create_user(*args, password="x")

    def test_create_superuser(self):
        su = User.objects.create_superuser("su@example.com", "Super User", "+254700000020", "pw")
        assert su.is_staff and su.is_superuser and su.verified

    @pytest.mark.parametrize("flag", ["is_staff", "is_superuser"])
    def test_create_superuser_rejects_false_flags(self, flag):
        with pytest.raises(ValueError):
            User.objects.create_superuser("su2@example.com", "S U", "+254700000021", "pw",
                                          **{flag: False})

    def test_natural_key_is_email(self):
        u = make_user(email="nk@example.com")
        assert User.objects.get_by_natural_key("nk@example.com") == u

    def test_email_and_phone_unique(self):
        from django.db import IntegrityError, transaction
        make_user(email="dup@example.com", phone_number="+254700000099")
        with pytest.raises(IntegrityError), transaction.atomic():
            make_user(email="dup@example.com")
        with pytest.raises(IntegrityError), transaction.atomic():
            make_user(phone_number="+254700000099")


class TestUserModel:
    def test_names_and_str(self):
        u = make_user(email="n@example.com", full_name="Wanjiru Mwangi Kamau")
        assert str(u) == "Wanjiru Mwangi Kamau (n@example.com)"
        assert u.get_full_name() == "Wanjiru Mwangi Kamau"
        assert u.get_short_name() == "Wanjiru"
        u.full_name = ""
        assert u.get_short_name() == ""

    def test_avatar_url(self):
        u = make_user()
        assert u.get_avatar_url() == "/static/assets/img/brand/hodi app logo.png"
        u.userprofile.avatar_url = "https://cdn.example/a.png"
        u.userprofile.save()
        u.refresh_from_db()
        assert u.get_avatar_url() == "https://cdn.example/a.png"
        UserProfile.objects.filter(user=u).delete()
        u = User.objects.get(pk=u.pk)
        assert u.get_avatar_url().endswith("hodi app logo.png")

    def test_profile_display_avatar_falls_back(self):
        u = make_user()
        p = u.userprofile
        p.avatar_url = ""
        assert p.display_avatar.endswith("hodi app logo.png")
        assert str(p) == f"Profile for {u.full_name}"


class TestTokensAndSessions:
    def test_custom_token_generates_key(self):
        u = make_user()
        t = CustomToken.objects.create(user=u)
        assert len(t.key) == 40 and str(t) == f"Token for {u.full_name}"
        t2 = CustomToken(user=make_user(), key="fixed")
        t2.save()
        assert t2.key == "fixed"

    def test_token_authentication(self):
        from django.test import RequestFactory
        u = make_user()
        t = CustomToken.objects.create(user=u)
        auth = CustomTokenAuthentication()
        rf = RequestFactory()
        assert auth.authenticate(rf.get("/", HTTP_AUTHORIZATION=f"Token {t.key}")) == (u, t)
        assert auth.authenticate(rf.get("/")) is None
        assert auth.authenticate(rf.get("/", HTTP_AUTHORIZATION="Token")) is None
        assert auth.authenticate(rf.get("/", HTTP_AUTHORIZATION="Token a b")) is None
        assert auth.authenticate(rf.get("/", HTTP_AUTHORIZATION="Token nope")) is None
        u.is_active = False
        u.save()
        assert auth.authenticate(rf.get("/", HTTP_AUTHORIZATION=f"Token {t.key}")) is None

    def test_backend(self):
        u = make_user(password="secret-1")
        be = CustomUserBackend()
        assert be.authenticate(None, email=u.email, password="secret-1") == u
        assert be.authenticate(None, email=u.email, password="bad") is None
        assert be.authenticate(None, email="ghost@example.com", password="x") is None
        assert be.authenticate(None) is None
        assert be.get_user(u.pk) == u
        assert be.get_user(99999) is None
        u.is_active = False
        u.save()
        assert be.authenticate(None, email=u.email, password="secret-1") is None
        assert be.get_user(u.pk) is None

    def test_create_user_session_helper(self):
        from django.test import RequestFactory
        from apps.authentication.backends import create_user_session
        u = make_user()
        req = RequestFactory().get("/", HTTP_X_FORWARDED_FOR="203.0.113.5, 10.0.0.1")
        s = create_user_session(u, req)
        assert s.ip_address == "203.0.113.5"
        assert s.expires_at > timezone.now() + datetime.timedelta(hours=23)
        assert str(s) == f"{u.full_name} - {s.session_id}"

    def test_api_token_str(self):
        u = make_user()
        t = ApiToken.objects.create(user=u, token_name="ci", token_hash="h",
                                    expires_at=timezone.now())
        assert str(t) == f"Token ci for {u.full_name}"


class TestRbacModels:
    def test_strs(self):
        role = UserRole.objects.create(role_name="Counsellor")
        assert str(role) == "Counsellor"
        perm = Permission.objects.get(permission_name="view_facilities")
        assert str(perm) == "view facilities"


class TestLookupAndAnalyticsModels:
    def test_lookup_strs(self, lookups):
        assert [str(lookups[k]) for k in ("status", "contact_type", "service_category",
                                          "owner_type", "gbv_category", "infra_type",
                                          "condition", "doc_type")] == [
            "Operational", "Phone", "Medical", "Government", "Physical Violence",
            "Shelter", "Good", "PDF"]

    def test_contact_interaction_and_audit_strs(self, world):
        from apps.analytics.models import AuditTrail, ContactInteraction
        ci = ContactInteraction.objects.create(contact=world["contact"],
                                               device=world["mobile_session"])
        assert str(ci) == f"Interaction {ci.pk} from device device-test-0001"
        anon = ContactInteraction.objects.create(contact=world["contact"])
        assert str(anon).endswith("from device Unknown")
        audit = AuditTrail.objects.create(table_name="facilities", record_id=7,
                                          action_type="UPDATE", event_category="DATA")
        assert str(audit) == "UPDATE on facilities.7"
