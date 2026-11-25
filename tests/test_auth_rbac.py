"""
Authentication (login/logout/register/password reset/profile) and the custom
RBAC layer in apps/authentication/permissions.py.
"""

import datetime
import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from apps.authentication import permissions as P
from apps.authentication.models import (
    Permission, RolePermission, UserRole, UserRoleAssignment, UserSession,
)
from tests.conftest import grant, logged_in_client, make_user

pytestmark = pytest.mark.django_db
User = get_user_model()


def _session_user_id(client):
    return client.session.get("_auth_user_id")


# ---------------------------------------------------------------------------
# Login / logout
# ---------------------------------------------------------------------------

class TestLogin:
    def test_login_page_renders(self, client):
        r = client.get(reverse("login"))
        assert r.status_code == 200
        assert b"password" in r.content.lower()

    def test_valid_credentials_log_in_and_redirect_to_dashboard(self, client, staff_user, password):
        r = client.post(reverse("login"), {"email": staff_user.email, "password": password})
        assert r.status_code == 302
        assert r["Location"] == "/dashboard/"
        assert _session_user_id(client) == str(staff_user.pk)

    def test_login_records_a_user_session_row(self, client, staff_user, password):
        client.post(reverse("login"), {"email": staff_user.email, "password": password})
        assert UserSession.objects.filter(user=staff_user).count() == 1
        assert client.session.get("session_id")

    def test_login_honours_relative_next(self, client, staff_user, password):
        r = client.post(reverse("login") + "?next=/facilities/",
                        {"email": staff_user.email, "password": password})
        assert r["Location"] == "/facilities/"

    def test_login_refuses_offsite_next(self, client, staff_user, password):
        r = client.post(reverse("login") + "?next=https://evil.example/phish",
                        {"email": staff_user.email, "password": password})
        assert "evil.example" not in r.get("Location", "")

    def test_wrong_password_is_rejected(self, client, staff_user):
        r = client.post(reverse("login"), {"email": staff_user.email, "password": "nope"})
        assert r.status_code == 200
        assert _session_user_id(client) is None
        assert b"Invalid email or password" in r.content or b"Please" in r.content

    def test_unknown_email_is_rejected(self, client):
        r = client.post(reverse("login"), {"email": "ghost@example.com", "password": "x"})
        assert r.status_code == 200
        assert _session_user_id(client) is None

    def test_malformed_email_is_rejected(self, client):
        r = client.post(reverse("login"), {"email": "not-an-email", "password": "x"})
        assert r.status_code == 200
        assert _session_user_id(client) is None

    def test_inactive_user_cannot_log_in(self, client, password):
        user = make_user(password=password, is_staff=True, is_active=False)
        r = client.post(reverse("login"), {"email": user.email, "password": password})
        assert r.status_code == 200
        assert _session_user_id(client) is None

    def test_email_login_is_case_sensitive_on_stored_value(self, client, staff_user, password):
        # normalize_email lowercases only the domain part; logging in with the
        # stored address must work.
        r = client.post(reverse("login"), {"email": staff_user.email, "password": password})
        assert r.status_code == 302

    def test_logout_ends_session_and_marks_user_session_expired(self, client, staff_user, password):
        client.post(reverse("login"), {"email": staff_user.email, "password": password})
        sess = UserSession.objects.get(user=staff_user)
        r = client.get(reverse("logout"))
        assert r.status_code == 302
        assert r["Location"] == "/"
        assert _session_user_id(client) is None
        sess.refresh_from_db()
        assert sess.expires_at <= timezone.now()

    def test_logout_when_not_logged_in_is_harmless(self, client):
        assert client.get(reverse("logout")).status_code == 302

    def test_dashboard_requires_login(self, client):
        r = client.get(reverse("home"))
        assert r.status_code == 302
        assert r["Location"].startswith("/login/")

    def test_landing_redirects_authenticated_users_to_dashboard(self, staff_client):
        r = staff_client.get(reverse("landing"))
        assert r.status_code == 302
        assert r["Location"] == reverse("home")

    def test_landing_shows_public_counts(self, client, facility_factory, admin_user):
        facility_factory(admin_user)
        r = client.get(reverse("landing"))
        assert r.status_code == 200
        assert r.context["total_facilities"] == 1
        assert r.context["operational_facilities"] == 1

    def test_dashboard_renders_for_logged_in_user(self, staff_client):
        r = staff_client.get(reverse("home"))
        assert r.status_code == 200


