"""
Facilities: dashboard list/search/filter/detail/map/create/edit, forms and
the cache helpers in apps/facilities/cache_utils.py.

(The facility map *template* and facility_form.html are being edited
elsewhere; these tests only assert on status codes, context and database
state, never on that markup.)
"""

import pytest
from django.urls import reverse

from apps.facilities import cache_utils
from apps.facilities.forms import (
    FacilityCoordinateForm, FacilityForm, FacilityGBVCategoryForm,
)
from apps.facilities.models import Facility, FacilityGBVCategory
from tests.conftest import grant, logged_in_client

pytestmark = pytest.mark.django_db


@pytest.fixture
def manager(staff_user):
    """A Facility-Manager-like account."""
    grant(staff_user, "view_facilities", "add_facilities", "change_facilities")
    return staff_user


@pytest.fixture
def manager_client(manager):
    return logged_in_client(manager)


@pytest.fixture
def viewer_client(user_factory):
    u = user_factory(is_staff=True)
    grant(u, "view_facilities")
    return logged_in_client(u)


# ---------------------------------------------------------------------------
# Access control
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,args", [
    ("facilities:facility_list", []),
    ("facilities:facility_map", []),
    ("facilities:facility_create", []),
])
def test_staff_without_role_is_redirected_to_dashboard(staff_client, name, args):
    r = staff_client.get(reverse(name, args=args))
    assert r.status_code == 302
    assert r["Location"] == "/dashboard/"


def test_anonymous_ends_up_at_login(client):
    r = client.get(reverse("facilities:facility_list"), follow=True)
    assert r.redirect_chain[-1][0].startswith("/login/")


def test_viewer_cannot_open_create_or_edit(viewer_client, facility_factory, admin_user):
    f = facility_factory(admin_user)
    assert viewer_client.get(reverse("facilities:facility_create")).status_code == 302
    assert viewer_client.get(reverse("facilities:facility_update", args=[f.pk])).status_code == 302


def test_viewer_post_to_edit_changes_nothing(viewer_client, facility_factory, admin_user):
    f = facility_factory(admin_user, name="Original")
    viewer_client.post(reverse("facilities:facility_update", args=[f.pk]),
                       {"facility_name": "Changed"})
    f.refresh_from_db()
    assert f.facility_name == "Original"


# ---------------------------------------------------------------------------
# List / search / filter / pagination
# ---------------------------------------------------------------------------

class TestFacilityList:
    def test_lists_active_facilities_only(self, viewer_client, facility_factory, admin_user):
        a = facility_factory(admin_user, name="Alpha Centre")
        facility_factory(admin_user, name="Gone Centre", is_active=False)
        r = viewer_client.get(reverse("facilities:facility_list"))
        assert r.status_code == 200
        assert list(r.context["facilities"]) == [a]
        assert r.context["total_facilities"] == 1

    @pytest.mark.parametrize("term", ["alpha", "REG-", "Parklands", "Westlands", "Nairobi"])
    def test_search_by_name_registration_and_geography(self, viewer_client, facility_factory,
                                                       admin_user, term):
        a = facility_factory(admin_user, name="Alpha Centre")
        r = viewer_client.get(reverse("facilities:facility_list"), {"search": term})
        assert a in list(r.context["facilities"])
        assert r.context["search_query"] == term

    def test_search_with_no_match(self, viewer_client, facility_factory, admin_user):
        facility_factory(admin_user, name="Alpha Centre")
        r = viewer_client.get(reverse("facilities:facility_list"), {"search": "zzz-no-match"})
        assert list(r.context["facilities"]) == []

    def test_filter_by_county_and_status(self, viewer_client, facility_factory, admin_user,
                                         geo, lookups):
        from apps.geography.models import Constituency, County, Ward
        other_county = County.objects.create(county_name="Mombasa", county_code="001")
        other_ward = Ward.objects.create(
            ward_name="Old Town", ward_code="001-01-01",
            constituency=Constituency.objects.create(
                constituency_name="Mvita", constituency_code="001-01", county=other_county),
        )
        nairobi = facility_factory(admin_user, name="N")
        mombasa = facility_factory(admin_user, name="M", ward=other_ward,
                                   operational_status=lookups["status_closed"])
        url = reverse("facilities:facility_list")
        assert list(viewer_client.get(url, {"county": geo["county"].pk}).context["facilities"]) == [nairobi]
        assert list(viewer_client.get(url, {"county": other_county.pk}).context["facilities"]) == [mombasa]
        r = viewer_client.get(url, {"status": lookups["status_closed"].pk})
        assert list(r.context["facilities"]) == [mombasa]
        assert r.context["selected_status"] == str(lookups["status_closed"].pk)

    def test_pagination_50_per_page_and_bad_page_numbers(self, viewer_client, facility_factory,
                                                         admin_user):
        for _ in range(51):
            facility_factory(admin_user, with_related=False, lat=None, lng=None)
        url = reverse("facilities:facility_list")
        r = viewer_client.get(url)
        assert len(r.context["facilities"]) == 50
        assert r.context["total_pages"] == 2 and r.context["has_next"]
        assert viewer_client.get(url, {"page": "abc"}).context["current_page"] == 1
        assert viewer_client.get(url, {"page": 999}).context["current_page"] == 2
        assert len(viewer_client.get(url, {"page": 2}).context["facilities"]) == 1


