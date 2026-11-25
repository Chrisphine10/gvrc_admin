# -*- encoding: utf-8 -*-
"""
Common models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os


def get_upload_path(instance, filename):
    """Generate upload path for settings files"""
    return f'settings/{filename}'


class ApplicationSettings(models.Model):
    """Application-wide settings for logo, favicon, and theme customization"""
    
    # Basic settings
    site_name = models.CharField(
        max_length=100, 
        default="Hodi Admin",
        help_text="Application name displayed in browser title and branding"
    )
    site_tagline = models.CharField(
        max_length=200, 
        default="Multi-Institutional GBV Response Platform",
        help_text="Tagline displayed under the site name"
    )
    
    # Logo settings
    logo = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gif'])],
        help_text="Main application logo (recommended: 200x60px, PNG/SVG)"
    )
    logo_alt_text = models.CharField(
        max_length=100,
        default="Hodi Admin Logo",
        help_text="Alt text for the logo image"
    )
    
    # Favicon settings
    favicon = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['ico', 'png', 'jpg', 'jpeg'])],
        help_text="Favicon for browser tabs (recommended: 32x32px, ICO/PNG)"
    )
    apple_touch_icon = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
        help_text="Apple touch icon for mobile devices (recommended: 180x180px)"
    )
    
    # Theme color settings
    primary_color = models.CharField(
        max_length=7,
        default="#5e72e4",
        help_text="Primary brand color (hex code, e.g., #5e72e4)"
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#8392ab",
        help_text="Secondary brand color (hex code, e.g., #8392ab)"
    )
    success_color = models.CharField(
        max_length=7,
        default="#2dce89",
        help_text="Success/positive action color (hex code, e.g., #2dce89)"
    )
    warning_color = models.CharField(
        max_length=7,
        default="#fb6340",
        help_text="Warning color (hex code, e.g., #fb6340)"
    )
    danger_color = models.CharField(
        max_length=7,
        default="#f5365c",
        help_text="Danger/error color (hex code, e.g., #f5365c)"
    )
    info_color = models.CharField(
        max_length=7,
        default="#11cdef",
        help_text="Info color (hex code, e.g., #11cdef)"
    )
    dark_color = models.CharField(
        max_length=7,
        default="#212529",
        help_text="Dark color for text and backgrounds (hex code, e.g., #212529)"
    )
    light_color = models.CharField(
        max_length=7,
        default="#f8f9fe",
        help_text="Light color for backgrounds (hex code, e.g., #f8f9fe)"
    )
    
    # Additional theme settings
    enable_dark_mode = models.BooleanField(
        default=False,
        help_text="Enable dark mode toggle for users"
    )
    default_theme = models.CharField(
        max_length=10,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('auto', 'Auto (System)')
        ],
        default='light',
        help_text="Default theme for new users"
    )
    
    # Essential Application Settings
    contact_email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Primary contact email address"
    )
    contact_phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Primary contact phone number"
    )
    support_email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Support email address for user inquiries"
    )
    organization_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Organization name"
    )
    organization_address = models.TextField(
        blank=True,
        null=True,
        help_text="Organization physical address"
    )
    
    # Social Media & Links
    website_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Main website URL"
    )
    facebook_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Facebook page URL"
    )
    twitter_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Twitter/X profile URL"
    )
    linkedin_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="LinkedIn profile URL"
    )
    
    # Application Tour Settings
    enable_application_tour = models.BooleanField(
        default=True,
        help_text="Enable the built-in application tour for new users"
    )
    show_tour_on_first_login = models.BooleanField(
        default=True,
        help_text="Automatically show tour on first user login"
    )
    
    # Mobile App Download
    android_apk = models.FileField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        help_text="Android APK file for mobile app download",
        validators=[FileExtensionValidator(allowed_extensions=['apk'])]
    )
    android_apk_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Direct download URL for APK (alternative to file upload)"
    )
    android_apk_version = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="APK version number (e.g., 1.0.0)"
    )
    android_apk_size = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="APK file size (e.g., 25.5 MB)"
    )
    enable_apk_download = models.BooleanField(
        default=True,
        help_text="Show APK download button on landing page"
    )
    
    # Maps
    MAP_PROVIDER_GOOGLE = 'google'
    MAP_PROVIDER_OSM = 'openstreetmap'
    MAP_PROVIDER_CHOICES = [
        (MAP_PROVIDER_OSM, 'OpenStreetMap (free, no API key)'),
        (MAP_PROVIDER_GOOGLE, 'Google Maps (needs an API key)'),
    ]
    map_provider = models.CharField(
        max_length=20,
        choices=MAP_PROVIDER_CHOICES,
        default=MAP_PROVIDER_GOOGLE,
        help_text="Map used on the admin facility maps and location pickers, "
                  "and offered to the mobile app. OpenStreetMap needs no API key."
    )
    osm_tile_url = models.CharField(
        max_length=300,
        default='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        help_text="Tile server for OpenStreetMap. Keep the default unless you run your own tiles."
    )
    osm_attribution = models.CharField(
        max_length=300,
        default='© OpenStreetMap contributors',
        help_text="Credit line shown on OpenStreetMap maps (required by the tile licence)."
    )
    map_default_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=-1.286389,
        help_text="Where maps open when there is nothing to show (default: Nairobi)."
    )
    map_default_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=36.817223,
        help_text="Where maps open when there is nothing to show (default: Nairobi)."
    )
    map_default_zoom = models.PositiveSmallIntegerField(
        default=7,
        help_text="Zoom level maps open at (1 = world, 18 = street)."
    )

    # Meta information
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'application_settings'
        verbose_name = 'Application Settings'
        verbose_name_plural = 'Application Settings'
    
    def __str__(self):
        return f"Application Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and ApplicationSettings.objects.exists():
            # If this is a new instance and one already exists, update the existing one
            existing = ApplicationSettings.objects.first()
            for field in self._meta.fields:
                if field.name not in ['id', 'created_at', 'updated_at']:
                    setattr(existing, field.name, getattr(self, field.name))
            existing.save()
            return existing
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the current application settings, creating default if none exist"""
        settings, created = cls.objects.get_or_create(
            defaults={
                'site_name': 'Hodi Admin',
                'site_tagline': 'Multi-Institutional GBV Response Platform',
                'primary_color': '#5e72e4',
                'secondary_color': '#8392ab',
                'success_color': '#2dce89',
                'warning_color': '#fb6340',
                'danger_color': '#f5365c',
                'info_color': '#11cdef',
                'dark_color': '#212529',
                'light_color': '#f8f9fe',
            }
        )
        return settings
    
    def get_theme_css_variables(self):
        """Generate CSS custom properties for theme colors"""
        return {
            '--primary-color': self.primary_color,
            '--secondary-color': self.secondary_color,
            '--success-color': self.success_color,
            '--warning-color': self.warning_color,
            '--danger-color': self.danger_color,
            '--info-color': self.info_color,
            '--dark-color': self.dark_color,
            '--light-color': self.light_color,
        }
    
    def get_logo_url(self):
        """Get logo URL or return default"""
        if self.logo:
            return self.logo.url
        return '/static/assets/img/brand/hodi app logo.png'
    
    def get_favicon_url(self):
        """Get favicon URL or return default"""
        if self.favicon:
            return self.favicon.url
        return '/static/assets/img/icons/common/favicon.ico'
    
    def get_apple_touch_icon_url(self):
        """Get apple touch icon URL or return default"""
        if self.apple_touch_icon:
            return self.apple_touch_icon.url
        return '/static/assets/img/icons/common/favicon.ico'

    def get_apk_url(self):
        """Get Android APK URL - prefer uploaded file, fallback to manual URL"""
        if self.android_apk:
            return self.android_apk.url
        if self.android_apk_url:
            return self.android_apk_url
        return None

    def has_apk(self):
        """Check if APK file or URL is available"""
        return bool((self.android_apk or self.android_apk_url) and self.enable_apk_download)

    def effective_map_provider(self):
        """The provider pages should actually use.

        Google Maps without a key shows a grey "for development purposes only"
        map, so with no key configured the admin falls back to OpenStreetMap
        instead of showing a broken map.
        """
        from django.conf import settings as dj_settings
        if self.map_provider == self.MAP_PROVIDER_GOOGLE and not getattr(dj_settings, 'GOOGLE_MAPS_API_KEY', ''):
            return self.MAP_PROVIDER_OSM
        return self.map_provider

    def map_config(self):
        """Map settings for templates and the mobile app (no secrets)."""
        return {
            'provider': self.effective_map_provider(),
            'selected_provider': self.map_provider,
            'osm_tile_url': self.osm_tile_url,
            'osm_attribution': self.osm_attribution,
            'default_center': {
                'lat': float(self.map_default_latitude),
                'lng': float(self.map_default_longitude),
            },
            'default_zoom': self.map_default_zoom,
        }
