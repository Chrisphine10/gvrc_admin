# -*- encoding: utf-8 -*-
"""
Admin configuration for common app models
"""

from django.contrib import admin
from .models import ApplicationSettings


@admin.register(ApplicationSettings)
class ApplicationSettingsAdmin(admin.ModelAdmin):
    """Admin configuration for ApplicationSettings"""
    list_display = ['site_name', 'site_tagline', 'primary_color', 'enable_dark_mode', 'default_theme', 'enable_apk_download', 'updated_at']
    list_filter = ['enable_dark_mode', 'default_theme', 'enable_apk_download', 'created_at', 'updated_at']
    search_fields = ['site_name', 'site_tagline']
    readonly_fields = ['created_at', 'updated_at', 'logo_preview', 'favicon_preview', 'apple_touch_icon_preview', 'apk_info']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'organization_name', 'organization_address')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'support_email')
        }),
        ('Social Media & Links', {
            'fields': ('website_url', 'facebook_url', 'twitter_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Logo Settings', {
            'fields': ('logo', 'logo_preview', 'logo_alt_text'),
            'description': 'Upload your main application logo. Recommended size: 200x60px. Supported formats: PNG, JPG, JPEG, SVG, GIF (max 5MB)'
        }),
        ('Favicon Settings', {
            'fields': ('favicon', 'favicon_preview', 'apple_touch_icon', 'apple_touch_icon_preview'),
            'description': 'Upload favicon for browser tabs (32x32px) and Apple touch icon for mobile devices (180x180px)'
        }),
        ('Theme Colors', {
            'fields': ('primary_color', 'secondary_color', 'success_color', 'warning_color', 'danger_color', 'info_color', 'dark_color', 'light_color'),
            'description': 'Customize your application color scheme using hex color codes (e.g., #5e72e4)'
        }),
        ('Theme Options', {
            'fields': ('enable_dark_mode', 'default_theme')
        }),
        ('Application Tour', {
            'fields': ('enable_application_tour', 'show_tour_on_first_login'),
            'description': 'Configure the built-in application tour feature'
        }),
        ('Mobile App (APK)', {
            'fields': ('android_apk_url', 'android_apk', 'apk_info', 'android_apk_version', 'android_apk_size', 'enable_apk_download'),
            'description': 'Upload Android APK file OR provide a direct download URL. The APK will be available for download on the landing page when enabled. You can use either method - URL is faster for large files.'
        }),
        ('Meta Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        """Display logo preview in admin"""
        if obj.logo:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 60px; max-width: 200px;" />', obj.logo.url)
        return 'No logo uploaded'
    logo_preview.short_description = 'Logo Preview'
    
    def favicon_preview(self, obj):
        """Display favicon preview in admin"""
        if obj.favicon:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 32px; max-width: 32px;" />', obj.favicon.url)
        return 'No favicon uploaded'
    favicon_preview.short_description = 'Favicon Preview'
    
    def apple_touch_icon_preview(self, obj):
        """Display apple touch icon preview in admin"""
        if obj.apple_touch_icon:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 180px; max-width: 180px;" />', obj.apple_touch_icon.url)
        return 'No Apple touch icon uploaded'
    apple_touch_icon_preview.short_description = 'Apple Touch Icon Preview'
    
    def apk_info(self, obj):
        """Display APK file information"""
        if obj.android_apk:
            from django.utils.html import format_html
            apk_url = obj.get_apk_url()
            file_size = obj.android_apk.size if hasattr(obj.android_apk, 'size') else 'Unknown'
            size_mb = round(file_size / (1024 * 1024), 2) if isinstance(file_size, (int, float)) else 'Unknown'
            version = obj.android_apk_version or 'Not specified'
            return format_html(
                '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">'
                '<p><strong>APK File:</strong> <a href="{}" target="_blank">{}</a></p>'
                '<p><strong>Version:</strong> {}</p>'
                '<p><strong>File Size:</strong> {} MB</p>'
                '<p><strong>Status:</strong> {}</p>'
                '</div>',
                apk_url,
                obj.android_apk.name if hasattr(obj.android_apk, 'name') else 'Download',
                version,
                size_mb,
                'Enabled' if obj.enable_apk_download else 'Disabled'
            )
        return 'No APK file uploaded'
    apk_info.short_description = 'APK Information'
    
    def has_add_permission(self, request):
        """Only allow one settings instance"""
        return not ApplicationSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False
# All concrete models are registered in their respective app admin files
