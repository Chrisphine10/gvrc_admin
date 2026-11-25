"""
Mobile API under /mobile/ (also mounted at /api/mobile/).

The Flutter app first calls POST /mobile/sessions/create/ with a device_id;
every protected endpoint then needs that device_id (query string for GET,
query string or JSON body for POST/PUT). Without it DRF answers 403 with
{"detail": "Authentication credentials were not provided."}.

External services (Gemini for /ai/chat/, Google Directions for
/directions/route/) are mocked; the autouse _no_network fixture in conftest
turns any real HTTP call into a failure.

apps/mobile/views.py and urls.py are being edited (map-config endpoint); this
file only tests the endpoints that already existed.
"""

import json
from unittest import mock

import pytest
from django.test import Client

from apps.analytics.models import ContactInteraction
from apps.chat.models import Conversation, Message
from apps.mobile_sessions.models import MobileSession

pytestmark = pytest.mark.django_db

NOT_AUTH = "Authentication credentials were not provided."
PREFIXES = ["/mobile", "/api/mobile"]


@pytest.fixture
def api():
    return Client()


@pytest.fixture
def device(api):
    """A device session obtained the way the app does it."""
    r = api.post("/mobile/sessions/create/", {"device_id": "flutter-device-1"},
                 content_type="application/json")
    assert r.status_code == 201, r.content
    s = MobileSession.objects.get(device_id="flutter-device-1")
    s.update_location(-1.2650, 36.8040)
    return s.device_id


def get(api, path, device_id=None, **params):
    if device_id:
        params["device_id"] = device_id
    return api.get(path, params)


def post(api, path, body, device_id=None):
    if device_id:
        body = {**body, "device_id": device_id}
    return api.post(path, json.dumps(body), content_type="application/json")


# ---------------------------------------------------------------------------
# Authentication contract
# ---------------------------------------------------------------------------

PROTECTED_GET = [
    "/facilities/list/", "/facilities/map/", "/music/list/", "/documents/list/",
    "/lookups/data/", "/contacts/list/", "/resources/list/", "/directions/route/",
]
PROTECTED_POST = ["/emergency/sos/", "/analytics/contact-interaction/",
                  "/analytics/contact-click/", "/ai/chat/"]


@pytest.mark.parametrize("prefix", PREFIXES)
@pytest.mark.parametrize("path", PROTECTED_GET)
def test_get_without_device_is_403_json(api, prefix, path):
    r = api.get(prefix + path)
    assert r.status_code == 403
    assert r["Content-Type"].startswith("application/json")
    assert r.json() == {"detail": NOT_AUTH}


@pytest.mark.parametrize("prefix", PREFIXES)
@pytest.mark.parametrize("path", PROTECTED_POST)
def test_post_without_device_is_403_json(api, prefix, path):
    r = post(api, prefix + path, {"message": "hi"})
    assert r.status_code == 403
    assert r.json() == {"detail": NOT_AUTH}


@pytest.mark.parametrize("path", PROTECTED_GET)
def test_unknown_or_inactive_device_is_refused(api, path, mobile_session):
    assert get(api, "/mobile" + path, "no-such-device").status_code == 403
    mobile_session.is_active = False
    mobile_session.save()
    assert get(api, "/mobile" + path, mobile_session.device_id).status_code == 403


def test_facility_detail_without_device_is_403(api, world):
    r = api.get(f"/mobile/facilities/{world['facility'].pk}/detail/")
    assert r.status_code == 403
    assert r.json()["detail"] == NOT_AUTH


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

