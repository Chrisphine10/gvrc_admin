"""
Emergency chat: staff web pages (/chat/), admin API (/chat/admin/... and
/api/chat/admin/...), services and models. Mobile-side chat is in
test_mobile_api.py.
"""

import json

import pytest
from django.test import Client
from rest_framework.test import APIClient

from apps.chat.models import ChatNotification, Conversation, Message
from apps.chat.services import ConversationService, MessageService, NotificationService
from tests.conftest import grant, logged_in_client

pytestmark = pytest.mark.django_db


@pytest.fixture
def counsellor(staff_user):
    grant(staff_user, "view_chat", "change_chat")
    return staff_user


# ---------------------------------------------------------------------------
# Web pages
# ---------------------------------------------------------------------------

class TestWebViews:
    def test_conversation_list_for_staff_with_filters(self, counsellor, world):
        c = logged_in_client(counsellor)
        r = c.get("/chat/")
        assert r.status_code == 200
        assert list(r.context["conversations"]) == [world["conversation"]]
        for params, expected in (({"status": "new"}, 1), ({"status": "closed"}, 0),
                                 ({"priority": "medium"}, 1), ({"admin": "unassigned"}, 0),
                                 ({"admin": world["admin"].pk}, 1), ({"search": "Need"}, 1),
                                 ({"search": "device-test"}, 1), ({"search": "zzz"}, 0)):
            assert len(c.get("/chat/", params).context["conversations"]) == expected, params

    def test_conversation_list_requires_login(self, world):
        r = Client().get("/chat/")
        assert r.status_code in (302, 403)

    def test_transcript_export_requires_login(self, world):
        r = Client().get(f"/chat/conversation/{world['conversation'].pk}/export/")
        assert r.status_code in (302, 403)
        assert b"I need help" not in r.content

    def test_detail_for_staff(self, counsellor, world):
        c = logged_in_client(counsellor)
        r = c.get(f"/chat/conversation/{world['conversation'].pk}/")
        assert r.status_code == 200

    def test_non_staff_redirect_target_exists(self, plain_user, world):
        c = logged_in_client(plain_user)
        r = c.get(f"/chat/conversation/{world['conversation'].pk}/", follow=True)
        assert r.status_code == 200

    def test_non_staff_cannot_open_detail(self, plain_user, world):
        r = logged_in_client(plain_user).get(f"/chat/conversation/{world['conversation'].pk}/")
        assert r.status_code == 302

    def test_assign_to_self_and_other(self, counsellor, world, user_factory):
        c = logged_in_client(counsellor)
        conv = world["conversation"]
        url = f"/chat/conversation/{conv.pk}/assign/"
        assert c.post(url, json.dumps({"admin_id": "self"}),
                      content_type="application/json").json() == {"success": True}
        conv.refresh_from_db()
        assert conv.assigned_admin == counsellor and conv.status == "active"
        other = user_factory(is_staff=True)
        c.post(url, json.dumps({"admin_id": other.pk}), content_type="application/json")
        conv.refresh_from_db()
        assert conv.assigned_admin == other
        assert c.get(url).status_code == 405
        assert c.post(url, "nope", content_type="application/json").status_code == 400

    def test_assign_requires_change_chat(self, staff_user, world):
        c = logged_in_client(staff_user)
        r = c.post(f"/chat/conversation/{world['conversation'].pk}/assign/",
                   json.dumps({"admin_id": "self"}), content_type="application/json")
        assert r.status_code == 302
        world["conversation"].refresh_from_db()
        assert world["conversation"].assigned_admin == world["admin"]

    def test_update_status(self, counsellor, world):
        c = logged_in_client(counsellor)
        url = f"/chat/conversation/{world['conversation'].pk}/status/"
        assert c.patch(url, json.dumps({"status": "resolved"}),
                       content_type="application/json").json() == {"success": True}
        world["conversation"].refresh_from_db()
        assert world["conversation"].status == "resolved"
        assert c.patch(url, json.dumps({"status": "bogus"}),
                       content_type="application/json").status_code == 400
        assert c.post(url).status_code == 405

    def test_exports_for_staff(self, counsellor, world):
        c = logged_in_client(counsellor)
        r = c.get("/chat/export/")
        assert r["Content-Type"] == "text/csv"
        rows = r.content.decode().strip().splitlines()
        assert rows[0].startswith("Conversation ID") and len(rows) == 2
        r = c.get(f"/chat/conversation/{world['conversation'].pk}/export/")
        assert "Hello, I need help" in r.content.decode()

    def test_export_analytics_needs_dates(self, counsellor, world):
        c = logged_in_client(counsellor)
        assert c.get("/chat/analytics/export/").status_code == 400
        r = c.get("/chat/analytics/export/", {"start_date": "2020-01-01", "end_date": "2099-01-01"})
        assert r.status_code == 200

    def test_analytics_page(self, counsellor, world):
        c = logged_in_client(counsellor)
        for params in ({}, {"time_range": "30d"}, {"time_range": "90d"}, {"time_range": "1y"},
                       {"time_range": "weird"}):
            assert c.get("/chat/analytics/", params).status_code == 200

    def test_analytics_custom_date_range(self, counsellor, world):
        c = Client(raise_request_exception=False)
        c.force_login(counsellor)
        r = c.get("/chat/analytics/", {"start_date": "2024-01-01", "end_date": "2024-12-31"})
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# Admin API
# ---------------------------------------------------------------------------

