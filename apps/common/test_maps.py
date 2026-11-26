"""Map provider setting: model logic, admin page, mobile config, map pages."""

import json
from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from apps.common.models import ApplicationSettings

OSM = ApplicationSettings.MAP_PROVIDER_OSM
GOOGLE = ApplicationSettings.MAP_PROVIDER_GOOGLE


@pytest.fixture
def app_settings(db):
    return ApplicationSettings.get_settings()


def _set_provider(provider):
    s = ApplicationSettings.get_settings()
    s.map_provider = provider
    s.save()
    return s


# ------------------------------------------------------------------ model

@override_settings(GOOGLE_MAPS_API_KEY="browser-key")
def test_google_used_when_key_present(app_settings):
    s = _set_provider(GOOGLE)
    assert s.effective_map_provider() == GOOGLE


@override_settings(GOOGLE_MAPS_API_KEY="")
def test_google_without_key_falls_back_to_osm(app_settings):
    s = _set_provider(GOOGLE)
    cfg = s.map_config()
    assert cfg["provider"] == OSM and cfg["selected_provider"] == GOOGLE


def test_map_config_shape(app_settings):
    cfg = _set_provider(OSM).map_config()
    assert cfg["provider"] == OSM
    assert "{z}" in cfg["osm_tile_url"]
    assert cfg["osm_attribution"].startswith("©")
    assert cfg["default_center"] == {"lat": pytest.approx(-1.286389), "lng": pytest.approx(36.817223)}
    assert cfg["default_zoom"] == 7
    assert "google_maps_api_key" not in cfg  # never in the model's public config


def test_restored_settings_fields_exist(app_settings):
    """The fields dropped from the model in July still exist in production's
    table; they are back on the model so inserts and migrations agree."""
    names = {f.name for f in ApplicationSettings._meta.get_fields()}
    for field in ("contact_email", "organization_name", "android_apk", "enable_apk_download", "map_provider"):
        assert field in names
    assert app_settings.has_apk() is False


# --------------------------------------------------------- mobile endpoint