class TestDrfTokenEndpoint:
    def test_obtain_token_with_valid_credentials(self, client, staff_user, password):
        r = client.post("/api/auth/token/", {"email": staff_user.email, "password": password},
                        content_type="application/json")
        assert r.status_code == 200
        body = r.json()
        assert len(body["token"]) == 40
        assert body["user_id"] == staff_user.pk
        assert "password" not in json.dumps(body)

    def test_token_is_reused_on_second_call(self, client, staff_user, password):
        payload = {"email": staff_user.email, "password": password}
        first = client.post("/api/auth/token/", payload, content_type="application/json").json()
        second = client.post("/api/auth/token/", payload, content_type="application/json").json()
        assert first["token"] == second["token"]
        assert second["created"] is False

    @pytest.mark.parametrize("payload", [
        {}, {"email": "x@example.com"}, {"email": "x@example.com", "password": "bad"},
    ])
    def test_bad_credentials_give_400(self, client, staff_user, payload):
        r = client.post("/api/auth/token/", payload, content_type="application/json")
        assert r.status_code == 400
        assert "token" not in r.json()

    def test_inactive_user_gets_no_token(self, client, password):
        u = make_user(password=password, is_active=False)
        r = client.post("/api/auth/token/", {"email": u.email, "password": password},
                        content_type="application/json")
        assert r.status_code == 400

    def test_token_authenticates_api_requests(self, client, staff_user, password):
        token = client.post("/api/auth/token/", {"email": staff_user.email, "password": password},
                            content_type="application/json").json()["token"]
        api = Client()
        assert api.get("/api/statistics/").status_code in (401, 403)
        r = api.get("/api/statistics/", HTTP_AUTHORIZATION=f"Token {token}")
        assert r.status_code == 200

    @pytest.mark.parametrize("header", ["Token", "Token a b", "Bearer abc", "Token wrong"])
    def test_malformed_or_unknown_token_is_refused(self, header):
        r = Client().get("/api/statistics/", HTTP_AUTHORIZATION=header)
        assert r.status_code in (401, 403)


# ---------------------------------------------------------------------------
# Registration and password reset
# ---------------------------------------------------------------------------

class TestRegistration:
    def _payload(self, **kw):
        data = {
            "full_name": "New Person", "email": "new@example.com",
            "phone_number": "+254711000999",
            "password1": "Sup3r-Secret-Pass", "password2": "Sup3r-Secret-Pass",
        }
        data.update(kw)
        return data

    def test_register_creates_non_staff_user(self, client):
        r = client.post(reverse("register"), self._payload())
        assert r.status_code == 200
        user = User.objects.get(email="new@example.com")
        assert user.username == "new@example.com"
        assert not user.is_staff and not user.is_superuser
        assert user.check_password("Sup3r-Secret-Pass")

    def test_register_rejects_duplicate_email(self, client, staff_user):
        client.post(reverse("register"), self._payload(email=staff_user.email))
        assert User.objects.filter(email=staff_user.email).count() == 1

    def test_register_rejects_duplicate_phone(self, client, staff_user):
        r = client.post(reverse("register"), self._payload(phone_number=staff_user.phone_number))
        assert not User.objects.filter(email="new@example.com").exists()
        assert r.context["form"].errors.get("phone_number")

    def test_register_rejects_mismatched_passwords(self, client):
        client.post(reverse("register"), self._payload(password2="different-Pass-1"))
        assert not User.objects.filter(email="new@example.com").exists()

    def test_registered_user_gets_no_dashboard_permissions(self, client):
        client.post(reverse("register"), self._payload())
        user = User.objects.get(email="new@example.com")
        assert not P.has_permission(user, "view_facilities")
        assert list(P.get_user_permissions(user)) == []


