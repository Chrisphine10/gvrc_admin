"""Chat alerts by SMS through Bonga (the Intelli-Wealth account).

Three alerts, each switchable on the SMS settings page:

* assigned - the staff member a help chat is assigned to (their account phone);
* new_chat - the on-call numbers, when someone starts a help chat;
* urgent   - the on-call numbers, when the app marks a message urgent.

The text names the chat and the page to open, nothing else: an SMS shows on a
locked screen, and the person asking for help may be in danger if what they
wrote is seen.

Sending happens after the database commit, in a background thread, so the
mobile app's request never waits on the SMS provider. Each (kind, chat, phone)
is recorded once, so nobody is texted twice for the same thing.
"""

from __future__ import annotations

import logging
import threading

from django.conf import settings
from django.db import IntegrityError, close_old_connections, transaction

from .models import SmsNotification, SmsSettings
from .services import is_sendable_phone, normalize_phone, send_sms, split_phone_values

logger = logging.getLogger(__name__)


def chat_url(conversation_id: int) -> str:
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    return f"{base}/chat/conversation/{conversation_id}/"


def _messages(kind: str, conversation_id: int) -> str:
    url = chat_url(conversation_id)
    return {
        SmsNotification.KIND_NEW_CHAT: f"Hodi: a new help chat (#{conversation_id}) is waiting. Please respond: {url}",
        SmsNotification.KIND_ASSIGNED: f"Hodi: help chat #{conversation_id} has been assigned to you. Please respond: {url}",
        SmsNotification.KIND_URGENT: f"Hodi: URGENT message in help chat #{conversation_id}. Please respond now: {url}",
    }[kind]


def alert_numbers(sms_settings: SmsSettings) -> list[str]:
    seen, out = set(), []
    for raw in split_phone_values(sms_settings.alert_numbers or ""):
        phone = normalize_phone(raw)
        if is_sendable_phone(phone) and phone not in seen:
            seen.add(phone)
            out.append(phone)
    return out


def _send_once(kind: str, conversation_id: int, phone: str, sms_settings: SmsSettings) -> SmsNotification | None:
    """Claim (kind, chat, phone) by inserting its row first, then send."""
    phone = normalize_phone(phone)
    message = _messages(kind, conversation_id)
    try:
        with transaction.atomic():
            note = SmsNotification.objects.create(
                kind=kind, conversation_id=conversation_id, phone=phone, message=message,
                status=SmsNotification.STATUS_NOT_SENT,
            )
    except IntegrityError:
        return None  # already texted about this
    result = send_sms(phone, message, sms_settings=sms_settings)
    note.status = (
        SmsNotification.STATUS_SENT if result.ok
        else SmsNotification.STATUS_NOT_SENT if result.queued_only
        else SmsNotification.STATUS_FAILED
    )
    note.provider_status = result.status
    note.provider_message = result.message[:500]
    note.save(update_fields=["status", "provider_status", "provider_message"])
    if not result.ok:
        logger.warning("Chat SMS alert %s for chat %s not sent: %s", kind, conversation_id, result.message)
    return note


def send_chat_alert(kind: str, conversation_id: int, user_id: int | None = None) -> list[SmsNotification]:
    """Send one alert now (the background thread and tests call this)."""
    from apps.chat.models import Conversation

    sms_settings = SmsSettings.get_solo()
    if not sms_settings.enabled:
        return []
    conversation = Conversation.objects.select_related("assigned_admin").filter(pk=conversation_id).first()
    if conversation is None:
        return []

    if kind == SmsNotification.KIND_ASSIGNED:
        if not sms_settings.notify_assigned_staff:
            return []
        admin = conversation.assigned_admin
        if admin is None or (user_id and admin.pk != user_id) or not admin.is_active:
            return []
        if not is_sendable_phone(admin.phone_number or ""):
            logger.info("Chat %s assigned to a user with no mobile number; no SMS", conversation_id)
            return []
        phones = [admin.phone_number]
    else:
        wanted = {
            SmsNotification.KIND_NEW_CHAT: sms_settings.notify_new_chats,
            SmsNotification.KIND_URGENT: sms_settings.notify_urgent_messages,
        }[kind]
        if not wanted:
            return []
        phones = alert_numbers(sms_settings)
        # The assigned staff member already gets their own text.
        admin = conversation.assigned_admin
        if kind == SmsNotification.KIND_NEW_CHAT and admin and sms_settings.notify_assigned_staff:
            mine = normalize_phone(admin.phone_number or "")
            phones = [p for p in phones if p != mine]

    sent = []
    for phone in phones:
        note = _send_once(kind, conversation.pk, phone, sms_settings)
        if note:
            sent.append(note)
    return sent


def queue_chat_alert(kind: str, conversation_id: int, user_id: int | None = None) -> None:
    """Send after the current transaction commits, off the request thread."""

    def run():
        try:
            close_old_connections()
            send_chat_alert(kind, conversation_id, user_id)
        except Exception:  # never let an SMS problem break a chat
            logger.exception("Chat SMS alert %s for chat %s failed", kind, conversation_id)
        finally:
            close_old_connections()

    if not getattr(settings, "SMS_SEND_IN_BACKGROUND", True):
        transaction.on_commit(lambda: send_chat_alert(kind, conversation_id, user_id))
        return
    transaction.on_commit(lambda: threading.Thread(target=run, name=f"sms-chat-{conversation_id}", daemon=True).start())
