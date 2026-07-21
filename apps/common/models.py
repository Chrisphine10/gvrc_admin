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


# ... existing code ...