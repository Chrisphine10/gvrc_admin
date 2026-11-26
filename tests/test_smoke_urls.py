"""
URL smoke test: every routed URL, GET, as anonymous / staff-without-role /
superuser. Nothing may answer 500 or raise.

URLs come from tests/urlwalk.py, which walks the live URLconf, so routes added
later (map-config endpoint, SMS app, ...) are covered without editing this
file. URL parameters are filled from the ``world`` fixture by parameter name;
an unknown parameter gets "1" (a 404 is fine, a 500 is not).

A second test asserts that anonymous visitors cannot read anything that is not
public. Known holes are marked xfail(strict=True) with the file:line of the
missing check, so the test turns red (XPASS) once the code is fixed and the
marker can be removed.
"""

import pytest
from django.apps import apps as django_apps
from django.test import Client

from tests.urlwalk import all_routes

pytestmark = pytest.mark.django_db

# Admin history pages and the bare "<object_id>/" redirect add hundreds of
# near-identical cases without exercising different code.
_SKIP_SUFFIXES = ("_history",)


def _wanted(route):
    if route.name.endswith(_SKIP_SUFFIXES):
        return False
    if route.name.startswith("admin:") and route.name.endswith("<unnamed>"):
        return False
    if route.name == "admin:view_on_site":
        return False
    return True


ROUTES = [r for r in all_routes() if _wanted(r)]


def _value_for(route, param, world):
    name = route.name
    if param == "pk":
        if "notification" in name:
            return world["notification"].pk
        if "chat" in name or "conversation" in name:
            return world["conversation"].pk
        if "facility" in name:
            return world["facility"].pk
        if "session" in name:
            return world["mobile_session"].device_id
        if "music" in name:
            return world["music"].pk
        if "document" in name:
            return world["document"].pk
        return 1
    if param == "object_id" and name.startswith("admin:"):
        # admin:<app>_<model>_<view>  ->  first row of that model, if any
        label = name.split(":", 1)[1].rsplit("_", 1)[0]
        for model in django_apps.get_models():
            if f"{model._meta.app_label}_{model._meta.model_name}" == label:
                obj = model._default_manager.order_by("pk").first()
                return obj.pk if obj is not None else 1
        return 1
    simple = {
        "facility_id": world["facility"].pk,
        "user_id": world["staff"].pk,
        "role_id": world["role"].pk,
        "permission_id": world["permission"].pk,
        "county_id": world["county"].pk,
        "constituency_id": world["constituency"].pk,
        "ward_id": world["ward"].pk,
        "document_id": world["document"].pk,
        "music_id": world["music"].pk,
        "conversation_id": world["conversation"].pk,
        "message_id": world["message"].pk,
        "status_id": world["status"].pk,
        "type_id": world["contact_type"].pk,
        "category_id": world["service_category"].pk,
        "token": "not-a-real-token",
        "format": ".json",
        "app_label": "authentication",
        "url": "nothing-here/",
    }
    return simple.get(param, 1)


def build_path(route, world):
    return route.build({p: _value_for(route, p, world) for p in route.params})


def _is_mobile(route):
    return route.template.startswith("mobile/") or route.template.startswith("api/mobile/")


def _get(client, path, **extra):
    """GET without letting a view exception escape as a test error."""
    try:
        return client.get(path, **extra), None
    except Exception as exc:  # noqa: BLE001 - we want to report any crash
        return None, exc


# Every route that used to 500 here has been fixed (Nov 2026).
KNOWN_500 = {}


def _smoke_params():
    out = []
    for r in ROUTES:
        marks = []
        if r.name in KNOWN_500:
            marks.append(pytest.mark.xfail(strict=True, reason=KNOWN_500[r.name]))
        out.append(pytest.param(r, marks=marks, id=r.id))
    return out


@pytest.mark.parametrize("route", _smoke_params())
def test_no_server_error(route, world):
    path = build_path(route, world)
    callers = {
        "anonymous": Client(raise_request_exception=False),
        "staff-without-role": Client(raise_request_exception=False),
        "superuser": Client(raise_request_exception=False),
    }
    callers["staff-without-role"].force_login(world["staff"])
    callers["superuser"].force_login(world["admin"])

    requests_to_make = [(who, c, {}) for who, c in callers.items()]
    if _is_mobile(route):
        # Also exercise the real code path behind the device-session check.
        requests_to_make.append((
            "anonymous+device_id", Client(raise_request_exception=False),
            {"data": {"device_id": world["mobile_session"].device_id}},
        ))

    failures = []
    for who, client, extra in requests_to_make:
        response, exc = _get(client, path, **extra)
        if exc is not None:
            failures.append(f"{who}: raised {type(exc).__name__}: {exc}")
        elif response.status_code >= 500:
            failures.append(f"{who}: HTTP {response.status_code}")
    assert not failures, f"GET {path}\n" + "\n".join(failures)


# ---------------------------------------------------------------------------
# Anonymous access
# ---------------------------------------------------------------------------

# Pages that are meant to be reachable without logging in.
PUBLIC = {
    "landing", "login", "register", "logout",
    "password_reset", "password_reset_done", "password_reset_complete",
    "password_reset_confirm",
    "schema-json", "schema-swagger-ui", "schema-redoc",
    "api:api-status", "api:hello-world",
    "admin:login", "admin:jsi18n",
    # Static leftovers rendered by home.views.pages / help_page; they contain
    # no data.
    "help", "billing", "rtl", "vr", "new-user", "icons", "notifications",
    "tables", "upgrade",
}


def _public(route):
    if route.name in PUBLIC:
        return True
    # Mobile endpoints authenticate the device, not a user; they are checked
    # in test_mobile_api.py (403 JSON without a device session).
    if _is_mobile(route):
        return True
    return False


# All the anonymous-access holes found here were closed in Nov 2026.
KNOWN_ANON_HOLES = {}


def _anon_params():
    out = []
    for r in ROUTES:
        if _public(r):
            continue
        marks = []
        if r.name in KNOWN_ANON_HOLES:
            marks.append(pytest.mark.xfail(strict=True, reason=KNOWN_ANON_HOLES[r.name]))
        out.append(pytest.param(r, marks=marks, id=r.id))
    return out


@pytest.mark.parametrize("route", _anon_params())
def test_anonymous_is_refused(route, world):
    """Anonymous GET of a non-public page: redirect, 401/403, 404 or 405 -
    never 200 with content."""
    path = build_path(route, world)
    response = Client().get(path)
    assert response.status_code in (301, 302, 400, 401, 403, 404, 405), (
        f"anonymous GET {path} -> {response.status_code}"
    )
    if response.status_code in (301, 302):
        location = response["Location"]
        assert not location.startswith("http") or "testserver" in location, location


def test_walker_found_the_main_areas():
    """Guard against the walker silently finding nothing."""
    names = {r.name for r in ROUTES}
    for expected in ("login", "home", "facilities:facility_list",
                     "api:facility-list", "mobile:mobile-session-create-session",
                     "documents:document_list", "music:music_list",
                     "chat:conversation_list"):
        assert expected in names
    assert len(ROUTES) > 150