class TestSessions:
    def test_create_then_fetch(self, api):
        r = post(api, "/mobile/sessions/create/", {"device_id": "abc-123",
                                                   "preferred_language": "sw"})
        assert r.status_code == 201
        body = r.json()
        assert body["device_id"] == "abc-123"
        assert body["is_active"] is True
        assert set(body) >= {"notification_enabled", "dark_mode_enabled",
                             "preferred_language", "game_high_score", "last_active_at"}
        r = api.get("/mobile/sessions/", {"device_id": "abc-123"})
        assert r.status_code == 200 and r.json()["device_id"] == "abc-123"

    def test_create_is_idempotent_and_updates_preferences(self, api):
        post(api, "/mobile/sessions/create/", {"device_id": "abc"})
        r = post(api, "/mobile/sessions/create/", {"device_id": "abc", "dark_mode_enabled": True})
        assert r.status_code == 200
        assert MobileSession.objects.filter(device_id="abc").count() == 1
        assert MobileSession.objects.get(device_id="abc").dark_mode_enabled is True

    def test_create_reactivates_ended_session(self, api, mobile_session):
        mobile_session.is_active = False
        mobile_session.save()
        r = post(api, "/mobile/sessions/create/", {"device_id": mobile_session.device_id})
        assert r.status_code == 200
        mobile_session.refresh_from_db()
        assert mobile_session.is_active

    def test_create_requires_device_id(self, api):
        r = post(api, "/mobile/sessions/create/", {})
        assert r.status_code == 400
        assert "device_id" in r.json()

    def test_create_is_post_only(self, api):
        assert api.get("/mobile/sessions/create/").status_code == 405

    def test_create_stores_location(self, api):
        post(api, "/mobile/sessions/create/", {"device_id": "loc-1",
                                               "latitude": "-1.2", "longitude": "36.8"})
        s = MobileSession.objects.get(device_id="loc-1")
        assert s.latitude is not None and s.longitude is not None

    def test_list_without_device_id_is_400(self, api):
        r = api.get("/mobile/sessions/")
        assert r.status_code == 400
        assert r.json()["error"] == "Missing device_id"

    def test_list_unknown_device_is_404(self, api):
        assert api.get("/mobile/sessions/", {"device_id": "ghost"}).status_code == 404

    def test_update(self, api, device):
        r = api.put("/mobile/sessions/update/",
                    json.dumps({"device_id": device, "notification_enabled": False,
                                "game_high_score": 42}),
                    content_type="application/json")
        assert r.status_code == 200
        s = MobileSession.objects.get(device_id=device)
        assert s.notification_enabled is False and s.game_high_score == 42

    def test_update_unknown_device(self, api):
        r = api.put("/mobile/sessions/update/", json.dumps({"device_id": "ghost"}),
                    content_type="application/json")
        assert r.status_code == 400

    def test_update_rejects_negative_score(self, api, device):
        r = api.put("/mobile/sessions/update/",
                    json.dumps({"device_id": device, "game_high_score": -1}),
                    content_type="application/json")
        assert r.status_code == 400

    def test_end_session_then_endpoints_refuse(self, api, device):
        r = post(api, "/mobile/sessions/end/", {"device_id": device})
        assert r.status_code == 200 and r.json()["device_id"] == device
        assert not MobileSession.objects.get(device_id=device).is_active
        assert get(api, "/mobile/facilities/list/", device).status_code == 403
        assert post(api, "/mobile/sessions/end/", {"device_id": device}).status_code == 400

    def test_end_requires_device_id(self, api):
        assert post(api, "/mobile/sessions/end/", {}).status_code == 400


# ---------------------------------------------------------------------------
# Facilities
# ---------------------------------------------------------------------------