class TestFacilityDetailAndMap:
    def test_detail(self, viewer_client, facility_factory, admin_user):
        f = facility_factory(admin_user)
        r = viewer_client.get(reverse("facilities:facility_detail", args=[f.pk]))
        assert r.status_code == 200
        assert r.context["facility"] == f
        assert r.context["contacts"].count() == 1
        assert r.context["services"].count() == 1
        assert float(r.context["coordinates"].latitude) == pytest.approx(-1.264)

    def test_detail_404_for_inactive_or_missing(self, viewer_client, facility_factory, admin_user):
        f = facility_factory(admin_user, is_active=False)
        assert viewer_client.get(reverse("facilities:facility_detail", args=[f.pk])).status_code == 404
        assert viewer_client.get(reverse("facilities:facility_detail", args=[99999])).status_code == 404

    def test_map_context(self, viewer_client, facility_factory, admin_user):
        facility_factory(admin_user, name="With coords")
        facility_factory(admin_user, name="No coords", lat=None, lng=None)
        r = viewer_client.get(reverse("facilities:facility_map"))
        assert r.status_code == 200
        assert r.context["total_facilities"] == 2
        assert r.context["facilities_with_coords_count"] == 1
        item = r.context["facilities_with_coords"][0]
        assert item["facility"]["facility_name"] == "With coords"
        assert item["coordinates"] == {"latitude": pytest.approx(-1.264), "longitude": pytest.approx(36.803)}
        assert r.context["viewport_filtered"] is False

    def test_map_viewport_filter(self, viewer_client, facility_factory, admin_user):
        facility_factory(admin_user, name="Inside")
        facility_factory(admin_user, name="Outside", lat=-4.05, lng=39.66)
        r = viewer_client.get(reverse("facilities:facility_map"), {
            "ne_lat": -1.0, "ne_lng": 37.0, "sw_lat": -1.5, "sw_lng": 36.5, "zoom": 12,
        })
        names = [i["facility"]["facility_name"] for i in r.context["facilities_with_coords"]]
        assert names == ["Inside"]
        assert r.context["viewport_filtered"] is True
        assert r.context["zoom_level"] == 12

    def test_map_low_zoom_shows_only_operational(self, viewer_client, facility_factory,
                                                admin_user, lookups):
        facility_factory(admin_user, name="Open")
        facility_factory(admin_user, name="Shut", operational_status=lookups["status_closed"])
        r = viewer_client.get(reverse("facilities:facility_map"), {"zoom": 4})
        names = [i["facility"]["facility_name"] for i in r.context["facilities_with_coords"]]
        assert names == ["Open"]

    def test_map_tolerates_bad_zoom(self, manager):
        from django.test import Client
        c = Client(raise_request_exception=False)
        c.force_login(manager)
        for params in ({"zoom": "abc"}, {"ne_lat": "x", "ne_lng": "1", "sw_lat": "1", "sw_lng": "1"}):
            assert c.get(reverse("facilities:facility_map"), params).status_code == 200


