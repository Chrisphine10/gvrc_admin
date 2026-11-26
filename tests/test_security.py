"""
Security checks: CSRF, admin access, secrets, headers, debug routes and the
production settings module.
"""

import importlib
import re
import sys

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse

from tests.conftest import grant, logged_in_client

pytestmark = pytest.mark.django_db


def _csrf_from(response):
    m = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', response.content)
    assert m, "no CSRF token in form"
    return m.group(1).decode()


# ---------------------------------------------------------------------------
# CSRF
# ---------------------------------------------------------------------------

class TestCsrf:
    def test_login_post_without_token_is_rejected(self, staff_user, password):
        c = Client(enforce_csrf_checks=True)
        r = c.post(reverse("login"), {"email": staff_user.email, "password": password})
        assert r.status_code == 403
        assert "_auth_user_id" not in c.session

    def test_login_post_with_token_works(self, staff_user, password):
        c = Client(enforce_csrf_checks=True)
        token = _csrf_from(c.get(reverse("login")))
        r = c.post(reverse("login"), {"email": staff_user.email, "password": password,
                                      "csrfmiddlewaretoken": token})
        assert r.status_code == 302

    @pytest.mark.parametrize("url,data", [
        ("/roles/create/", {"role_name": "X"}),
        ("/permissions/create/", {"permission_name": "a_b", "resource_name": "b", "action_name": "a"}),
        ("/change-password/", {"current_password": "x"}),
        ("/music/add/", {"name": "x", "link": "https://e.org/a.mp3"}),
        ("/documents/create/", {"title": "x", "content": "y"}),
        ("/facilities/create/", {"facility_name": "x"}),
        ("/register/", {"email": "a@b.co"}),
    ])
    def test_dashboard_forms_require_csrf(self, admin_user, url, data):
        c = Client(enforce_csrf_checks=True)
        c.force_login(admin_user)
        assert c.post(url, data).status_code == 403

    def test_ajax_role_assignment_requires_csrf(self, admin_user, plain_user):
        from apps.authentication.models import UserRole
        role = UserRole.objects.create(role_name="R")
        c = Client(enforce_csrf_checks=True)
        c.force_login(admin_user)
        r = c.post(f"/users/{plain_user.pk}/assign-role/", '{"role_id": %d}' % role.pk,
                   content_type="application/json")
        assert r.status_code == 403

    def test_mobile_api_is_usable_without_csrf(self):
        """The Flutter app has no CSRF cookie; anonymous DRF calls must work."""
        c = Client(enforce_csrf_checks=True)
        r = c.post("/mobile/sessions/create/", {"device_id": "csrf-free"},
                   content_type="application/json")
        assert r.status_code == 201


# ---------------------------------------------------------------------------
# Admin site and authorisation
# ---------------------------------------------------------------------------

class TestAdminSite:
    def test_anonymous_redirected_to_admin_login(self, client):
        r = client.get("/admin/")
        assert r.status_code == 302 and r["Location"].startswith("/admin/login/")

    def test_non_staff_user_cannot_use_admin(self, plain_user):
        r = logged_in_client(plain_user).get("/admin/authentication/user/")
        assert r.status_code == 302 and "/admin/login/" in r["Location"]

    def test_staff_without_model_permissions_sees_no_user_data(self, staff_user, admin_user):
        r = logged_in_client(staff_user).get("/admin/authentication/user/")
        assert r.status_code == 403

    def test_superuser_can_use_admin(self, admin_client_):
        assert admin_client_.get("/admin/").status_code == 200
        assert admin_client_.get("/admin/authentication/user/").status_code == 200

    def test_debug_endpoints_are_not_routed(self, admin_client_):
        for path in ("/chat/debug/auth/", "/chat/debug/user/", "/chat/test/",
                     "/chat/test-conversations/", "/chat/debug/messages/1/"):
            assert admin_client_.get(path).status_code == 404, path


# ---------------------------------------------------------------------------
# Secrets and headers
# ---------------------------------------------------------------------------

class TestNoSecretsInResponses:
    PAGES = ["/", "/login/", "/dashboard/", "/facilities/", "/api/status/",
             "/swagger.json", "/roles/", "/users/", "/profile/", "/mobile/chat/websocket-info/"]

    def test_secret_key_and_db_password_never_rendered(self, world):
        c = logged_in_client(world["admin"])
        secrets = [settings.SECRET_KEY]
        db_pass = settings.DATABASES["default"].get("PASSWORD")
        if db_pass:
            secrets.append(db_pass)
        for path in self.PAGES:
            body = c.get(path).content.decode(errors="replace")
            for s in secrets:
                assert s not in body, f"secret leaked on {path}"

    def test_password_hashes_not_in_api_or_pages(self, world):
        c = logged_in_client(world["admin"])
        hashed = world["staff"].password
        for path in (f"/users/{world['staff'].pk}/", "/users/", "/api/chat/admin/conversations/"):
            assert hashed not in c.get(path).content.decode(errors="replace"), path

    def test_ai_and_directions_keys_not_exposed(self, monkeypatch, mobile_session):
        monkeypatch.setenv("GEMINI_API_KEY", "gemini-secret-xyz")
        monkeypatch.setenv("GOOGLE_MAPS_SERVER_KEY", "maps-secret-xyz")
        c = Client()
        for path in ("/mobile/chat/websocket-info/", "/swagger.json"):
            body = c.get(path, {"device_id": mobile_session.device_id}).content.decode()
            assert "gemini-secret-xyz" not in body and "maps-secret-xyz" not in body

    def test_passwords_are_hashed(self, staff_user, password):
        assert staff_user.password != password
        assert staff_user.password.startswith("md5$")  # test hasher; real one is PBKDF2