class TestPasswordReset:
    def test_reset_form_renders(self, client):
        assert client.get(reverse("password_reset")).status_code == 200

    def test_reset_emails_the_link_and_never_shows_it(self, client, staff_user, mailoutbox):
        r = client.post(reverse("password_reset"), {"email": staff_user.email}, follow=True)
        assert r.status_code == 200
        assert b"password-reset/confirm/" not in r.content
        assert len(mailoutbox) == 1
        assert mailoutbox[0].to == [staff_user.email]
        assert "/password-reset/confirm/" in mailoutbox[0].body

    def test_reset_for_unknown_email_looks_the_same(self, client, staff_user, mailoutbox):
        known = client.post(reverse("password_reset"), {"email": staff_user.email})
        unknown = client.post(reverse("password_reset"), {"email": "ghost@example.com"})
        assert known.status_code == unknown.status_code == 302
        assert known["Location"] == unknown["Location"]
        assert len(mailoutbox) == 1  # only the real account got mail

    def test_reset_link_changes_the_password_once(self, client, staff_user, mailoutbox):
        import re
        client.post(reverse("password_reset"), {"email": staff_user.email})
        path = re.search(r"/password-reset/confirm/[^/\s]+/", mailoutbox[0].body).group(0)
        assert client.get(path).status_code == 200
        r = client.post(path, {"password1": "Brand-New-Pass-2026", "password2": "Brand-New-Pass-2026"})
        assert r.status_code == 302
        staff_user.refresh_from_db()
        assert staff_user.check_password("Brand-New-Pass-2026")
        # The token is tied to the old password hash, so it cannot be reused.
        assert client.get(path).status_code == 302

    def test_reset_rejects_weak_password(self, client, staff_user, mailoutbox, password):
        import re
        client.post(reverse("password_reset"), {"email": staff_user.email})
        path = re.search(r"/password-reset/confirm/[^/\s]+/", mailoutbox[0].body).group(0)
        r = client.post(path, {"password1": "123", "password2": "123"})
        assert r.status_code == 200 and r.context["form"].errors
        staff_user.refresh_from_db()
        assert staff_user.check_password(password)

    def test_confirm_get_redirects_back_to_request_page(self, client):
        r = client.get(reverse("password_reset_confirm", kwargs={"token": "abc"}))
        assert r.status_code == 302
        assert r["Location"] == reverse("password_reset")

    def test_confirm_post_never_changes_a_password(self, client, staff_user, password):
        client.post(reverse("password_reset_confirm", kwargs={"token": "abc"}),
                    {"password1": "Other-Pass-123", "password2": "Other-Pass-123"})
        staff_user.refresh_from_db()
        assert staff_user.check_password(password)

    def test_done_and_complete_pages_render(self, client):
        assert client.get(reverse("password_reset_done")).status_code == 200
        assert client.get(reverse("password_reset_complete")).status_code == 200


# ---------------------------------------------------------------------------
# Profile / change password
# ---------------------------------------------------------------------------

