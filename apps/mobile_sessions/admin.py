# -*- encoding: utf-8 -*-
"""
Admin interface for Mobile Sessions
"""

from django.contrib import admin
from .models import MobileSession, MobileAppUsage


@admin.register(MobileSession)
class MobileSessionAdmin(admin.ModelAdmin):
    """Admin interface for MobileSession model"""
    list_display = [
        'device_id', 'is_active', 'game_high_score', 'notification_enabled', 'dark_mode_enabled',
        'preferred_language', 'location_permission_granted', 'last_active_at'
    ]
    list_filter = [
        'is_active', 'notification_enabled', 'dark_mode_enabled', 
        'location_permission_granted', 'preferred_language', 'last_active_at'
    ]
    search_fields = [
        'device_id'
    ]
    readonly_fields = [
        'created_at', 'updated_at'
    ]
    fieldsets = (
        ('Device Information', {
            'fields': ('device_id', 'is_active', 'game_high_score', 'last_active_at')
        }),
        ('User Preferences', {
            'fields': ('notification_enabled', 'dark_mode_enabled', 'preferred_language')
        }),
        ('Location Data', {
            'fields': ('latitude', 'longitude', 'location_updated_at', 'location_permission_granted')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(MobileAppUsage)
class MobileAppUsageAdmin(admin.ModelAdmin):
    """Admin interface for MobileAppUsage model"""
    list_display = [
        'usage_id', 'session', 'feature_name', 'feature_category', 
        'usage_count', 'first_used', 'last_used'
    ]
    list_filter = [
        'feature_category', 'first_used', 'last_used'
    ]
    search_fields = [
        'feature_name', 'session__device_id'
    ]
    readonly_fields = [
        'usage_id', 'created_at'
    ]
    fieldsets = (
        ('Usage Information', {
            'fields': ('session', 'feature_name', 'feature_category', 'usage_count')
        }),
        ('Timing', {
            'fields': ('first_used', 'last_used')
        }),
        ('Additional Data', {
            'fields': ('additional_data',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('usage_id', 'created_at'),
            'classes': ('collapse',)
        })
    )