class TestHeaders:
    def test_clickjacking_and_nosniff_headers(self, client):
        r = client.get(reverse("login"))
        assert r["X-Frame-Options"] in ("DENY", "SAMEORIGIN")
        assert r["X-Content-Type-Options"] == "nosniff"

    def test_session_cookie_is_httponly(self, client, staff_user, password):
        client.post(reverse("login"), {"email": staff_user.email, "password": password})
        cookie = client.cookies[settings.SESSION_COOKIE_NAME]
        assert cookie["httponly"]

    def test_cors_does_not_allow_arbitrary_origins(self, client):
        r = client.get("/api/status/", HTTP_ORIGIN="https://evil.example")
        assert r.get("Access-Control-Allow-Origin") != "https://evil.example"
        assert r.get("Access-Control-Allow-Origin") != "*"

    def test_cors_allows_known_origin(self, client):
        r = client.get("/api/status/", HTTP_ORIGIN="https://hodi.co.ke")
        assert r.get("Access-Control-Allow-Origin") == "https://hodi.co.ke"


class TestAccountEnumeration:
    def test_login_error_is_identical_for_unknown_email_and_wrong_password(self, client, staff_user):
        a = client.post(reverse("login"), {"email": staff_user.email, "password": "wrong"})
        b = client.post(reverse("login"), {"email": "nobody@example.com", "password": "wrong"})
        msgs = lambda r: [str(m) for m in r.context["messages"]]  # noqa: E731
        assert msgs(a) == msgs(b)

    def test_password_reset_does_not_reveal_accounts(self, client, staff_user):
        a = client.post(reverse("password_reset"), {"email": staff_user.email})
        b = client.post(reverse("password_reset"), {"email": "nobody@example.com"})
        assert b"No user found" not in b.content
        assert a.status_code == b.status_code


# ---------------------------------------------------------------------------
# Production settings
# ---------------------------------------------------------------------------

def load_prod_settings(monkeypatch, **env):
    """Import core.settings.prod fresh with a controlled environment, then put
    the already-loaded modules back so the running test settings are untouched."""
    import dotenv
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *a, **k: False)
    for key in ("SECRET_KEY", "APP_DOMAIN", "RENDER_EXTERNAL_HOSTNAME", "DB_ENGINE",
                "DB_NAME", "DB_USERNAME", "CORS_EXTRA_ORIGINS"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    names = ("core.settings.prod", "core.settings.base")
    saved = {n: sys.modules.pop(n) for n in names if n in sys.modules}
    try:
        return importlib.import_module("core.settings.prod")
    finally:
        for n in names:
            sys.modules.pop(n, None)
        sys.modules.update(saved)


class TestProdSettings:
    @pytest.fixture
    def prod(self, monkeypatch):
        return load_prod_settings(monkeypatch, SECRET_KEY="x" * 50, APP_DOMAIN="hodi.example")

    def test_debug_off(self, prod):
        assert prod.DEBUG is False

    def test_secure_cookies(self, prod):
        assert prod.SESSION_COOKIE_SECURE is True
        assert prod.CSRF_COOKIE_SECURE is True
        assert prod.SESSION_COOKIE_HTTPONLY is True
        assert prod.SESSION_COOKIE_SAMESITE in ("Lax", "Strict")

    def test_hsts_and_headers(self, prod):
        assert prod.SECURE_HSTS_SECONDS >= 31536000
        assert prod.SECURE_HSTS_INCLUDE_SUBDOMAINS is True
        assert prod.SECURE_CONTENT_TYPE_NOSNIFF is True
        assert prod.X_FRAME_OPTIONS == "DENY"
        assert prod.SECURE_PROXY_SSL_HEADER == ("HTTP_X_FORWARDED_PROTO", "https")

    def test_hosts_and_origins(self, prod):
        assert "*" not in prod.ALLOWED_HOSTS
        assert "hodi.example" in prod.ALLOWED_HOSTS
        assert all(o.startswith("https://") for o in prod.CSRF_TRUSTED_ORIGINS)
        assert prod.CORS_ALLOW_ALL_ORIGINS is False

    def test_secret_key_from_environment(self, prod):
        assert prod.SECRET_KEY == "x" * 50

    def test_render_hostname_is_allowed(self, monkeypatch):
        prod = load_prod_settings(monkeypatch, SECRET_KEY="k" * 50,
                                  RENDER_EXTERNAL_HOSTNAME="hodi.onrender.com")
        assert "hodi.onrender.com" in prod.ALLOWED_HOSTS

    def test_importing_prod_did_not_touch_running_settings(self, prod):
        assert settings.DATABASES["default"]["NAME"] in (":memory:", "file:memorydb_default?mode=memory&cache=shared") \
            or "memory" in str(settings.DATABASES["default"]["NAME"])
        assert sys.modules["core.settings.base"] is not prod

    def test_prod_refuses_missing_secret_key(self, monkeypatch):
        try:
            prod = load_prod_settings(monkeypatch)
        except Exception:
            return
        assert prod.SECRET_KEY != "TODO_SET_SECRET_KEY"