class TestProfile:
    def test_profile_requires_login(self, client):
        assert client.get(reverse("profile")).status_code == 302

    def test_profile_get(self, staff_client, staff_user):
        r = staff_client.get(reverse("profile"))
        assert r.status_code == 200
        assert r.context["profile"] == staff_user.userprofile

    def test_profile_update(self, staff_client, staff_user):
        r = staff_client.post(reverse("profile"), {
            "profile_form": "1", "full_name": "Renamed Person",
            "phone_number": "+254733000111", "bio": "Hi", "department": "Ops",
            "job_title": "Lead", "avatar_url": "",
        })
        assert r.status_code == 302
        staff_user.refresh_from_db()
        assert staff_user.full_name == "Renamed Person"
        assert staff_user.userprofile.department == "Ops"

    def test_invalid_profile_post_re_renders_with_errors(self, staff_user, plain_user):
        c = Client(raise_request_exception=False)
        c.force_login(staff_user)
        r = c.post(reverse("profile"), {
            "profile_form": "1", "full_name": "X Y", "phone_number": plain_user.phone_number,
        })
        assert r.status_code == 200

    def test_change_password(self, staff_client, staff_user, password):
        r = staff_client.post(reverse("change_password"), {
            "current_password": password,
            "new_password1": "Brand-New-Pass-9", "new_password2": "Brand-New-Pass-9",
        })
        assert r.status_code == 302
        assert r["Location"] == reverse("logout")
        staff_user.refresh_from_db()
        assert staff_user.check_password("Brand-New-Pass-9")

    @pytest.mark.parametrize("current,new1,new2", [
        ("wrong", "Brand-New-Pass-9", "Brand-New-Pass-9"),
        (None, "Brand-New-Pass-9", "Different-Pass-9"),
        (None, "short", "short"),
        (None, "1234567890", "1234567890"),
    ])
    def test_change_password_validation(self, staff_client, staff_user, password, current, new1, new2):
        r = staff_client.post(reverse("change_password"), {
            "current_password": current or password,
            "new_password1": new1, "new_password2": new2,
        })
        assert r.status_code == 200
        staff_user.refresh_from_db()
        assert staff_user.check_password(password)


# ---------------------------------------------------------------------------
# RBAC primitives
# ---------------------------------------------------------------------------

class TestRbacFunctions:
    def test_seed_migration_created_permission_catalogue(self):
        names = set(Permission.objects.values_list("permission_name", flat=True))
        for expected in ("view_facilities", "add_facilities", "change_facilities",
                         "delete_facilities", "view_users", "change_roles",
                         "view_chat", "change_chat", "manage_system", "view_admin"):
            assert expected in names

    def test_anonymous_has_nothing(self):
        from django.contrib.auth.models import AnonymousUser
        anon = AnonymousUser()
        assert P.has_permission(anon, "view_facilities") is False
        assert P.has_permission(None, "view_facilities") is False
        assert P.has_role(anon, "Super Admin") is False
        assert P.has_any_role(anon, ["Super Admin"]) is False
        assert P.get_user_permissions(anon).count() == 0
        assert P.get_user_roles(anon).count() == 0

    def test_superuser_has_everything(self, admin_user):
        assert P.has_permission(admin_user, "anything_at_all")
        assert P.has_role(admin_user, "Whatever")
        assert P.has_any_role(admin_user, ["X"])
        assert P.get_user_permissions(admin_user).count() == Permission.objects.count()

    def test_user_without_role_has_nothing(self, staff_user):
        assert not P.has_permission(staff_user, "view_facilities")
        assert not P.has_role(staff_user, "Facility Manager")

    def test_role_grants_only_its_permissions(self, staff_user):
        role = grant(staff_user, "view_facilities", role_name="Facility Viewer")
        assert P.has_permission(staff_user, "view_facilities")
        assert not P.has_permission(staff_user, "add_facilities")
        assert P.has_role(staff_user, "Facility Viewer")
        assert P.has_any_role(staff_user, ["Nope", "Facility Viewer"])
        assert not P.has_any_role(staff_user, ["Nope"])
        assert list(P.get_user_roles(staff_user)) == [role]
        assert list(P.get_user_permissions(staff_user).values_list(
            "permission_name", flat=True)) == ["view_facilities"]

    def test_permissions_from_several_roles_combine_without_duplicates(self, staff_user):
        grant(staff_user, "view_facilities", "view_music")
        grant(staff_user, "view_music", "view_documents")
        names = sorted(P.get_user_permissions(staff_user).values_list("permission_name", flat=True))
        assert names == ["view_documents", "view_facilities", "view_music"]

    def test_expired_assignment_grants_nothing(self, staff_user):
        grant(staff_user, "view_facilities",
              expires_at=timezone.now() - datetime.timedelta(days=1))
        assert not P.has_permission(staff_user, "view_facilities")

    def test_assignment_with_future_expiry_still_grants(self, staff_user):
        grant(staff_user, "view_facilities",
              expires_at=timezone.now() + datetime.timedelta(days=30))
        assert P.has_permission(staff_user, "view_facilities")

    def test_context_processor(self, staff_user):
        grant(staff_user, "view_music")
        req = RequestFactory().get("/")
        req.user = staff_user
        ctx = P.user_permissions_context(req)
        assert ctx["user_permission_names"] == ["view_music"]
        assert callable(ctx["has_permission"])

    def test_context_processor_anonymous(self):
        from django.contrib.auth.models import AnonymousUser
        req = RequestFactory().get("/")
        req.user = AnonymousUser()
        assert P.user_permissions_context(req) == {}