class TestFacilities:
    def test_list_shape_and_distance_sort(self, api, device, facility_factory, admin_user):
        near = facility_factory(admin_user, name="Near", lat=-1.2651, lng=36.8041)
        far = facility_factory(admin_user, name="Far", lat=-4.05, lng=39.66)
        facility_factory(admin_user, name="Hidden", is_active=False)
        r = get(api, "/mobile/facilities/list/", device)
        assert r.status_code == 200
        body = r.json()
        assert body["count"] == 2
        ids = [f["facility_id"] for f in body["results"]]
        assert ids == [near.pk, far.pk]

    def test_search(self, api, device, facility_factory, admin_user):
        facility_factory(admin_user, name="Kenyatta Hospital")
        facility_factory(admin_user, name="Mbagathi Clinic")
        body = get(api, "/mobile/facilities/list/", device, search="kenyatta").json()
        assert [f["facility_name"] for f in body["results"]] == ["Kenyatta Hospital"]

    def test_filter_by_county_ward_and_service(self, api, device, facility_factory, admin_user,
                                               geo, lookups):
        f = facility_factory(admin_user)
        for params in ({"county": geo["county"].pk}, {"ward": geo["ward"].pk},
                       {"constituency": geo["constituency"].pk}):
            body = get(api, "/mobile/facilities/list/", device, **params).json()
            assert [x["facility_id"] for x in body["results"]] == [f.pk], params
        body = get(api, "/mobile/facilities/list/", device, county=99999).json()
        assert body["count"] == 0

    def test_pagination_params_are_clamped(self, api, device, facility_factory, admin_user):
        for _ in range(3):
            facility_factory(admin_user, with_related=False)
        body = get(api, "/mobile/facilities/list/", device, page_size=2).json()
        assert len(body["results"]) == 2 and body["next"]
        body = get(api, "/mobile/facilities/list/", device, page="x", page_size="y").json()
        assert body["count"] == 3

    def test_radius_filter(self, api, device, facility_factory, admin_user):
        facility_factory(admin_user, name="Near", lat=-1.2651, lng=36.8041)
        facility_factory(admin_user, name="Far", lat=-4.05, lng=39.66)
        body = get(api, "/mobile/facilities/list/", device, radius_km=10).json()
        assert [f["facility_name"] for f in body["results"]] == ["Near"]

    def test_detail(self, api, device, facility_factory, admin_user):
        f = facility_factory(admin_user, name="Detail Centre")
        r = get(api, f"/mobile/facilities/{f.pk}/detail/", device)
        assert r.status_code == 200
        body = r.json()
        assert body["facility_id"] == f.pk
        assert body["facility_name"] == "Detail Centre"

    def test_detail_404(self, api, device, facility_factory, admin_user):
        f = facility_factory(admin_user, is_active=False)
        assert get(api, f"/mobile/facilities/{f.pk}/detail/", device).status_code == 404
        assert get(api, "/mobile/facilities/99999/detail/", device).status_code == 404

    def test_map(self, api, device, facility_factory, admin_user):
        facility_factory(admin_user, name="On map")
        facility_factory(admin_user, name="No coords", lat=None, lng=None)
        r = get(api, "/mobile/facilities/map/", device)
        assert r.status_code == 200
        assert "On map" in r.content.decode()
        assert "No coords" not in r.content.decode()

    def test_map_viewport(self, api, device, facility_factory, admin_user):
        facility_factory(admin_user, name="Inside")
        facility_factory(admin_user, name="Outside", lat=-4.05, lng=39.66)
        r = get(api, "/mobile/facilities/map/", device, ne_lat=-1.0, ne_lng=37.0,
                sw_lat=-1.5, sw_lng=36.5, zoom=12)
        text = r.content.decode()
        assert "Inside" in text and "Outside" not in text

    def test_api_mobile_mount_behaves_the_same(self, api, device, facility_factory, admin_user):
        facility_factory(admin_user)
        a = get(api, "/mobile/facilities/list/", device).json()
        b = get(api, "/api/mobile/facilities/list/", device).json()
        assert a["count"] == b["count"] == 1


# ---------------------------------------------------------------------------
# Lookups, music, documents, resources, contacts
# ---------------------------------------------------------------------------

def test_lookups_all_and_by_type(api, device, lookups):
    body = get(api, "/mobile/lookups/data/", device).json()
    assert set(body) == {"service_categories", "gbv_categories", "contact_types",
                         "owner_types", "infrastructure_types", "condition_statuses",
                         "document_types"}
    assert body["gbv_categories"][0]["category_name"] == "Physical Violence"
    only = get(api, "/mobile/lookups/data/", device, lookup_type="contact_types").json()
    assert {c["type_name"] for c in only} == {"Phone", "Email"}


def test_music_list(api, device, admin_user):
    from apps.music.models import Music
    Music.objects.create(name="Calm", genre="Ambient", link="https://example.org/a.mp3")
    Music.objects.create(name="Pop", genre="Pop", link="https://example.org/b.mp3")
    Music.objects.create(name="Off", genre="Pop", link="https://example.org/c.mp3", is_active=False)
    body = get(api, "/mobile/music/list/", device).json()
    assert body["count"] == 2
    assert {t["name"] for t in body["results"]} == {"Calm", "Pop"}
    body = get(api, "/mobile/music/list/", device, genre="amb").json()
    assert [t["name"] for t in body["results"]] == ["Calm"]
    body = get(api, "/mobile/music/list/", device, page_size=1).json()
    assert body["total_pages"] == 2 and body["next"]