@override_settings(GOOGLE_MAPS_API_KEY="secret-browser-key")
def test_mobile_map_config_is_public_and_has_no_key(client, app_settings):
    _set_provider(GOOGLE)
    resp = client.get("/mobile/config/map/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["provider"] == GOOGLE
    assert set(data) == {"provider", "selected_provider", "osm_tile_url", "osm_attribution",
                         "default_center", "default_zoom"}
    assert b"secret-browser-key" not in resp.content
    assert "max-age" in resp["Cache-Control"]
    assert reverse("mobile:map-config") == "/mobile/config/map/"


def test_mobile_map_config_osm(client, app_settings):
    _set_provider(OSM)
    assert client.get("/mobile/config/map/").json()["provider"] == OSM


def test_mobile_map_config_rejects_writes(client, app_settings):
    assert client.post("/mobile/config/map/", {}).status_code == 405


# ------------------------------------------------------------- admin page

@pytest.fixture
def plain_user(db):
    return get_user_model().objects.create_user(email="plain@x.ke", full_name="Plain",
                                                phone_number="0700000098", password="pass12345")


def test_map_settings_requires_permission(client, plain_user):
    url = reverse("common:map_settings")
    assert client.get(url).status_code == 302
    client.force_login(plain_user)
    resp = client.get(url)
    assert resp.status_code == 302 and resp.url == "/dashboard/"


def test_application_settings_requires_permission(client, plain_user):
    """Any logged-in account could rebrand the whole admin before."""
    client.force_login(plain_user)
    resp = client.post(reverse("common:application_settings"), {"site_name": "Hacked"})
    assert resp.status_code == 302 and resp.url == "/dashboard/"
    assert ApplicationSettings.get_settings().site_name != "Hacked"


def test_map_settings_page_and_save(client, superuser, app_settings):
    client.force_login(superuser)
    url = reverse("common:map_settings")
    page = client.get(url)
    assert page.status_code == 200
    assert b'id="hodi-map-config"' in page.content and b"hodi-map.js" in page.content
    resp = client.post(url, {
        "map_provider": OSM,
        "osm_tile_url": "https://tiles.example.org/{z}/{x}/{y}.png",
        "osm_attribution": "© OSM",
        "map_default_latitude": "0.514277",
        "map_default_longitude": "35.269779",
        "map_default_zoom": "10",
    })
    assert resp.status_code == 302
    s = ApplicationSettings.get_settings()
    assert s.map_provider == OSM and s.map_default_zoom == 10
    assert s.map_default_latitude == Decimal("0.514277")


@pytest.mark.parametrize("field,value,message", [
    ("osm_tile_url", "https://tiles.example.org/tiles.png", b"{z}, {x} and {y}"),
    ("osm_tile_url", "http://tiles.example.org/{z}/{x}/{y}.png", b"https://"),
    ("map_default_latitude", "95", b"between -90 and 90"),
    ("map_default_longitude", "-200", b"between -180 and 180"),
    ("map_default_zoom", "30", b"between 1 and 18"),
])
def test_map_settings_validation(client, superuser, app_settings, field, value, message):
    client.force_login(superuser)
    data = {
        "map_provider": OSM, "osm_tile_url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "osm_attribution": "© OSM", "map_default_latitude": "-1.28", "map_default_longitude": "36.8",
        "map_default_zoom": "7",
    }
    data[field] = value
    resp = client.post(reverse("common:map_settings"), data)
    assert resp.status_code == 200 and message in resp.content


# -------------------------------------------------------------- map pages

def _page_config(resp):
    html = resp.content.decode()
    start = html.index(">", html.index('id="hodi-map-config"')) + 1
    return json.loads(html[start:html.index("</script>", start)])


@override_settings(GOOGLE_MAPS_API_KEY="browser-key")
def test_facility_map_follows_provider(client, superuser, app_settings):
    client.force_login(superuser)
    _set_provider(OSM)
    cfg = _page_config(client.get(reverse("facilities:facility_map")))
    assert cfg["provider"] == OSM and cfg["google_maps_api_key"] == ""
    _set_provider(GOOGLE)
    resp = client.get(reverse("facilities:facility_map"))
    cfg = _page_config(resp)
    assert cfg["provider"] == GOOGLE and cfg["google_maps_api_key"] == "browser-key"
    assert b"maps.googleapis.com/maps/api/js?key=" not in resp.content  # loaded by hodi-map.js only


@pytest.fixture
def mapped_facility(db, ward, operational_status, superuser):
    from apps.facilities.models import Facility, FacilityCoordinate
    f = Facility.objects.create(
        facility_name='Clinic </script><script>alert(1)</script>', registration_number="R1", facility_code="F1",
        operational_status=operational_status, ward=ward, created_by=superuser)
    FacilityCoordinate.objects.create(facility=f, latitude=Decimal("-1.30"), longitude=Decimal("36.80"), collection_date=date.today(),
                                      created_by=superuser)
    return f


def test_facility_map_escapes_names_and_returns_json(client, superuser, mapped_facility):
    client.force_login(superuser)
    resp = client.get(reverse("facilities:facility_map"))
    assert resp.status_code == 200
    assert b"</script><script>alert(1)" not in resp.content  # json_script escapes "<"
    data = client.get(reverse("facilities:facility_map"), {
        "format": "json", "ne_lat": "0", "ne_lng": "38", "sw_lat": "-2", "sw_lng": "35", "zoom": "9"}).json()
    assert data["count"] == 1
    assert data["facilities"][0]["coordinates"] == {"latitude": -1.3, "longitude": 36.8}
    outside = client.get(reverse("facilities:facility_map"), {
        "format": "json", "ne_lat": "5", "ne_lng": "42", "sw_lat": "4", "sw_lng": "41"}).json()
    assert outside["count"] == 0


@pytest.mark.parametrize("params", [{"zoom": "abc"}, {"ne_lat": "x", "ne_lng": "1", "sw_lat": "1", "sw_lng": "1"},
                                    {"zoom": "nan"}, {"ne_lat": "inf", "ne_lng": "1", "sw_lat": "0", "sw_lng": "0"}])
def test_facility_map_bad_params_do_not_crash(client, superuser, mapped_facility, params):
    client.force_login(superuser)
    assert client.get(reverse("facilities:facility_map"), params).status_code == 200


def test_facility_map_query_count_does_not_grow_per_facility(client, superuser, mapped_facility,
                                                             django_assert_max_num_queries, ward,
                                                             operational_status):
    from apps.facilities.models import Facility, FacilityCoordinate
    for i in range(15):
        f = Facility.objects.create(facility_name=f"F{i}", registration_number=f"RR{i}", facility_code=f"FC{i}",
                                    operational_status=operational_status, ward=ward, created_by=superuser)
        FacilityCoordinate.objects.create(facility=f, latitude=Decimal("-1.2"), longitude=Decimal("36.7"), collection_date=date.today(),
                                          created_by=superuser)
    client.force_login(superuser)
    with django_assert_max_num_queries(30):
        data = client.get(reverse("facilities:facility_map"), {"format": "json"}).json()
    assert data["count"] == 16


def test_facility_form_has_location_picker(client, superuser, app_settings):
    client.force_login(superuser)
    resp = client.get(reverse("facilities:facility_create"))
    assert resp.status_code == 200
    assert b"searchAddress()" in resp.content and b'id="placesMap"' in resp.content
    assert b"hodi-map.js" in resp.content


def test_theme_colours_reach_the_page_as_valid_json(client, superuser, app_settings):
    """The base layout used to print the colour dict with |safe (Python quotes),
    so JSON.parse failed in the browser and custom colours never applied."""
    client.force_login(superuser)
    html = client.get(reverse("common:map_settings")).content.decode()
    start = html.index(">", html.index('id="theme-variables"')) + 1
    colours = json.loads(html[start:html.index("</script>", start)])
    assert colours["--primary-color"] == app_settings.primary_color
    assert "json_script" not in html  # template comments must not leak into the page
