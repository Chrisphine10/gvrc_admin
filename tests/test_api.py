"""
REST API under /api/ (DRF, session or "Token <key>" auth, IsAuthenticated).
"""

import pytest
from rest_framework.test import APIClient

from apps.authentication.models import CustomToken

pytestmark = pytest.mark.django_db

AUTH_REQUIRED_GET = [
    "/api/facilities/", "/api/facilities/map/", "/api/statistics/", "/api/lookups/",
    "/api/geography/", "/api/geography/counties/", "/api/geography/constituencies/",
    "/api/geography/wards/",
]
AUTH_REQUIRED_POST = [
    "/api/facilities/search/", "/api/facilities/emergency/", "/api/facilities/gbv-services/",
    "/api/facilities/referral-chain/", "/api/analytics/contact-interaction/",
    "/api/analytics/referral-outcome/",
]


@pytest.fixture
def api(staff_user):
    c = APIClient()
    token = CustomToken.objects.create(user=staff_user)
    c.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return c


@pytest.mark.parametrize("path", AUTH_REQUIRED_GET)
def test_get_requires_authentication(path):
    r = APIClient().get(path)
    assert r.status_code in (401, 403)
    assert "detail" in r.json()


@pytest.mark.parametrize("path", AUTH_REQUIRED_POST)
def test_post_requires_authentication(path):
    r = APIClient().post(path, {}, format="json")
    assert r.status_code in (401, 403)


def test_detail_requires_authentication(world):
    r = APIClient().get(f"/api/facilities/{world['facility'].pk}/")
    assert r.status_code in (401, 403)


def test_status_and_hello_are_public():
    c = APIClient()
    body = c.get("/api/status/").json()
    assert body["status"] == "active" and "timestamp" in body
    assert c.get("/api/hello/").json() == {"message": "Hello, Hodi Admin API!"}


def test_session_auth_also_works(staff_client):
    assert staff_client.get("/api/statistics/").status_code == 200


def test_csrf_enforced_for_session_authenticated_writes(staff_user):
    c = APIClient(enforce_csrf_checks=True)
    c.force_login(staff_user)
    r = c.post("/api/analytics/referral-outcome/",
               {"from_facility": 1, "to_facility": 2, "service_accessed": True}, format="json")
    assert r.status_code == 403
    assert "CSRF" in r.json()["detail"]


# ---------------------------------------------------------------------------
# Facilities
# ---------------------------------------------------------------------------

class TestFacilityEndpoints:
    def test_list_shape(self, api, world):
        r = api.get("/api/facilities/")
        assert r.status_code == 200
        body = r.json()
        assert body["count"] == 1
        item = body["results"][0]
        assert item["facility_id"] == world["facility"].pk
        assert "facility_name" in item

    def test_list_empty(self, api):
        r = api.get("/api/facilities/")
        assert r.status_code == 200
        assert r.json()["count"] == 0

    def test_detail_shape(self, api, world):
        r = api.get(f"/api/facilities/{world['facility'].pk}/")
        assert r.status_code == 200
        assert r.json()["facility_name"] == "Parklands GBV Centre"

    def test_detail_404(self, api):
        assert api.get("/api/facilities/99999/").status_code == 404

    def test_complete_view(self, api, world):
        r = api.get(f"/api/facilities/{world['facility'].pk}/complete/")
        assert r.status_code == 200
        assert r.json()["facility_id"] == world["facility"].pk

    def test_map(self, api, world):
        r = api.get("/api/facilities/map/")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_search(self, api, world):
        r = api.post("/api/facilities/search/", {"search": "Parklands"}, format="json")
        assert r.status_code == 200

    def test_emergency_services(self, api, world):
        r = api.post("/api/facilities/emergency/",
                     {"latitude": "-1.2640", "longitude": "36.8030",
                      "service_types": ["Medical"]}, format="json")
        assert r.status_code == 200
        assert r.json()["emergency_contacts"]["police"] == "999"

    def test_emergency_validation(self, api):
        r = api.post("/api/facilities/emergency/", {}, format="json")
        assert r.status_code == 400
        assert {"latitude", "longitude"} <= set(r.json())

    def test_gbv_services_validation(self, api):
        assert api.post("/api/facilities/gbv-services/", {}, format="json").status_code == 400

    def test_referral_chain_validation(self, api):
        assert api.post("/api/facilities/referral-chain/", {}, format="json").status_code == 400


# ---------------------------------------------------------------------------
# Statistics / lookups / geography
# ---------------------------------------------------------------------------

def test_statistics(api, world):
    body = api.get("/api/statistics/").json()
    assert body["total_facilities"] == 1
    assert body["operational_facilities"] == 1
    assert body["counties_count"] == 1
    assert body["facilities_with_coordinates"] == 1
    assert body["facilities_by_status"] == {"Operational": 1}


def test_lookups(api, lookups):
    body = api.get("/api/lookups/").json()
    assert set(body) == {"counties", "operational_statuses", "service_categories",
                         "contact_types", "owner_types", "gbv_categories"}
    assert {s["status_name"] for s in body["operational_statuses"]} == {"Operational", "Closed"}
    assert set(body["gbv_categories"][0]) == {"gbv_category_id", "category_name",
                                              "description", "icon_url"}


def test_geography_lists(api, geo):
    counties = api.get("/api/geography/counties/").json()
    assert counties[0]["county_name"] == "Nairobi"
    assert {"county_id", "county_name", "county_code"} <= set(counties[0])
    cons = api.get("/api/geography/constituencies/").json()
    assert cons[0]["constituency_name"] == "Westlands"
    wards = api.get("/api/geography/wards/").json()
    assert wards[0]["ward_name"] == "Parklands"


def test_consolidated_geography(api, geo):
    body = api.get("/api/geography/").json()
    assert len(body) == 1
    text = str(body)
    assert "Westlands" in text and "Parklands" in text


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

def test_referral_outcome(api):
    r = api.post("/api/analytics/referral-outcome/",
                 {"from_facility": 1, "to_facility": 2, "service_accessed": True,
                  "satisfaction_rating": 5}, format="json")
    assert r.status_code == 201
    assert r.json()["success"] is True


@pytest.mark.parametrize("rating", [0, 6])
def test_referral_outcome_rating_bounds(api, rating):
    r = api.post("/api/analytics/referral-outcome/",
                 {"from_facility": 1, "to_facility": 2, "service_accessed": True,
                  "satisfaction_rating": rating}, format="json")
    assert r.status_code == 400


def test_contact_interaction_requires_contact_id(api):
    assert api.post("/api/analytics/contact-interaction/", {}, format="json").status_code == 400


def test_contact_interaction_unknown_contact(api):
    r = api.post("/api/analytics/contact-interaction/", {"contact_id": 99999}, format="json")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Admin chat API
# ---------------------------------------------------------------------------

def test_chat_notifications_require_staff(world, plain_user):
    c = APIClient()
    assert c.get("/api/chat/admin/notifications/unread/").status_code in (401, 403)
    c.force_login(plain_user)
    assert c.get("/api/chat/admin/notifications/unread/").status_code == 403


def test_chat_notifications_for_staff(world):
    c = APIClient()
    c.force_login(world["admin"])
    r = c.get("/api/chat/admin/notifications/unread/")
    assert r.status_code == 200