class TestDocuments:
    def _docs(self, admin_user, lookups):
        from apps.documents.models import Document
        pub = Document.objects.create(title="Public guide", document_type=lookups["doc_type"],
                                      is_public=True, uploaded_by=admin_user, content="x")
        priv = Document.objects.create(title="Internal memo", document_type=lookups["doc_type"],
                                       is_public=False, uploaded_by=admin_user, content="x")
        return pub, priv

    def test_filters(self, api, device, admin_user, lookups):
        pub, priv = self._docs(admin_user, lookups)
        r = get(api, "/mobile/documents/list/", device, is_public="true")
        assert r.status_code == 200
        text = r.content.decode()
        assert "Public guide" in text and "Internal memo" not in text
        text = get(api, "/mobile/documents/list/", device,
                   document_type=lookups["doc_type"].pk).content.decode()
        assert "Public guide" in text

    def test_private_documents_not_served_to_devices(self, api, device, admin_user, lookups):
        self._docs(admin_user, lookups)
        text = get(api, "/mobile/documents/list/", device).content.decode()
        assert "Internal memo" not in text


def test_resources_list(api, device, world):
    r = get(api, "/mobile/resources/list/", device)
    assert r.status_code == 200
    assert "Know your rights" in r.content.decode() or "Calm" in r.content.decode()


def test_contacts_list(api, device, facility_factory, admin_user):
    facility_factory(admin_user, name="Contact Centre")
    r = get(api, "/mobile/contacts/list/", device)
    assert r.status_code == 200
    assert "+254700111222" in r.content.decode()
    r = get(api, "/mobile/contacts/list/", device, contact_type="Email")
    assert "+254700111222" not in r.content.decode()


# ---------------------------------------------------------------------------
# Emergency and analytics
# ---------------------------------------------------------------------------

class TestEmergency:
    def test_sos_returns_location_and_matching_facilities(self, api, device, facility_factory,
                                                         admin_user):
        f = facility_factory(admin_user)  # service category "Medical"
        r = post(api, "/mobile/emergency/sos/", {"emergency_type": "medical"}, device)
        assert r.status_code == 200
        body = r.json()
        assert body["message"] == "Emergency SOS received"
        assert body["location"] == {"latitude": pytest.approx(-1.265), "longitude": pytest.approx(36.804)}
        assert [x["facility_id"] for x in body["facilities_nearby"]] == [f.pk]

    def test_sos_requires_emergency_type(self, api, device):
        r = post(api, "/mobile/emergency/sos/", {}, device)
        assert r.status_code == 400

    def test_sos_without_location(self, api):
        post(api, "/mobile/sessions/create/", {"device_id": "no-gps"})
        r = post(api, "/mobile/emergency/sos/", {"emergency_type": "medical"}, "no-gps")
        assert r.status_code == 400
        assert "location" in r.json()["error"].lower()

    def test_sos_device_id_in_query_string(self, api, device):
        r = api.post(f"/mobile/emergency/sos/?device_id={device}",
                     json.dumps({"emergency_type": "x"}), content_type="application/json")
        assert r.status_code == 200