class TestDecorators:
    def _call(self, decorator, user):
        from django.contrib.messages.storage.fallback import FallbackStorage
        from django.http import HttpResponse

        @decorator
        def view(request):
            return HttpResponse("ok")

        req = RequestFactory().get("/x/")
        req.user = user
        req.session = {}
        req._messages = FallbackStorage(req)
        return view(req)

    def test_permission_required(self, staff_user):
        r = self._call(P.permission_required("view_music"), staff_user)
        assert r.status_code == 302 and r["Location"] == "/dashboard/"
        grant(staff_user, "view_music")
        assert self._call(P.permission_required("view_music"), staff_user).status_code == 200

    def test_permission_required_custom_redirect(self, staff_user):
        r = self._call(P.permission_required("view_music", redirect_url="/elsewhere/",
                                             message="no"), staff_user)
        assert r["Location"] == "/elsewhere/"

    def test_role_required(self, staff_user):
        assert self._call(P.role_required("Editors"), staff_user).status_code == 302
        grant(staff_user, role_name="Editors")
        assert self._call(P.role_required("Editors"), staff_user).status_code == 200

    def test_any_role_required(self, staff_user):
        dec = P.any_role_required(["A", "B"])
        assert self._call(dec, staff_user).status_code == 302
        grant(staff_user, role_name="B")
        assert self._call(dec, staff_user).status_code == 200

    def test_staff_required(self, staff_user, plain_user):
        assert self._call(P.staff_required(), plain_user).status_code == 302
        assert self._call(P.staff_required(), staff_user).status_code == 200

    def test_superuser_required(self, staff_user, admin_user):
        assert self._call(P.superuser_required(redirect_url="/no/"), staff_user)["Location"] == "/no/"
        assert self._call(P.superuser_required(), admin_user).status_code == 200

    def test_ajax_permission_required_returns_json_403(self, staff_user):
        r = self._call(P.ajax_permission_required("change_roles"), staff_user)
        assert r.status_code == 403
        assert json.loads(r.content)["success"] is False

    def test_ajax_role_required(self, staff_user):
        assert self._call(P.ajax_role_required("Boss"), staff_user).status_code == 403
        grant(staff_user, role_name="Boss")
        assert self._call(P.ajax_role_required("Boss"), staff_user).status_code == 200

    def test_drf_permission_classes(self, staff_user, plain_user, admin_user):
        from django.contrib.auth.models import AnonymousUser
        req = RequestFactory().get("/")
        for user, staff, sup in ((staff_user, True, False), (plain_user, False, False),
                                 (admin_user, True, True), (AnonymousUser(), False, False)):
            req.user = user
            assert bool(P.StaffPermission().has_permission(req, None)) is staff
            assert bool(P.SuperuserPermission().has_permission(req, None)) is sup
        req.user = staff_user
        assert not P.HasPermissionPermission("view_music").has_permission(req, None)
        assert not P.HasRolePermission("R").has_permission(req, None)
        assert not P.HasAnyRolePermission(["R"]).has_permission(req, None)
        grant(staff_user, "view_music", role_name="R")
        assert P.HasPermissionPermission("view_music").has_permission(req, None)
        assert P.HasRolePermission("R").has_permission(req, None)
        assert P.HasAnyRolePermission(["R"]).has_permission(req, None)

    def test_check_api_helpers(self, staff_user):
        assert P.check_api_permission(staff_user, "view_music").status_code == 403
        assert P.check_api_role(staff_user, "R").status_code == 403
        grant(staff_user, "view_music", role_name="R")
        assert P.check_api_permission(staff_user, "view_music") is None
        assert P.check_api_role(staff_user, "R") is None


