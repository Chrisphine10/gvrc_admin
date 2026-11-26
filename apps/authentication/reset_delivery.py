"""Delivering a password reset link: by email and by SMS (Bonga).

Every Hodi account has a phone number, while email delivery depends on the
server having a mail account configured (production had none), so the link
also goes by SMS to the account's own phone.

Both are sent off the request thread: if the page waited on the mail server
or the SMS provider only when an account exists, the response time would tell
anyone which addresses belong to Hodi staff.

SMS is limited to one per account per RESET_SMS_INTERVAL, so typing someone's
email into the form again and again cannot flood their phone or run up the
SMS bill.
"""

import logging
import threading

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import close_old_connections
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

RESET_SMS_INTERVAL = 15 * 60  # seconds


def reset_sms_text(reset_url: str, welcome: bool = False) -> str:
    if welcome:
        return (f"Hodi: an account was created for you. Set your password here: {reset_url} "
                "It works once and expires in 3 days.")
    return (f"Hodi: reset your password here: {reset_url} "
            "It works once and expires in 3 days. If you did not ask, ignore this.")


def _send_email(user, reset_url, welcome=False):
    context = {"user": user, "reset_url": reset_url, "site_name": "Hodi Admin"}
    prefix = "accounts/welcome" if welcome else "accounts/password_reset"
    try:
        send_mail(
            render_to_string(f"{prefix}_subject.txt", context).strip(),
            render_to_string(f"{prefix}_email.html", context),
            None,
            [user.email],
        )
    except Exception:
        logger.exception("Could not send the password reset email")


def _send_sms(user, reset_url, welcome=False):
    from apps.sms.services import is_sendable_phone, send_sms

    if not is_sendable_phone(user.phone_number or ""):
        return
    if not cache.add(f"password-reset-sms:{user.pk}", 1, RESET_SMS_INTERVAL):
        logger.info("Password reset SMS for user %s skipped: one was sent recently", user.pk)
        return
    result = send_sms(user.phone_number, reset_sms_text(reset_url, welcome))
    if not result.ok:
        logger.warning("Password reset SMS for user %s not sent: %s", user.pk, result.message)


def deliver_reset_link(user, reset_url, welcome=False):
    def run():
        try:
            close_old_connections()
            _send_email(user, reset_url, welcome)
            _send_sms(user, reset_url, welcome)
        except Exception:  # pragma: no cover - logged, never breaks the page
            logger.exception("Password reset delivery failed")
        finally:
            close_old_connections()

    if not getattr(settings, "SMS_SEND_IN_BACKGROUND", True):
        run()
        return
    threading.Thread(target=run, name="password-reset", daemon=True).start()
