"""
Dashboard pages in apps/home (index, services, human resources,
infrastructure, help, legacy template pages).
"""

import pytest
from django.urls import reverse

from tests.conftest import grant, logged_in_client

pytestmark = pytest.mark.django_db


@pytest.fixture
def world(world):
    """The services / HR / infrastructure pages need view_facilities (they
    were open to anyone before), as System Administrators have in production."""
    grant(world["staff"], "view_facilities")
    return world


@pytest.mark.parametrize("name", ["services", "human_resources", "infrastructure"])
def test_facility_pages_need_view_facilities(staff_client, name):
    r = staff_client.get(reverse(name))
    assert r.status_code == 302 and r.url == "/dashboard/"


def test_dashboard_counts(world):
    r = logged_in_client(world["staff"]).get(reverse("home"))
    assert r.status_code == 200
    ctx = r.context
    assert ctx["total_facilities"] == 1
    assert ctx["total_conversations"] == 1
    assert ctx["total_messages"] == 1
    assert ctx["total_music_tracks"] == 1
    assert ctx["total_services"] == 1
    assert ctx["total_contacts"] == 1
    assert ctx["total_infrastructure"] == 1
    assert ctx["segment"] == "index"


def test_dashboard_on_empty_database(staff_client):
    r = staff_client.get(reverse("home"))
    assert r.status_code == 200
    assert r.context["total_facilities"] == 0


class TestServicesPage:
    def test_lists_services(self, world):
        c = logged_in_client(world["staff"])
        r = c.get(reverse("services"))
        assert r.status_code == 200
        assert r.context["total_services"] == 1

    @pytest.mark.parametrize("params,count", [
        ({"search": "medical"}, 1), ({"search": "parklands gbv"}, 1), ({"search": "zzz"}, 0),
    ])
    def test_search(self, world, params, count):
        r = logged_in_client(world["staff"]).get(reverse("services"), params)
        assert len(r.context["page_obj"]) == count

    def test_search_matches_service_name(self, world):
        r = logged_in_client(world["staff"]).get(reverse("services"), {"search": "counselling"})
        assert len(r.context["page_obj"]) == 1

    def test_filters(self, world):
        c = logged_in_client(world["staff"])
        r = c.get(reverse("services"), {"category": world["service_category"].pk,
                                        "facility": world["facility"].pk})
        assert len(r.context["page_obj"]) == 1

    def test_add_redirects_to_facilities(self, staff_client):
        r = staff_client.get(reverse("add_service"))
        assert r.status_code == 302 and r["Location"] == reverse("facilities:facility_list")


class TestHumanResourcesPage:
    def test_page(self, world):
        c = logged_in_client(world["staff"])
        r = c.get(reverse("human_resources"))
        assert r.status_code == 200
        for params in ({"search": "+2547"}, {"contact_type": world["contact_type"].pk},
                       {"facility": world["facility"].pk}):
            assert c.get(reverse("human_resources"), params).status_code == 200

    def test_add_redirects(self, staff_client):
        assert staff_client.get(reverse("add_staff")).status_code == 302


class TestInfrastructurePage:
    def test_page_and_filters(self, world):
        c = logged_in_client(world["staff"])
        r = c.get(reverse("infrastructure"))
        assert r.status_code == 200
        for params in ({"search": "shelter"}, {"infrastructure_type": world["infra_type"].pk},
                       {"condition": world["condition"].pk}, {"facility": world["facility"].pk}):
            assert c.get(reverse("infrastructure"), params).status_code == 200


def test_help_page(staff_client):
    r = staff_client.get(reverse("help"))
    assert r.status_code == 200
    assert r.context["segment"] == "help"


@pytest.mark.parametrize("name", ["icons", "tables"])
def test_legacy_template_pages_render(staff_client, name):
    assert staff_client.get(reverse(name)).status_code == 200


def test_missing_legacy_page_is_a_real_404(staff_client):
    assert staff_client.get("/billing/").status_code == 404


def test_favicon_redirect(client):
    r = client.get("/favicon.ico")
    assert r.status_code == 301
    assert r["Location"].endswith("favicon.ico")


def test_swagger_and_redoc_render(client):
    assert client.get("/swagger/").status_code == 200
    assert client.get("/redoc/").status_code == 200
    r = client.get("/swagger.json")
    assert r.status_code == 200
    spec = r.json()
    # the schema is limited to the /api/ urlconf (paths are relative to it)
    assert "/facilities/" in spec["paths"] and "/auth/token/" in spec["paths"]