class TestAnalytics:
    def test_contact_interaction_is_logged(self, api, device, facility_factory, admin_user):
        f = facility_factory(admin_user)
        r = post(api, "/mobile/analytics/contact-interaction/",
                 {"facility_id": f.pk, "contact_type": "phone",
                  "interaction_data": {"is_helpful": True}}, device)
        assert r.status_code == 200, r.content
        ci = ContactInteraction.objects.get(pk=r.json()["interaction_id"])
        assert ci.device.device_id == device
        assert ci.is_helpful is True
        assert ci.contact == f.facilitycontact_set.first()

    @pytest.mark.parametrize("body,code", [
        ({}, 400), ({"facility_id": 99999, "contact_type": "phone"}, 404),
    ])
    def test_contact_interaction_errors(self, api, device, body, code):
        r = post(api, "/mobile/analytics/contact-interaction/", body, device)
        assert r.status_code in (code, 400)
        assert ContactInteraction.objects.count() == 0

    def test_contact_interaction_unknown_type(self, api, device, facility_factory, admin_user):
        f = facility_factory(admin_user)
        r = post(api, "/mobile/analytics/contact-interaction/",
                 {"facility_id": f.pk, "contact_type": "Fax"}, device)
        assert r.status_code == 400

    def test_contact_click(self, api, device, facility_factory, admin_user):
        f = facility_factory(admin_user)
        contact = f.facilitycontact_set.first()
        r = post(api, "/mobile/analytics/contact-click/",
                 {"contact_id": contact.pk, "click_type": "call"}, device)
        assert r.status_code == 200
        assert r.json()["contact_value"] == "+254700111222"
        assert ContactInteraction.objects.get().interaction_type == "call"

    def test_contact_click_errors(self, api, device):
        assert post(api, "/mobile/analytics/contact-click/", {}, device).status_code == 400
        assert post(api, "/mobile/analytics/contact-click/",
                    {"contact_id": 99999}, device).status_code == 404


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class TestChat:
    def test_start_conversation_then_send_and_read(self, api, device, staff_user):
        r = post(api, "/mobile/chat/start/", {"subject": "Help"}, device)
        assert r.status_code == 201, r.content
        conv_id = r.json()["conversation_id"]
        conv = Conversation.objects.get(pk=conv_id)
        # auto-assigned to the only staff account, which makes it active
        assert conv.assigned_admin == staff_user
        assert conv.status == "active"

        again = post(api, "/mobile/chat/start/", {}, device)
        assert again.status_code == 200 and again.json()["conversation_id"] == conv_id

        r = post(api, f"/mobile/chat/{conv_id}/send-message/", {"content": "I am scared"}, device)
        assert r.status_code == 201, r.content
        msg = Message.objects.get(conversation=conv)
        assert msg.sender_type == "mobile" and msg.sender is None
        conv.refresh_from_db()
        assert conv.last_message == "I am scared"
        assert conv.unread_count_admin == 1

        r = get(api, f"/mobile/chat/{conv_id}/detail/", device)
        assert r.status_code == 200
        assert "I am scared" in r.content.decode()

        r = get(api, "/mobile/chat/list/", device)
        assert [c["conversation_id"] for c in r.json()] == [conv_id]

    def test_start_requires_valid_device(self, api):
        assert post(api, "/mobile/chat/start/", {}).status_code == 400
        assert post(api, "/mobile/chat/start/", {"device_id": "ghost"}).status_code == 400

    def test_send_requires_content(self, api, world):
        conv = world["conversation"]
        r = post(api, f"/mobile/chat/{conv.pk}/send-message/", {"content": ""},
                 world["mobile_session"].device_id)
        assert r.status_code == 400

    def test_other_device_cannot_read_or_write_conversation(self, api, world):
        post(api, "/mobile/sessions/create/", {"device_id": "intruder"})
        conv = world["conversation"]
        assert get(api, f"/mobile/chat/{conv.pk}/detail/", "intruder").status_code == 403
        r = post(api, f"/mobile/chat/{conv.pk}/send-message/", {"content": "hi"}, "intruder")
        assert r.status_code == 403
        assert conv.messages.count() == 1

    def test_detail_and_list_need_device(self, api, world):
        conv = world["conversation"]
        assert api.get(f"/mobile/chat/{conv.pk}/detail/").status_code == 400
        assert api.get("/mobile/chat/list/").status_code == 400
        assert api.get("/mobile/chat/list/", {"device_id": "ghost"}).status_code == 400

    def test_unknown_conversation_is_404(self, api, device):
        assert get(api, "/mobile/chat/99999/detail/", device).status_code == 404

    def test_close_conversation(self, api, world):
        conv = world["conversation"]
        r = post(api, f"/mobile/chat/{conv.pk}/close/", {}, world["mobile_session"].device_id)
        assert r.status_code in (200, 201)
        conv.refresh_from_db()
        assert conv.status in ("closed", "resolved")

    def test_update_message_status(self, api, world):
        msg = world["message"]
        r = api.put(f"/mobile/chat/messages/{msg.pk}/status/?device_id={world['mobile_session'].device_id}",
                    json.dumps({"status": "read"}), content_type="application/json")
        assert r.status_code == 200, r.content
        msg.refresh_from_db()
        assert msg.status == "read"

    def test_websocket_info(self, api):
        r = api.get("/mobile/chat/websocket-info/")
        assert r.status_code == 200

    def test_superuser_can_list_all_conversations(self, world):
        c = Client()
        c.force_login(world["admin"])
        r = c.get("/mobile/chat/list/")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_send_message_multipart(self, world):
        c = Client(raise_request_exception=False)
        conv = world["conversation"]
        r = c.post(f"/mobile/chat/{conv.pk}/send-message/?device_id={world['mobile_session'].device_id}",
                   {"content": "with form encoding"})
        assert r.status_code == 201


