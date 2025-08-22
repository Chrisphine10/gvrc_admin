# -*- encoding: utf-8 -*-
"""
Admin configuration for analytics models
"""

from django.contrib import admin
from .models import ContactInteraction, AuditTrail


@admin.register(ContactInteraction)
class ContactInteractionAdmin(admin.ModelAdmin):
    """Admin configuration for ContactInteraction model"""
    list_display = ('interaction_id', 'device', 'contact', 'is_helpful', 'created_at')
    list_filter = ('is_helpful', 'created_at')
    search_fields = ('device__device_id', 'contact__contact_value', 'contact__facility__facility_name')
    readonly_fields = ('interaction_id', 'created_at')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'device', 'contact', 'contact__facility'
        )


@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    """Admin configuration for AuditTrail model"""
    list_display = ('audit_id', 'table_name', 'record_id', 'action_type', 'event_category', 'severity_level', 'created_at')
    list_filter = ('action_type', 'event_category', 'severity_level', 'table_name', 'created_at')
    search_fields = ('table_name', 'record_id', 'description', 'session__user__full_name')
    readonly_fields = ('audit_id', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('table_name', 'record_id', 'action_type', 'event_category', 'severity_level')
        }),
        ('Session Information', {
            'fields': ('session', 'ip_address')
        }),
        ('Change Details', {
            'fields': ('old_values', 'new_values', 'changed_fields'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('description', 'justification', 'failure_reason', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session', 'session__user')