class TestAdminApi:
    def test_staff_can_list_and_read(self, world):
        c = APIClient()
        c.force_login(world["admin"])
        r = c.get("/api/chat/admin/conversations/")
        assert r.status_code == 200
        r = c.get(f"/api/chat/admin/conversations/{world['conversation'].pk}/messages/")
        assert r.status_code == 200
        assert "Hello, I need help" in r.content.decode()
        for path in ("stats/", "analytics/", "list/"):
            assert c.get("/api/chat/admin/conversations/" + path).status_code == 200

    def test_staff_sends_admin_message(self, world):
        c = APIClient()
        c.force_login(world["admin"])
        conv = world["conversation"]
        r = c.post(f"/api/chat/admin/conversations/{conv.pk}/send-message/",
                   {"content": "We are here for you"}, format="json")
        assert r.status_code == 201, r.content
        msg = conv.messages.order_by("-message_id").first()
        assert msg.sender_type == "admin" and msg.sender == world["admin"]
        conv.refresh_from_db()
        assert conv.unread_count_mobile == 1

    def test_mark_read_and_resolve(self, world):
        c = APIClient()
        c.force_login(world["admin"])
        conv = world["conversation"]
        assert c.post(f"/api/chat/admin/conversations/{conv.pk}/messages/read/").status_code == 200
        assert c.post(f"/api/chat/admin/conversations/{conv.pk}/resolve/").status_code == 200
        conv.refresh_from_db()
        assert conv.status == "resolved"

    def test_anonymous_cannot_change_status(self, world):
        conv = world["conversation"]
        r = APIClient().put(f"/api/chat/admin/conversations/{conv.pk}/status/",
                            {"status": "closed"}, format="json")
        assert r.status_code in (401, 403)
        conv.refresh_from_db()
        assert conv.status == "new"

    def test_notifications(self, world):
        c = APIClient()
        c.force_login(world["admin"])
        n = world["notification"]
        assert c.get("/api/chat/admin/notifications/unread/").status_code == 200
        assert c.post(f"/api/chat/admin/notifications/{n.pk}/mark-read/").status_code == 200
        n.refresh_from_db()
        assert n.is_read
        assert c.post("/api/chat/admin/notifications/mark-all-read/").status_code == 200
        assert c.get("/api/chat/admin/notifications/unread-conversations/").status_code == 200


# ---------------------------------------------------------------------------
# Services and models
# ---------------------------------------------------------------------------