# ---------------------------------------------------------------------------
# AI and directions proxies (external calls mocked)
# ---------------------------------------------------------------------------

def _resp(status, payload=None, text=""):
    m = mock.Mock()
    m.status_code = status
    m.json.return_value = payload
    m.text = text or json.dumps(payload or {})
    return m


class TestAiProxy:
    def test_requires_message(self, api, device):
        r = post(api, "/mobile/ai/chat/", {"message": "   "}, device)
        assert r.status_code == 400

    def test_no_key_configured_degrades_gracefully(self, api, device, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with mock.patch("apps.mobile.ai_service.requests.post") as p:
            r = post(api, "/mobile/ai/chat/", {"message": "hello"}, device)
        p.assert_not_called()
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is False and "999" in body["reply"]

    def test_success_reply_is_cleaned(self, api, device, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key")
        payload = {"candidates": [{"content": {"parts": [{"text": "**Hello** there\n# Title"}]}}]}
        with mock.patch("apps.mobile.ai_service.requests.post",
                        return_value=_resp(200, payload)) as p:
            r = post(api, "/mobile/ai/chat/", {
                "message": "hi", "history": [{"role": "user", "content": "earlier"}],
                "facility_context": "Parklands GBV Centre, 1 km",
            }, device)
        body = r.json()
        assert body == {"reply": "Hello there\nTitle", "ok": True, "model": body["model"]}
        sent = json.loads(p.call_args.kwargs["data"])
        prompt = sent["contents"][0]["parts"][0]["text"]
        assert "Parklands GBV Centre" in prompt and "User: earlier" in prompt
        # the key never comes back to the client
        assert "test-key" not in r.content.decode()

    def test_falls_back_to_next_model_on_429_then_reports_quota(self, api, device, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key")
        with mock.patch("apps.mobile.ai_service.requests.post",
                        return_value=_resp(429, {}, "quota")) as p:
            body = post(api, "/mobile/ai/chat/", {"message": "hi"}, device).json()
        assert p.call_count >= 2
        assert body["ok"] is False

    def test_network_error_is_not_an_error_screen(self, api, device, monkeypatch):
        import requests
        monkeypatch.setenv("GEMINI_API_KEY", "test-key")
        with mock.patch("apps.mobile.ai_service.requests.post",
                        side_effect=requests.ConnectionError("down")):
            r = post(api, "/mobile/ai/chat/", {"message": "hi"}, device)
        assert r.status_code == 200 and r.json()["ok"] is False

    def test_long_message_is_truncated(self, api, device, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "k")
        payload = {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}
        with mock.patch("apps.mobile.ai_service.requests.post",
                        return_value=_resp(200, payload)) as p:
            post(api, "/mobile/ai/chat/", {"message": "x" * 10000}, device)
        prompt = json.loads(p.call_args.kwargs["data"])["contents"][0]["parts"][0]["text"]
        assert "x" * 4000 in prompt and "x" * 4001 not in prompt

    def test_malformed_history_does_not_500(self, device, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "k")
        c = Client(raise_request_exception=False)
        with mock.patch("apps.mobile.ai_service.requests.post",
                        return_value=_resp(200, {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]})):
            r = post(c, "/mobile/ai/chat/", {"message": "hi", "history": ["hello"]}, device)
        assert r.status_code == 200


class TestDirectionsProxy:
    def test_bad_coordinates_never_reach_google(self, api, device, monkeypatch):
        monkeypatch.setenv("GOOGLE_MAPS_SERVER_KEY", "k")
        with mock.patch("apps.mobile.directions_service.requests.get") as g:
            for o, d in (("", "1,1"), ("abc", "1,1"), ("91,0", "1,1"), ("0,0", "1,1"),
                         ("1,2,3", "1,1")):
                r = get(api, "/mobile/directions/route/", device, origin=o, destination=d)
                assert r.json() == {"ok": False, "reason": "bad_coordinates"}
        g.assert_not_called()

    def test_success(self, api, device, monkeypatch):
        monkeypatch.setenv("GOOGLE_MAPS_SERVER_KEY", "server-key")
        upstream = {"status": "OK", "routes": [{
            "overview_polyline": {"points": "abc123"},
            "legs": [{"distance": {"text": "2.1 km"}, "duration": {"text": "7 mins"}}],
            "secret": "not forwarded",
        }]}
        with mock.patch("apps.mobile.directions_service.requests.get",
                        return_value=_resp(200, upstream)) as g:
            r = get(api, "/mobile/directions/route/", device, origin="-1.26,36.80",
                    destination="-1.30,36.82", mode="WALKING")
        assert r.json() == {"ok": True, "polyline": "abc123",
                            "distance_text": "2.1 km", "duration_text": "7 mins"}
        params = g.call_args.kwargs["params"]
        assert params["mode"] == "walking"
        assert params["origin"] == "-1.260000,36.800000"
        assert "server-key" not in r.content.decode()

    def test_unknown_mode_falls_back_to_driving(self, api, device, monkeypatch):
        monkeypatch.setenv("GOOGLE_MAPS_SERVER_KEY", "k")
        with mock.patch("apps.mobile.directions_service.requests.get",
                        return_value=_resp(200, {"status": "ZERO_RESULTS"})) as g:
            r = get(api, "/mobile/directions/route/", device, origin="1,1",
                    destination="2,2", mode="rocket")
        assert g.call_args.kwargs["params"]["mode"] == "driving"
        assert r.json() == {"ok": False, "reason": "ZERO_RESULTS"}

    @pytest.mark.parametrize("upstream,reason", [
        (_resp(500, {}), "upstream_status"),
        (_resp(200, {"status": "OK", "routes": []}), "unexpected_shape"),
        (_resp(200, {"status": "REQUEST_DENIED"}), "REQUEST_DENIED"),
    ])
    def test_upstream_failures(self, api, device, monkeypatch, upstream, reason):
        monkeypatch.setenv("GOOGLE_MAPS_SERVER_KEY", "k")
        with mock.patch("apps.mobile.directions_service.requests.get", return_value=upstream):
            r = get(api, "/mobile/directions/route/", device, origin="1,1", destination="2,2")
        assert r.status_code == 200
        assert r.json() == {"ok": False, "reason": reason}

    def test_no_key(self, api, device, monkeypatch):
        monkeypatch.delenv("GOOGLE_MAPS_SERVER_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
        r = get(api, "/mobile/directions/route/", device, origin="1,1", destination="2,2")
        assert r.json() == {"ok": False, "reason": "no_api_key"}

    def test_network_error(self, api, device, monkeypatch):
        import requests
        monkeypatch.setenv("GOOGLE_MAPS_SERVER_KEY", "k")
        with mock.patch("apps.mobile.directions_service.requests.get",
                        side_effect=requests.Timeout("slow")):
            r = get(api, "/mobile/directions/route/", device, origin="1,1", destination="2,2")
        assert r.json() == {"ok": False, "reason": "upstream_error"}


# ---------------------------------------------------------------------------
# MobileSession model / service
# ---------------------------------------------------------------------------

def test_mobile_session_model_and_service(db):
    from apps.mobile_sessions.models import MobileAppUsage
    from apps.mobile_sessions.services import MobileSessionService as S
    s = S.create_session("svc-1", location_data={"latitude": -1.1, "longitude": 36.1})
    assert str(s) == "Device svc-1 (Active)"
    assert float(s.latitude) == pytest.approx(-1.1) and s.location_updated_at
    assert S.get_active_session("svc-1") == s
    assert S.update_session_activity("svc-1") == s
    assert s.update_game_score(10) is True
    assert s.update_game_score(5) is False
    s.refresh_from_db()
    assert s.game_high_score == 10
    usage = MobileAppUsage.objects.create(session=s, feature_name="sos")
    assert str(usage) == "sos - svc-1"
    S.end_session(s)
    assert str(s) == "Device svc-1 (Inactive)"
    assert S.get_active_session("svc-1") is None
    assert S.update_session_activity("svc-1") is None
