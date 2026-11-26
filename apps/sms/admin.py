from django.contrib import admin

from .models import SmsBroadcast, SmsNotification, SmsRecipient, SmsSettings


@admin.register(SmsSettings)
class SmsSettingsAdmin(admin.ModelAdmin):
    list_display = ("provider_name", "sender_id", "enabled", "updated_at")
    # Credentials are edited on the dashboard SMS settings page, which never
    # shows them back; keep them out of the Django admin entirely.
    exclude = ("client_id", "api_key", "api_secret", "service_id")
    readonly_fields = ("updated_at", "updated_by")

    def has_add_permission(self, request):
        return not SmsSettings.objects.exists()


class SmsRecipientInline(admin.TabularInline):
    model = SmsRecipient
    extra = 0
    can_delete = False
    fields = ("phone", "name", "source", "status", "provider_status", "provider_message", "sent_at")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SmsBroadcast)
class SmsBroadcastAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "total_recipients", "sent_count", "failed_count", "created_by", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "message")
    readonly_fields = ("total_recipients", "sent_count", "failed_count", "skipped_count",
                       "created_by", "created_at", "started_at", "completed_at", "audience")
    inlines = [SmsRecipientInline]


@admin.register(SmsRecipient)
class SmsRecipientAdmin(admin.ModelAdmin):
    list_display = ("phone", "name", "broadcast", "status", "provider_status", "sent_at")
    list_filter = ("status", "source")
    search_fields = ("phone", "name", "provider_reference")
    readonly_fields = [f.name for f in SmsRecipient._meta.fields]

    def has_add_permission(self, request):
        return False


@admin.register(SmsNotification)
class SmsNotificationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "kind", "conversation_id", "phone", "status", "provider_status")
    list_filter = ("kind", "status")
    readonly_fields = [f.name for f in SmsNotification._meta.fields]

    def has_add_permission(self, request):
        return False
