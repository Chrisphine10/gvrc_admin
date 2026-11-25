"""
Geography AJAX endpoints (/geography/api/...) and model helpers.
(The read-only geography pages live in apps/common and are not tested here.)
"""

import json

import pytest
from django.core.exceptions import ValidationError
from django.test import Client

from apps.geography.models import Constituency, County, Ward
from tests.conftest import grant, logged_in_client

pytestmark = pytest.mark.django_db


@pytest.fixture
def geo_admin(staff_user):
    grant(staff_user, "view_geography", "add_geography", "change_geography", "delete_geography")
    return logged_in_client(staff_user)


def jpost(client, url, body):
    return client.post(url, json.dumps(body), content_type="application/json")


class TestReadEndpoints:
    def test_login_required(self, client, geo):
        r = client.get(f"/geography/api/constituencies/{geo['county'].pk}/")
        assert r.status_code == 302 and "/login/" in r["Location"]

    def test_constituencies_and_wards_for_parent(self, staff_client, geo):
        body = staff_client.get(f"/geography/api/constituencies/{geo['county'].pk}/").json()
        assert body["success"] and body["constituencies"][0]["constituency_name"] == "Westlands"
        body = staff_client.get(f"/geography/api/wards/{geo['constituency'].pk}/").json()
        assert body["wards"] == [{"ward_id": geo["ward"].pk, "ward_name": "Parklands",
                                  "ward_code": "047-01-01"}]
        assert staff_client.get("/geography/api/wards/99999/").json()["wards"] == []

    def test_all_counties_and_constituencies(self, staff_client, geo):
        assert staff_client.get("/geography/api/counties/").json()["counties"] == [
            {"county_id": geo["county"].pk, "county_name": "Nairobi"}]
        cons = staff_client.get("/geography/api/constituencies/").json()["constituencies"]
        assert cons[0]["county__county_name"] == "Nairobi"

    def test_search(self, staff_client, geo):
        r = staff_client.get("/geography/api/search/", {"q": "park"})
        res = r.json()["results"]
        assert res["counties"] == [] and res["wards"][0]["county_name"] == "Nairobi"
        res = staff_client.get("/geography/api/search/", {"q": "047"}).json()["results"]
        assert len(res["counties"]) == 1 and len(res["constituencies"]) == 1

    def test_search_requires_query(self, staff_client):
        assert staff_client.get("/geography/api/search/").status_code == 400

    def test_check_facility_connections(self, staff_client, geo, facility_factory, admin_user):
        url = "/geography/api/check-facilities/"
        assert staff_client.get(url, {"type": "ward", "id": geo["ward"].pk}).json()["has_facilities"] is False
        facility_factory(admin_user)
        for t, obj in (("county", geo["county"]), ("constituency", geo["constituency"]),
                       ("ward", geo["ward"])):
            assert staff_client.get(url, {"type": t, "id": obj.pk}).json()["has_facilities"] is True
        assert staff_client.get(url).status_code == 400
        assert staff_client.get(url, {"type": "planet", "id": 1}).status_code == 400
        assert staff_client.get(url, {"type": "ward", "id": 99999}).status_code == 404


