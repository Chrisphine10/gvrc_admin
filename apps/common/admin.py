# -*- encoding: utf-8 -*-
"""
Admin configuration for common app models
"""

from django.contrib import admin
from .models import ApplicationSettings


@admin.register(ApplicationSettings)
class ApplicationSettingsAdmin(admin.ModelAdmin):
    """Admin configuration for ApplicationSettings"""
    list_display = ['site_name', 'site_tagline', 'primary_color', 'enable_dark_mode', 'default_theme', 'updated_at']
    list_filter = ['enable_dark_mode', 'default_theme', 'created_at', 'updated_at']
    search_fields = ['site_name', 'site_tagline']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Logo Settings', {
            'fields': ('logo', 'logo_alt_text'),
            'classes': ('collapse',)
        }),
        ('Favicon Settings', {
            'fields': ('favicon', 'apple_touch_icon'),
            'classes': ('collapse',)
        }),
        ('Theme Colors', {
            'fields': ('primary_color', 'secondary_color', 'success_color', 'warning_color', 'danger_color', 'info_color', 'dark_color', 'light_color')
        }),
        ('Theme Options', {
            'fields': ('enable_dark_mode', 'default_theme')
        }),
        ('Meta Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow one settings instance"""
        return not ApplicationSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False
# All concrete models are registered in their respective app admin files
