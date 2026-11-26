"""Errors: JSON for the app and API, branded pages for browsers, and no
exception text ever reaching a client."""

import json

import pytest
from django.test import Client, RequestFactory
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from core import errors

pytestmark = pytest.mark.django_db

SECRET = "sqlite3.OperationalError: no such table secret_internal_table"


class Boom(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        raise RuntimeError(SECRET)


class NotFoundView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        from rest_framework.exceptions import NotFound
        raise NotFound("No such facility.")


def test_unhandled_api_error_is_json_500_without_details():
    resp = Boom.as_view()(APIRequestFactory().get("/api/boom/"))
    assert resp.status_code == 500
    assert resp.data == {"error": errors.SERVER_ERROR_MESSAGE}
    assert SECRET not in json.dumps(resp.data)


def test_known_api_error_keeps_detail_and_adds_error():
    resp = NotFoundView.as_view()(APIRequestFactory().get("/api/x/"))
    assert resp.status_code == 404
    assert resp.data["detail"] == "No such facility." and resp.data["error"] == "No such facility."


def test_validation_error_list_becomes_error_string():
    from rest_framework.exceptions import ValidationError
    resp = errors.api_exception_handler(ValidationError(["Bad phone number."]), {"view": None})
    assert resp.status_code == 400
    assert resp.data["error"] == "Bad phone number." and resp.data["detail"] == ["Bad phone number."]


def test_mobile_404_is_json():
    r = Client().get("/mobile/this-does-not-exist/")
    assert r.status_code == 404
    assert r["Content-Type"].startswith("application/json")
    assert r.json() == {"error": "Not found."}


def test_browser_404_is_branded_page():
    r = Client().get("/no-such-page-anywhere/")
    assert r.status_code == 404
    assert r["Content-Type"].startswith("text/html")
    assert b"404" in r.content


def test_json_accept_header_gets_json_404():
    r = Client().get("/no-such-page-anywhere/", HTTP_ACCEPT="application/json")
    assert r.status_code == 404 and r.json()["error"] == "Not found."


@pytest.mark.parametrize("path,is_json", [("/mobile/chat/start/", True), ("/api/facilities/", True), ("/dashboard/", False)])
def test_server_error_handler(path, is_json):
    resp = errors.server_error(RequestFactory().get(path))
    assert resp.status_code == 500
    if is_json:
        assert json.loads(resp.content) == {"error": errors.SERVER_ERROR_MESSAGE}
    else:
        assert resp["Content-Type"].startswith("text/html") and b"500" in resp.content


def test_server_error_page_survives_a_broken_template(monkeypatch):
    def broken(name):
        raise RuntimeError("template engine down")
    monkeypatch.setattr("django.template.loader.get_template", broken)
    resp = errors.server_error(RequestFactory().get("/dashboard/"))
    assert resp.status_code == 500 and b"Server error" in resp.content


def test_permission_denied_handler_json_and_html():
    assert errors.permission_denied(RequestFactory().get("/mobile/x/")).status_code == 403
    resp = errors.permission_denied(RequestFactory().get("/dashboard/"))
    assert resp.status_code == 403


def test_mobile_chat_failure_hides_exception_text(monkeypatch):
    from apps.chat.services import ConversationService

    api = Client()
    r = api.post("/mobile/sessions/create/", {"device_id": "err-device"}, content_type="application/json")
    assert r.status_code == 201

    def explode(*a, **k):
        raise RuntimeError(SECRET)
    monkeypatch.setattr(ConversationService, "get_or_create_conversation", staticmethod(explode))
    r = api.post("/mobile/chat/start/", json.dumps({"device_id": "err-device"}), content_type="application/json")
    assert r.status_code == 500
    body = r.content.decode()
    assert SECRET not in body and "Could not create conversation" in body


def test_unauthenticated_mobile_call_has_error_key():
    r = Client().get("/mobile/facilities/list/")
    assert r.status_code in (400, 401, 403)
    assert "error" in r.json()