class TestWriteEndpoints:
    def test_permission_required(self, staff_client, geo):
        r = jpost(staff_client, "/geography/api/add/", {"type": "county", "name": "X", "code": "X"})
        assert r.status_code == 302
        assert not County.objects.filter(county_code="X").exists()

    def test_get_is_rejected(self, geo_admin):
        for url in ("/geography/api/add/", "/geography/api/edit/", "/geography/api/delete/"):
            assert geo_admin.get(url).status_code == 405

    def test_add_county_constituency_ward(self, geo_admin):
        r = jpost(geo_admin, "/geography/api/add/", {"type": "county", "name": "Kisumu", "code": "042"})
        county_id = r.json()["county"]["id"]
        r = jpost(geo_admin, "/geography/api/add/", {"type": "constituency", "name": "Kisumu East",
                                                     "code": "042-01", "county_id": county_id})
        assert r.json()["constituency"]["county_name"] == "Kisumu"
        cons_id = r.json()["constituency"]["id"]
        r = jpost(geo_admin, "/geography/api/add/", {"type": "ward", "name": "Kajulu",
                                                     "code": "042-01-01", "constituency_id": cons_id})
        assert r.json()["success"]
        assert Ward.objects.get(ward_code="042-01-01").constituency.county.county_name == "Kisumu"

    @pytest.mark.parametrize("body,needle", [
        ({"type": "county", "name": "Nairobi", "code": "NEW"}, "name already exists"),
        ({"type": "county", "name": "New", "code": "047"}, "code already exists"),
        ({"type": "county", "name": "", "code": "1"}, "required"),
        ({"type": "constituency", "name": "C", "code": "C", "county_id": 99999}, "Invalid county"),
        ({"type": "ward", "name": "W", "code": "W", "constituency_id": 99999}, "Invalid constituency"),
        ({"type": "ward", "name": "parklands", "code": "NEWW"}, "required"),
        ({"type": "galaxy"}, "Invalid item type"),
    ])
    def test_add_validation(self, geo_admin, geo, body, needle):
        r = jpost(geo_admin, "/geography/api/add/", body)
        assert r.status_code == 400
        assert needle in r.json()["error"]

    def test_add_invalid_json(self, geo_admin):
        r = geo_admin.post("/geography/api/add/", "{not json", content_type="application/json")
        assert r.status_code == 400 and r.json()["error"] == "Invalid JSON data"

    def test_edit(self, geo_admin, geo):
        r = jpost(geo_admin, "/geography/api/edit/", {"type": "county", "id": geo["county"].pk,
                                                      "name": "Nairobi City", "code": "047"})
        assert r.json()["success"]
        geo["county"].refresh_from_db()
        assert geo["county"].county_name == "Nairobi City"

    def test_edit_rejects_duplicate_name(self, geo_admin, geo):
        County.objects.create(county_name="Mombasa", county_code="001")
        r = jpost(geo_admin, "/geography/api/edit/", {"type": "county", "id": geo["county"].pk,
                                                      "name": "mombasa", "code": "047"})
        assert r.status_code == 400

    def test_edit_needs_type_and_id(self, geo_admin):
        assert jpost(geo_admin, "/geography/api/edit/", {}).status_code == 400

    def test_delete_blocked_while_children_or_facilities_exist(self, geo_admin, geo,
                                                              facility_factory, admin_user):
        facility_factory(admin_user)
        for t, obj in (("county", geo["county"]), ("constituency", geo["constituency"]),
                       ("ward", geo["ward"])):
            r = jpost(geo_admin, "/geography/api/delete/", {"type": t, "id": obj.pk})
            assert r.status_code == 400, t
            assert "facilities" in r.json()["error"]
        assert Ward.objects.filter(pk=geo["ward"].pk).exists()

    def test_delete_bottom_up(self, geo_admin, geo):
        r = jpost(geo_admin, "/geography/api/delete/", {"type": "county", "id": geo["county"].pk})
        assert r.status_code == 400 and "constituencies" in r.json()["error"]
        assert jpost(geo_admin, "/geography/api/delete/",
                     {"type": "ward", "id": geo["ward"].pk}).json()["success"]
        assert jpost(geo_admin, "/geography/api/delete/",
                     {"type": "constituency", "id": geo["constituency"].pk}).json()["success"]
        assert jpost(geo_admin, "/geography/api/delete/",
                     {"type": "county", "id": geo["county"].pk}).json()["success"]
        assert County.objects.count() == 0

    def test_delete_missing(self, geo_admin):
        r = jpost(geo_admin, "/geography/api/delete/", {"type": "ward", "id": 99999})
        assert r.status_code == 404

    def test_writes_are_csrf_protected(self, staff_user, geo):
        grant(staff_user, "delete_geography")
        c = Client(enforce_csrf_checks=True)
        c.force_login(staff_user)
        r = c.post("/geography/api/delete/", json.dumps({"type": "ward", "id": geo["ward"].pk}),
                   content_type="application/json")
        assert r.status_code == 403


class TestModels:
    def test_strs(self, geo):
        assert str(geo["county"]) == "Nairobi"
        assert str(geo["constituency"]) == "Westlands - Nairobi"
        assert str(geo["ward"]) == "Parklands - Westlands"

    def test_can_delete_rules(self, geo, facility_factory, admin_user):
        county, cons, ward = geo["county"], geo["constituency"], geo["ward"]
        assert not county.can_delete() and not cons.can_delete() and ward.can_delete()
        assert not county.has_facilities()
        facility_factory(admin_user)
        assert county.has_facilities() and cons.has_facilities() and ward.has_facilities()
        assert not ward.can_delete()

    @pytest.mark.parametrize("model,kwargs", [
        (County, {"county_name": " ", "county_code": "1"}),
        (County, {"county_name": "A", "county_code": ""}),
    ])
    def test_clean(self, model, kwargs):
        with pytest.raises(ValidationError):
            model(**kwargs).clean()

    def test_clean_child_models(self, geo):
        with pytest.raises(ValidationError):
            Constituency(constituency_name="", constituency_code="x", county=geo["county"]).clean()
        with pytest.raises(ValidationError):
            Ward(ward_name="W", ward_code=" ", constituency=geo["constituency"]).clean()
        Ward(ward_name="W", ward_code="w", constituency=geo["constituency"]).clean()