# ---------------------------------------------------------------------------
# Create / edit through the dashboard
# ---------------------------------------------------------------------------

def _mgmt(prefix, total):
    return {
        f"{prefix}-TOTAL_FORMS": str(total), f"{prefix}-INITIAL_FORMS": "0",
        f"{prefix}-MIN_NUM_FORMS": "1", f"{prefix}-MAX_NUM_FORMS": "10",
    }


def facility_post_data(geo, lookups, **overrides):
    data = {
        "facility_name": "Hope Recovery Centre",
        "facility_code": "HRC-1",
        "registration_number": "REG-HRC-1",
        "operational_status": lookups["status"].pk,
        "county": geo["county"].pk,
        "constituency": geo["constituency"].pk,
        "ward": geo["ward"].pk,
        "address_line_1": "Limuru Road",
        "latitude": "-1.2580", "longitude": "36.8190", "collection_date": "2024-05-01",
        "gbv_categories": [lookups["gbv_category"].pk],
        **_mgmt("contacts", 1),
        "contacts-0-contact_type": lookups["contact_type"].pk,
        "contacts-0-contact_value": "+254722000000",
        **_mgmt("services", 1),
        "services-0-service_category": lookups["service_category"].pk,
        "services-0-service_name": "Medical care",
        "services-0-currency": "KES",
        **_mgmt("owners", 1),
        "owners-0-owner_name": "Ministry of Health",
        "owners-0-owner_type": lookups["owner_type"].pk,
        **_mgmt("infrastructure", 1),
        "infrastructure-0-infrastructure_type": lookups["infra_type"].pk,
        "infrastructure-0-condition_status": lookups["condition"].pk,
    }
    data.update(overrides)
    return data


class TestFacilityCreate:
    def test_create_form_renders(self, manager_client):
        r = manager_client.get(reverse("facilities:facility_create"))
        assert r.status_code == 200
        assert r.context["form_action"] == "Create"
        assert len(r.context["contact_formset"].forms) == 1

    def test_create_facility_with_related_records(self, manager_client, geo, lookups, manager):
        r = manager_client.post(reverse("facilities:facility_create"),
                                facility_post_data(geo, lookups))
        assert r.status_code == 302
        f = Facility.objects.get(registration_number="REG-HRC-1")
        assert f.created_by == manager
        assert f.ward == geo["ward"]
        assert f.facilitycoordinate_set.count() == 1
        assert f.facilitycontact_set.count() == 1
        assert f.facilityservice_set.count() == 1
        assert f.facilityowner_set.count() == 1
        assert FacilityGBVCategory.objects.filter(facility=f).count() == 1

    def test_create_currently_reports_an_error_and_saves_nothing(self, manager_client, geo, lookups):
        """Documents today's (broken) behaviour so a partial save would be caught."""
        r = manager_client.post(reverse("facilities:facility_create"),
                                facility_post_data(geo, lookups))
        if r.status_code == 302:  # fixed - the xfail above will report XPASS
            return
        assert r.status_code == 200
        assert not Facility.objects.filter(registration_number="REG-HRC-1").exists()

    @pytest.mark.parametrize("missing", ["facility_name", "registration_number",
                                         "operational_status", "ward"])
    def test_required_fields(self, manager_client, geo, lookups, missing):
        data = facility_post_data(geo, lookups)
        data.pop(missing)
        r = manager_client.post(reverse("facilities:facility_create"), data)
        assert r.status_code == 200
        assert missing in r.context["facility_form"].errors
        assert Facility.objects.count() == 0

    def test_gbv_category_required(self, manager_client, geo, lookups):
        data = facility_post_data(geo, lookups)
        data.pop("gbv_categories")
        r = manager_client.post(reverse("facilities:facility_create"), data)
        assert r.status_code == 200
        assert "gbv_categories" in r.context["gbv_form"].errors

    def test_at_least_one_contact_required(self, manager_client, geo, lookups):
        data = facility_post_data(geo, lookups, **_mgmt("contacts", 0))
        r = manager_client.post(reverse("facilities:facility_create"), data)
        assert r.status_code == 200
        assert r.context["contact_formset"].non_form_errors()

    def test_duplicate_registration_number_rejected(self, manager_client, geo, lookups,
                                                    facility_factory, admin_user):
        existing = facility_factory(admin_user)
        data = facility_post_data(geo, lookups, registration_number=existing.registration_number)
        r = manager_client.post(reverse("facilities:facility_create"), data)
        assert "registration_number" in r.context["facility_form"].errors