# ---------------------------------------------------------------------------
# User / role / permission management views
# ---------------------------------------------------------------------------

class TestUserAndRoleViews:
    def test_user_list_refused_without_permission(self, staff_client):
        r = staff_client.get(reverse("user_list"))
        assert r.status_code == 302 and r["Location"] == "/dashboard/"

    def test_user_list_with_permission_and_search(self, staff_user, plain_user):
        grant(staff_user, "view_users")
        c = logged_in_client(staff_user)
        r = c.get(reverse("user_list"), {"search": "Plain"})
        assert r.status_code == 200
        assert list(r.context["users"]) == [plain_user]

    def test_user_detail_requires_view_users(self, plain_user, admin_user):
        r = logged_in_client(plain_user).get(reverse("user_detail", args=[admin_user.pk]))
        assert r.status_code in (302, 403)

    def test_user_detail_for_privileged_user(self, admin_client_, plain_user):
        r = admin_client_.get(reverse("user_detail", args=[plain_user.pk]))
        assert r.status_code == 200

    def test_user_detail_404_for_inactive(self, admin_client_, password):
        u = make_user(password=password, is_active=False)
        assert admin_client_.get(reverse("user_detail", args=[u.pk])).status_code == 404

    def test_user_edit(self, admin_client_, plain_user):
        r = admin_client_.post(reverse("user_edit", args=[plain_user.pk]), {
            "full_name": "Edited Name", "phone_number": plain_user.phone_number,
        })
        assert r.status_code == 302
        plain_user.refresh_from_db()
        assert plain_user.full_name == "Edited Name"

    def test_user_edit_refused_without_change_users(self, staff_user, plain_user):
        grant(staff_user, "view_users")
        r = logged_in_client(staff_user).post(reverse("user_edit", args=[plain_user.pk]), {
            "full_name": "Hacked", "phone_number": plain_user.phone_number,
        })
        assert r.status_code == 302
        plain_user.refresh_from_db()
        assert plain_user.full_name != "Hacked"

    def test_role_list_requires_view_roles(self, staff_client, staff_user):
        assert staff_client.get(reverse("role_list")).status_code == 302
        grant(staff_user, "view_roles")
        assert staff_client.get(reverse("role_list"), {"search": "x"}).status_code == 200

    def test_role_create_edit_delete(self, admin_client_):
        r = admin_client_.post(reverse("role_create"), {"role_name": "Counsellor",
                                                        "description": "d"})
        role = UserRole.objects.get(role_name="Counsellor")
        assert r["Location"] == reverse("role_detail", args=[role.pk])
        assert admin_client_.get(reverse("role_detail", args=[role.pk])).status_code == 200

        admin_client_.post(reverse("role_edit", args=[role.pk]),
                           {"role_name": "Senior Counsellor"})
        role.refresh_from_db()
        assert role.role_name == "Senior Counsellor"

        assert admin_client_.get(reverse("role_delete", args=[role.pk])).status_code == 200
        r = admin_client_.post(reverse("role_delete", args=[role.pk]))
        assert r["Location"] == reverse("role_list")
        assert not UserRole.objects.filter(pk=role.pk).exists()

    def test_role_create_requires_name(self, admin_client_):
        r = admin_client_.post(reverse("role_create"), {"role_name": ""})
        assert r.status_code == 200
        assert UserRole.objects.count() == 0

    def test_role_create_refused_without_permission(self, staff_client):
        staff_client.post(reverse("role_create"), {"role_name": "Sneaky"})
        assert not UserRole.objects.filter(role_name="Sneaky").exists()

    def test_permission_crud(self, admin_client_):
        r = admin_client_.post(reverse("permission_create"), {
            "permission_name": "export_reports", "resource_name": "reports",
            "action_name": "export",
        })
        assert r.status_code == 302
        perm = Permission.objects.get(permission_name="export_reports")
        admin_client_.post(reverse("permission_edit", args=[perm.pk]), {
            "permission_name": "export_reports", "resource_name": "reports",
            "action_name": "download",
        })
        perm.refresh_from_db()
        assert perm.action_name == "download"
        admin_client_.post(reverse("permission_delete", args=[perm.pk]))
        assert not Permission.objects.filter(pk=perm.pk).exists()

    def test_permission_create_requires_all_fields(self, admin_client_):
        before = Permission.objects.count()
        r = admin_client_.post(reverse("permission_create"), {"permission_name": "x"})
        assert r.status_code == 200
        assert Permission.objects.count() == before

    def test_permission_list_search(self, admin_client_):
        r = admin_client_.get(reverse("permission_list"), {"search": "facilities"})
        assert r.status_code == 200
        assert set(r.context["permissions_by_resource"]) == {"facilities"}

    def test_assign_and_remove_permission_on_role(self, admin_client_, admin_user):
        role = UserRole.objects.create(role_name="R1")
        perm = Permission.objects.get(permission_name="view_music")
        url = reverse("assign_permission_to_role", args=[role.pk])
        r = admin_client_.post(url, json.dumps({"permission_id": perm.pk}),
                               content_type="application/json")
        assert r.json()["success"] is True
        assert RolePermission.objects.filter(role=role, permission=perm,
                                             granted_by=admin_user).exists()
        again = admin_client_.post(url, json.dumps({"permission_id": perm.pk}),
                                   content_type="application/json").json()
        assert again["success"] is False
        missing = admin_client_.post(url, "{}", content_type="application/json").json()
        assert missing["success"] is False

        r = admin_client_.post(reverse("remove_permission_from_role", args=[role.pk, perm.pk]))
        assert r.json()["success"] is True
        assert not RolePermission.objects.filter(role=role).exists()

    def test_assign_permission_refused_for_non_privileged(self, staff_client):
        role = UserRole.objects.create(role_name="R2")
        r = staff_client.post(reverse("assign_permission_to_role", args=[role.pk]),
                              json.dumps({"permission_id": 1}), content_type="application/json")
        assert r.status_code == 403

    def test_assign_permission_is_post_only(self, admin_client_):
        role = UserRole.objects.create(role_name="R3")
        assert admin_client_.get(
            reverse("assign_permission_to_role", args=[role.pk])).status_code == 405

    def test_assign_and_remove_role_on_user(self, admin_client_, plain_user):
        role = UserRole.objects.create(role_name="R4")
        url = reverse("assign_role_to_user", args=[plain_user.pk])
        assert admin_client_.post(url, json.dumps({"role_id": role.pk}),
                                  content_type="application/json").json()["success"]
        assert UserRoleAssignment.objects.filter(user=plain_user, role=role).exists()
        dup = admin_client_.post(url, json.dumps({"role_id": role.pk}),
                                 content_type="application/json").json()
        assert dup["success"] is False
        r = admin_client_.post(reverse("remove_role_from_user", args=[plain_user.pk, role.pk]))
        assert r.json()["success"]
        assert not UserRoleAssignment.objects.filter(user=plain_user).exists()

    def test_non_privileged_user_cannot_grant_himself_a_role(self, staff_user):
        role = UserRole.objects.create(role_name="Super Admin X")
        c = logged_in_client(staff_user)
        c.post(reverse("assign_role_to_user", args=[staff_user.pk]),
               json.dumps({"role_id": role.pk}), content_type="application/json")
        assert not UserRoleAssignment.objects.filter(user=staff_user).exists()

    def test_user_analytics(self, admin_client_):
        assert admin_client_.get(reverse("user_analytics")).status_code == 200