class TestServices:
    def test_get_or_create_reuses_open_conversation(self, mobile_session):
        a = ConversationService.get_or_create_conversation(mobile_session, "x")
        b = ConversationService.get_or_create_conversation(mobile_session, "y")
        assert a == b and a.status == "new"
        a.mark_resolved()
        c = ConversationService.get_or_create_conversation(mobile_session)
        assert c != a

    def test_auto_assign_picks_least_busy_staff(self, mobile_session, user_factory):
        busy = user_factory(is_staff=True)
        idle = user_factory(is_staff=True)
        user_factory(is_staff=False)
        from apps.mobile_sessions.models import MobileSession
        for i in range(2):
            s = MobileSession.objects.create(device_id=f"d{i}")
            Conversation.objects.create(mobile_session=s, assigned_admin=busy, status="active")
        conv = Conversation.objects.create(mobile_session=mobile_session)
        assert ConversationService.auto_assign_conversation(conv) == idle
        conv.refresh_from_db()
        assert conv.assigned_admin == idle and conv.status == "active"
        assert ChatNotification.objects.filter(user=idle,
                                               notification_type="conversation_assigned").exists()

    def test_auto_assign_with_no_staff(self, mobile_session):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        assert ConversationService.auto_assign_conversation(conv) is None

    def test_assign_requires_staff(self, mobile_session, plain_user):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        with pytest.raises(ValueError):
            ConversationService.assign_admin_to_conversation(conv, plain_user)

    def test_admin_message_requires_staff(self, mobile_session, plain_user):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        with pytest.raises(ValueError):
            MessageService.create_admin_message(conv, "hi", plain_user)

    def test_message_lifecycle(self, mobile_session, admin_user):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        m = MessageService.create_mobile_message(conv, "help " * 60)
        conv.refresh_from_db()
        assert len(conv.last_message) == 200
        assert conv.unread_count_admin == 1 and conv.unread_count_mobile == 0
        m.mark_delivered()
        assert m.status == "delivered" and m.delivered_at
        m.mark_read()
        assert m.status == "read" and m.read_at
        m.mark_delivered()  # no going back
        assert m.status == "read"
        reply = MessageService.create_admin_message(conv, "ok", admin_user)
        conv.refresh_from_db()
        assert conv.unread_count_mobile == 1 and conv.last_message_by == admin_user
        assert str(reply).startswith(f"Message {reply.pk} - {conv.pk} (admin)")

    def test_notification_service(self, mobile_session, admin_user):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        n = NotificationService.create_notification(
            user=admin_user, notification_type="new_message", conversation=conv,
            title="t", body="b")
        n2 = NotificationService.create_notification(
            user=admin_user, notification_type="urgent_message", conversation=conv,
            title="t2", body="b2")
        assert set(NotificationService.get_unread_notifications(admin_user)) == {n, n2}
        NotificationService.mark_notification_read(n)
        assert list(NotificationService.get_unread_notifications(admin_user)) == [n2]
        NotificationService.mark_all_notifications_read(admin_user)
        assert not NotificationService.get_unread_notifications(admin_user).exists()


class TestModels:
    def test_conversation_str_and_helpers(self, mobile_session, admin_user):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        assert str(conv) == f"Conversation {conv.pk} - device-test-0001 (new)"
        conv.assign_admin(admin_user)
        assert conv.status == "active"
        conv.mark_resolved()
        conv.refresh_from_db()
        assert conv.status == "resolved"

    def test_message_file_helpers(self, mobile_session):
        conv = Conversation.objects.create(mobile_session=mobile_session)
        m = Message.objects.create(conversation=conv, sender_type="mobile", content="x",
                                   metadata={"original_name": "photo.jpg",
                                             "file_size": 2 * 1024 * 1024,
                                             "file_type": "image/jpeg"})
        assert m.get_original_filename() == "photo.jpg"
        assert m.get_file_size_mb() == 2.0
        assert m.get_file_type() == "image/jpeg"
        bare = Message.objects.create(conversation=conv, sender_type="mobile", content="y")
        assert bare.get_original_filename() is None
        assert bare.get_file_size_mb() is None and bare.get_file_type() is None

    def test_notification_str_and_mark_read(self, world):
        n = world["notification"]
        assert str(n) == f"new_message - {world['admin'].username}"
        n.mark_read()
        n.refresh_from_db()
        assert n.is_read