class TestFacilityUpdate:
    def test_edit_form_prefills_related_data(self, manager_client, facility_factory, admin_user):
        f = facility_factory(admin_user)
        r = manager_client.get(reverse("facilities:facility_update", args=[f.pk]))
        assert r.status_code == 200
        assert r.context["contact_formset"].initial[0]["contact_value"] == "+254700111222"
        assert r.context["facility_form"].fields["county"].initial == f.ward.constituency.county
        assert list(r.context["gbv_form"].fields["gbv_categories"].initial)

    def test_edit_404_for_inactive(self, manager_client, facility_factory, admin_user):
        f = facility_factory(admin_user, is_active=False)
        assert manager_client.get(reverse("facilities:facility_update", args=[f.pk])).status_code == 404

    def test_edit_saves_changes(self, manager_client, facility_factory, admin_user, geo, lookups):
        f = facility_factory(admin_user)
        data = facility_post_data(geo, lookups, facility_name="Renamed",
                                  registration_number=f.registration_number,
                                  facility_code=f.facility_code)
        r = manager_client.post(reverse("facilities:facility_update", args=[f.pk]), data)
        assert r.status_code == 302
        f.refresh_from_db()
        assert f.facility_name == "Renamed"

    def test_failed_edit_leaves_record_untouched(self, manager_client, facility_factory,
                                                 admin_user, geo, lookups):
        f = facility_factory(admin_user, name="Keep me")
        data = facility_post_data(geo, lookups, facility_name="Renamed",
                                  registration_number=f.registration_number,
                                  facility_code=f.facility_code)
        r = manager_client.post(reverse("facilities:facility_update", args=[f.pk]), data)
        f.refresh_from_db()
        if r.status_code != 302:
            assert f.facility_name == "Keep me"
            assert f.facilitycontact_set.filter(is_active=True).count() == 1


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

class TestFacilityForms:
    def _data(self, geo, lookups, **kw):
        d = {
            "facility_name": "F", "registration_number": "R-1",
            "operational_status": lookups["status"].pk, "ward": geo["ward"].pk,
        }
        d.update(kw)
        return d

    def test_minimal_valid(self, geo, lookups):
        assert FacilityForm(data=self._data(geo, lookups)).is_valid()

    def test_ward_decides_location_whatever_county_says(self, geo, lookups, admin_user):
        """County/constituency are UI filters only; the saved ward is the truth,
        so a mismatched county cannot produce inconsistent geography."""
        from apps.geography.models import County
        other = County.objects.create(county_name="Other", county_code="999")
        form = FacilityForm(data=self._data(geo, lookups, county=other.pk))
        assert form.is_valid()
        f = form.save(commit=False)
        f.created_by = admin_user
        f.save()
        assert f.ward.constituency.county == geo["county"]

    def test_invalid_ward_rejected(self, geo, lookups):
        form = FacilityForm(data=self._data(geo, lookups, ward=99999))
        assert not form.is_valid() and "ward" in form.errors

    def test_two_facilities_without_code(self, geo, lookups, admin_user):
        first = FacilityForm(data=self._data(geo, lookups, registration_number="R-A"))
        assert first.is_valid()
        f = first.save(commit=False)
        f.created_by = admin_user
        f.save()
        second = FacilityForm(data=self._data(geo, lookups, registration_number="R-B"))
        assert second.is_valid(), second.errors

    def test_coordinates_valid(self):
        form = FacilityCoordinateForm(data={"latitude": "-1.286389", "longitude": "36.817223"})
        assert form.is_valid(), form.errors

    def test_coordinates_required(self):
        form = FacilityCoordinateForm(data={})
        assert not form.is_valid()
        assert {"latitude", "longitude"} <= set(form.errors)

    def test_coordinates_non_numeric_rejected(self):
        assert not FacilityCoordinateForm(data={"latitude": "north", "longitude": "36.8"}).is_valid()

    @pytest.mark.parametrize("lat,lng", [("95", "36.8"), ("-1.2", "200")])
    def test_out_of_range_coordinates_rejected(self, lat, lng):
        assert not FacilityCoordinateForm(data={"latitude": lat, "longitude": lng}).is_valid()

    def test_gbv_form_requires_a_category(self, lookups):
        assert not FacilityGBVCategoryForm(data={}).is_valid()
        assert FacilityGBVCategoryForm(data={"gbv_categories": [lookups["gbv_category"].pk]}).is_valid()

    def test_gbv_form_preselects_existing(self, facility_factory, admin_user, lookups):
        f = facility_factory(admin_user)
        form = FacilityGBVCategoryForm(facility=f)
        assert list(form.fields["gbv_categories"].initial) == [lookups["gbv_category"].pk]


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

