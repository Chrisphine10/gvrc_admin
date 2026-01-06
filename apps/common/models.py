# -*- encoding: utf-8 -*-
"""
Common models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile
from PIL import Image
import os
import io


def get_upload_path(instance, filename):
    """Generate upload path for settings files"""
    return f'settings/{filename}'


def resize_image(image_file, target_size, quality=95):
    """
    Resize an image to target size with high quality.
    Uses LANCZOS resampling for best quality (works for both upscaling and downscaling).
    
    Args:
        image_file: File-like object or file path
        target_size: Tuple of (width, height) in pixels
        quality: JPEG quality (1-100), only used for JPEG files
    
    Returns:
        Resized image as ContentFile or None if error
    """
    if not image_file:
        return None
    
    try:
        # Open the image (works with file objects and paths)
        img = Image.open(image_file)
        
        # Get original format
        original_format = img.format
        
        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        # Keep transparency for PNG
        if img.mode in ('RGBA', 'LA', 'P') and original_format != 'PNG':
            # Create a white background for formats that don't support transparency
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        elif img.mode not in ('RGB', 'RGBA'):
            # Convert to RGB for non-transparent formats
            if original_format == 'PNG':
                # Keep RGBA for PNG to preserve transparency
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
        
        # Resize using LANCZOS resampling (highest quality)
        # LANCZOS works well for both upscaling and downscaling
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Save to BytesIO buffer
        buffer = io.BytesIO()
        
        # Determine format - prefer PNG for favicons and apple touch icons
        # PNG preserves transparency and works universally
        if original_format == 'PNG' or img.mode == 'RGBA':
            resized_img.save(buffer, format='PNG', optimize=True)
            ext = '.png'
        elif original_format in ('JPEG', 'JPG'):
            resized_img.save(buffer, format='JPEG', quality=quality, optimize=True)
            ext = '.jpg'
        elif original_format == 'ICO':
            # For ICO files, save as PNG (browsers accept PNG for favicon)
            resized_img.save(buffer, format='PNG', optimize=True)
            ext = '.png'
        else:
            # Default to PNG for best quality and compatibility
            resized_img.save(buffer, format='PNG', optimize=True)
            ext = '.png'
        
        buffer.seek(0)
        
        # Generate new filename
        if hasattr(image_file, 'name'):
            base_name = os.path.splitext(os.path.basename(image_file.name))[0]
        else:
            base_name = 'resized_image'
        new_filename = f"{base_name}_{target_size[0]}x{target_size[1]}{ext}"
        
        return ContentFile(buffer.read(), name=new_filename)
        
    except Exception as e:
        # Log error but don't break the save process
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error resizing image: {str(e)}")
        return None


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
        
        # Store old file paths before saving
        old_favicon_path = None
        old_apple_icon_path = None
        if self.pk:
            try:
                old_instance = ApplicationSettings.objects.get(pk=self.pk)
                if old_instance.favicon:
                    old_favicon_path = old_instance.favicon.path if hasattr(old_instance.favicon, 'path') else None
                if old_instance.apple_touch_icon:
                    old_apple_icon_path = old_instance.apple_touch_icon.path if hasattr(old_instance.apple_touch_icon, 'path') else None
            except ApplicationSettings.DoesNotExist:
                pass
        
        # Auto-resize favicon before saving (32x32px)
        if self.favicon:
            # Check if this is a new file upload (file object exists)
            if hasattr(self.favicon, 'read'):
                resized_favicon = resize_image(self.favicon, (32, 32), quality=95)
                if resized_favicon:
                    # Save the resized image
                    self.favicon.save(
                        resized_favicon.name,
                        resized_favicon,
                        save=False
                    )
                    # Delete old file if it exists and is different
                    if old_favicon_path and os.path.exists(old_favicon_path):
                        try:
                            os.remove(old_favicon_path)
                        except Exception:
                            pass
        
        # Auto-resize apple touch icon before saving (180x180px)
        if self.apple_touch_icon:
            # Check if this is a new file upload (file object exists)
            if hasattr(self.apple_touch_icon, 'read'):
                resized_apple_icon = resize_image(self.apple_touch_icon, (180, 180), quality=95)
                if resized_apple_icon:
                    # Save the resized image
                    self.apple_touch_icon.save(
                        resized_apple_icon.name,
                        resized_apple_icon,
                        save=False
                    )
                    # Delete old file if it exists and is different
                    if old_apple_icon_path and os.path.exists(old_apple_icon_path):
                        try:
                            os.remove(old_apple_icon_path)
                        except Exception:
                            pass
        
        # For APK files, save directly without processing (they're already binary)
        # Only process images (favicon, apple_touch_icon)
        # APK files don't need resizing, so save them as-is
        
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


# ... existing code ...