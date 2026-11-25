"""
Bulk SMS through the Intelli-Wealth account on Bonga SMS (sender ID
INTELLIWLTH) — the same provider and account IntelliCash uses.

Three tables:

* SmsSettings  — one row: the Bonga credentials and an on/off switch. Values
  saved here win; anything left blank falls back to the BONGA_SMS_* environment
  variables, so the server can be configured either way.
* SmsBroadcast — one bulk message: who it was for, the text, progress counters.
* SmsRecipient — one row per phone number in a broadcast, with the provider's
  answer. A phone appears once per broadcast, so nobody is texted twice.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class SmsSettings(models.Model):
    DEFAULT_ENDPOINT = "http://167.172.14.50:4002/v1/send-sms"

    enabled = models.BooleanField(
        default=True,
        help_text="Switch off to stop all SMS sending immediately (queued messages wait).",
    )
    provider_name = models.CharField(
        max_length=100,
        default="Intelli-Wealth (Bonga SMS)",
        help_text="Shown in the admin so staff know which account is billed.",
    )
    sender_id = models.CharField(
        max_length=20,
        default="INTELLIWLTH",
        blank=True,
        help_text="Sender name recipients see. It is fixed by the Bonga service ID; this is for reference.",
    )
    client_id = models.CharField(max_length=100, blank=True, help_text="Bonga apiClientID")
    api_key = models.CharField(max_length=255, blank=True, help_text="Bonga key")
    api_secret = models.CharField(max_length=255, blank=True, help_text="Bonga secret")
    service_id = models.CharField(max_length=100, blank=True, help_text="Bonga serviceID")
    endpoint = models.URLField(
        max_length=300,
        blank=True,
        help_text="Bonga send-sms URL. Leave blank for the standard endpoint.",
    )
    # Chat alerts. Texts say only that a chat is waiting and where; never what
    # the person wrote, because an SMS can be read on a locked phone.
    notify_assigned_staff = models.BooleanField(
        default=True,
        help_text="Text a staff member when a help chat is assigned to them (to the phone number on their account).",
    )
    notify_new_chats = models.BooleanField(
        default=True,
        help_text="Text the on-call numbers when someone starts a new help chat.",
    )
    notify_urgent_messages = models.BooleanField(
        default=True,
        help_text="Text the on-call numbers when the app marks a message urgent (once per chat).",
    )
    alert_numbers = models.TextField(
        blank=True,
        help_text="On-call numbers for chat alerts, separated by commas or new lines.",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="+",
    )

    class Meta:
        db_table = "sms_settings"
        verbose_name = "SMS settings"
        verbose_name_plural = "SMS settings"

    def __str__(self):
        return self.provider_name

    @classmethod
    def get_solo(cls):
        obj = cls.objects.order_by("pk").first()
        if obj is None:
            obj = cls.objects.create()
        return obj


class SmsBroadcast(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_QUEUED = "queued"
    STATUS_SENDING = "sending"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_QUEUED, "Queued"),
        (STATUS_SENDING, "Sending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    title = models.CharField(max_length=150, help_text="Internal name, not sent.")
    message = models.TextField(help_text="Text sent. {name} is replaced with the recipient's name.")
    audience = models.JSONField(default=dict, blank=True, help_text="Audience choices and filters used.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED, db_index=True)

    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    skipped_count = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="sms_broadcasts",
    )
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sms_broadcasts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def pending_count(self):
        return max(self.total_recipients - self.sent_count - self.failed_count - self.skipped_count, 0)

    @property
    def progress_percent(self):
        if not self.total_recipients:
            return 100
        done = self.total_recipients - self.pending_count
        return int(done * 100 / self.total_recipients)

    def refresh_counts(self, save=True):
        counts = dict(
            self.recipients.values_list("status").annotate(n=models.Count("id"))
        )
        self.total_recipients = sum(counts.values())
        self.sent_count = counts.get(SmsRecipient.STATUS_SENT, 0)
        self.failed_count = counts.get(SmsRecipient.STATUS_FAILED, 0)
        self.skipped_count = counts.get(SmsRecipient.STATUS_SKIPPED, 0)
        if save:
            self.save(update_fields=[
                "total_recipients", "sent_count", "failed_count", "skipped_count",
            ])
        return counts


class SmsRecipient(models.Model):
    STATUS_QUEUED = "queued"
    STATUS_SENDING = "sending"
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"
    STATUS_SKIPPED = "skipped"
    STATUS_CHOICES = [
        (STATUS_QUEUED, "Queued"),
        (STATUS_SENDING, "Sending"),
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
        (STATUS_SKIPPED, "Skipped"),
    ]

    SOURCE_FACILITY = "facility"
    SOURCE_STAFF = "staff"
    SOURCE_CUSTOM = "custom"
    SOURCE_TEST = "test"
    SOURCE_CHOICES = [
        (SOURCE_FACILITY, "Facility contact"),
        (SOURCE_STAFF, "Staff user"),
        (SOURCE_CUSTOM, "Typed number"),
        (SOURCE_TEST, "Test message"),
    ]

    broadcast = models.ForeignKey(SmsBroadcast, on_delete=models.CASCADE, related_name="recipients")
    phone = models.CharField(max_length=20, help_text="Normalised to 2547XXXXXXXX / 2541XXXXXXXX.")
    name = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_CUSTOM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED, db_index=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    provider_reference = models.CharField(max_length=100, blank=True)
    provider_status = models.CharField(max_length=50, blank=True)
    provider_message = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    claimed_at = models.DateTimeField(null=True, blank=True, help_text="When a worker started sending it.")
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sms_recipients"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["broadcast", "phone"], name="sms_recipient_once_per_broadcast"),
        ]
        indexes = [models.Index(fields=["broadcast", "status"])]

    def __str__(self):
        return f"{self.phone} ({self.get_status_display()})"


class SmsNotification(models.Model):
    """One alert text about a chat. One row per (kind, chat, phone), so a
    retry or a second assignment never texts the same person twice."""

    KIND_NEW_CHAT = "new_chat"
    KIND_ASSIGNED = "assigned"
    KIND_URGENT = "urgent"
    KIND_CHOICES = [
        (KIND_NEW_CHAT, "New chat"),
        (KIND_ASSIGNED, "Chat assigned"),
        (KIND_URGENT, "Urgent message"),
    ]
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"
    STATUS_NOT_SENT = "not_sent"
    STATUS_CHOICES = [
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
        (STATUS_NOT_SENT, "Not sent"),
    ]

    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    conversation_id = models.IntegerField(db_index=True)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    provider_status = models.CharField(max_length=50, blank=True)
    provider_message = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "sms_notifications"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["kind", "conversation_id", "phone"], name="sms_notification_once"),
        ]

    def __str__(self):
        return f"{self.get_kind_display()} #{self.conversation_id} -> {self.phone}"