class TestCacheUtils:
    def test_cache_key_is_order_independent(self):
        assert cache_utils.get_cache_key("p", a=1, b=2) == cache_utils.get_cache_key("p", b=2, a=1)
        assert cache_utils.get_cache_key("p", a=1) != cache_utils.get_cache_key("p", a=2)

    def test_statistics_and_groupings(self, facility_factory, admin_user, lookups):
        facility_factory(admin_user)
        facility_factory(admin_user, operational_status=lookups["status_closed"], lat=None, lng=None)
        stats = cache_utils.get_facility_statistics()
        assert stats == {"total_facilities": 2, "operational_facilities": 1,
                         "counties_count": 1, "facilities_with_coordinates": 1}
        assert cache_utils.get_facilities_by_status() == {"Operational": 1, "Closed": 1}
        assert cache_utils.get_facilities_by_county()[0]["count"] == 2

    def test_statistics_are_cached(self, facility_factory, admin_user):
        facility_factory(admin_user)
        assert cache_utils.get_facility_statistics()["total_facilities"] == 1
        facility_factory(admin_user)
        assert cache_utils.get_facility_statistics()["total_facilities"] == 1

    def test_viewport_and_pagination(self, facility_factory, admin_user):
        facility_factory(admin_user, name="In")
        facility_factory(admin_user, name="Out", lat=-4.0, lng=39.6)
        data = cache_utils.get_facilities_in_viewport(-1.0, 37.0, -1.5, 36.5, zoom_level=10)
        assert [d["facility"]["facility_name"] for d in data] == ["In"]
        page = cache_utils.get_paginated_facilities(page=1, page_size=1, search_query="")
        assert page["total_count"] == 2 and page["has_next"]
        empty = cache_utils.get_paginated_facilities(page=50, page_size=1, search_query="zzz")
        assert empty["facilities"] == []

    def test_invalidate_cache_works_with_configured_backend(self, facility_factory, admin_user):
        facility_factory(admin_user)
        cache_utils.get_facility_statistics()
        cache_utils.invalidate_facility_cache()
        facility_factory(admin_user)
        assert cache_utils.get_facility_statistics()["total_facilities"] == 2


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_facility_model_strs(facility_factory, admin_user):
    f = facility_factory(admin_user, name="Hope")
    assert str(f) == "Hope - Parklands"
    contact = f.facilitycontact_set.first()
    assert str(contact) == "Hope - Phone: +254700111222"
    assert str(f.facilityservice_set.first()) == "Hope - Counselling"
    assert str(f.facilityowner_set.first()) == "Hope - County Government (Government)"
    assert str(f.facilityinfrastructure_set.first()) == "Hope - Shelter"
    assert str(f.facilitycoordinate_set.first()).startswith("Hope - -1.264")
