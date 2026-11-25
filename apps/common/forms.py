# -*- encoding: utf-8 -*-
"""
Forms for common app
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import ApplicationSettings
import re


class ApplicationSettingsForm(forms.ModelForm):
    """Form for managing application settings"""
    
    class Meta:
        model = ApplicationSettings
        fields = [
            'site_name', 'site_tagline', 'logo', 'logo_alt_text',
            'favicon', 'apple_touch_icon', 'primary_color', 'secondary_color',
            'success_color', 'warning_color', 'danger_color', 'info_color',
            'dark_color', 'light_color', 'enable_dark_mode', 'default_theme'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter application name'
            }),
            'site_tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter application tagline'
            }),
            'logo_alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter alt text for logo'
            }),
            'primary_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#5e72e4'
            }),
            'secondary_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#8392ab'
            }),
            'success_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#2dce89'
            }),
            'warning_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#fb6340'
            }),
            'danger_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#f5365c'
            }),
            'info_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#11cdef'
            }),
            'dark_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#212529'
            }),
            'light_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color',
                'placeholder': '#f8f9fe'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png,image/jpeg,image/jpg,image/svg+xml,image/gif'
            }),
            'favicon': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/x-icon,image/png,image/jpeg,image/jpg'
            }),
            'apple_touch_icon': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png,image/jpeg,image/jpg'
            }),
            'enable_dark_mode': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'default_theme': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def clean_primary_color(self):
        """Validate primary color format"""
        color = self.cleaned_data.get('primary_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #5e72e4)')
        return color
    
    def clean_secondary_color(self):
        """Validate secondary color format"""
        color = self.cleaned_data.get('secondary_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #8392ab)')
        return color
    
    def clean_success_color(self):
        """Validate success color format"""
        color = self.cleaned_data.get('success_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #2dce89)')
        return color
    
    def clean_warning_color(self):
        """Validate warning color format"""
        color = self.cleaned_data.get('warning_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #fb6340)')
        return color
    
    def clean_danger_color(self):
        """Validate danger color format"""
        color = self.cleaned_data.get('danger_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #f5365c)')
        return color
    
    def clean_info_color(self):
        """Validate info color format"""
        color = self.cleaned_data.get('info_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #11cdef)')
        return color
    
    def clean_dark_color(self):
        """Validate dark color format"""
        color = self.cleaned_data.get('dark_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #212529)')
        return color
    
    def clean_light_color(self):
        """Validate light color format"""
        color = self.cleaned_data.get('light_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #f8f9fe)')
        return color
    
    def _is_valid_hex_color(self, color):
        """Check if color is a valid hex color code"""
        if not color:
            return True
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, color))
    
    def clean_logo(self):
        """Validate logo file"""
        logo = self.cleaned_data.get('logo')
        if logo:
            # Check file size (max 5MB)
            if logo.size > 5 * 1024 * 1024:
                raise ValidationError('Logo file size must be less than 5MB')
            
            # Check file extension
            allowed_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.gif']
            if not any(logo.name.lower().endswith(ext) for ext in allowed_extensions):
                raise ValidationError('Logo must be a PNG, JPG, JPEG, SVG, or GIF file')
        
        return logo
    
    def clean_favicon(self):
        """Validate favicon file"""
        favicon = self.cleaned_data.get('favicon')
        if favicon:
            # Check file size (max 1MB)
            if favicon.size > 1 * 1024 * 1024:
                raise ValidationError('Favicon file size must be less than 1MB')
            
            # Check file extension
            allowed_extensions = ['.ico', '.png', '.jpg', '.jpeg']
            if not any(favicon.name.lower().endswith(ext) for ext in allowed_extensions):
                raise ValidationError('Favicon must be an ICO, PNG, JPG, or JPEG file')
        
        return favicon
    
    def clean_apple_touch_icon(self):
        """Validate apple touch icon file"""
        apple_touch_icon = self.cleaned_data.get('apple_touch_icon')
        if apple_touch_icon:
            # Check file size (max 2MB)
            if apple_touch_icon.size > 2 * 1024 * 1024:
                raise ValidationError('Apple touch icon file size must be less than 2MB')
            
            # Check file extension
            allowed_extensions = ['.png', '.jpg', '.jpeg']
            if not any(apple_touch_icon.name.lower().endswith(ext) for ext in allowed_extensions):
                raise ValidationError('Apple touch icon must be a PNG, JPG, or JPEG file')
        
        return apple_touch_icon


class ThemePreviewForm(forms.Form):
    """Form for theme color preview without saving"""
    
    primary_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#5e72e4'
        })
    )
    secondary_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#8392ab'
        })
    )
    success_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#2dce89'
        })
    )
    warning_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#fb6340'
        })
    )
    danger_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#f5365c'
        })
    )
    info_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#11cdef'
        })
    )
    dark_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#212529'
        })
    )
    light_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control color-picker',
            'type': 'color',
            'placeholder': '#f8f9fe'
        })
    )
    
    def clean_primary_color(self):
        """Validate primary color format"""
        color = self.cleaned_data.get('primary_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #5e72e4)')
        return color
    
    def clean_secondary_color(self):
        """Validate secondary color format"""
        color = self.cleaned_data.get('secondary_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #8392ab)')
        return color
    
    def clean_success_color(self):
        """Validate success color format"""
        color = self.cleaned_data.get('success_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #2dce89)')
        return color
    
    def clean_warning_color(self):
        """Validate warning color format"""
        color = self.cleaned_data.get('warning_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #fb6340)')
        return color
    
    def clean_danger_color(self):
        """Validate danger color format"""
        color = self.cleaned_data.get('danger_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #f5365c)')
        return color
    
    def clean_info_color(self):
        """Validate info color format"""
        color = self.cleaned_data.get('info_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #11cdef)')
        return color
    
    def clean_dark_color(self):
        """Validate dark color format"""
        color = self.cleaned_data.get('dark_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #212529)')
        return color
    
    def clean_light_color(self):
        """Validate light color format"""
        color = self.cleaned_data.get('light_color')
        if color and not self._is_valid_hex_color(color):
            raise ValidationError('Please enter a valid hex color code (e.g., #f8f9fe)')
        return color
    
    def _is_valid_hex_color(self, color):
        """Check if color is a valid hex color code"""
        if not color:
            return True
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, color))


class MapSettingsForm(forms.ModelForm):
    """Which map the admin and the mobile app use."""

    class Meta:
        model = ApplicationSettings
        fields = [
            'map_provider', 'osm_tile_url', 'osm_attribution',
            'map_default_latitude', 'map_default_longitude', 'map_default_zoom',
        ]
        widgets = {
            'map_provider': forms.RadioSelect,
            'osm_tile_url': forms.URLInput(attrs={'class': 'form-control'}),
            'osm_attribution': forms.TextInput(attrs={'class': 'form-control'}),
            'map_default_latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'map_default_longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'map_default_zoom': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 18}),
        }

    def clean_osm_tile_url(self):
        url = (self.cleaned_data.get('osm_tile_url') or '').strip()
        if not all(token in url for token in ('{z}', '{x}', '{y}')):
            raise ValidationError('The tile URL must contain {z}, {x} and {y}.')
        if not url.startswith('https://'):
            raise ValidationError('Use an https:// tile server, or browsers will block the map on the live site.')
        return url

    def clean_map_default_latitude(self):
        value = self.cleaned_data.get('map_default_latitude')
        if value is not None and not (-90 <= value <= 90):
            raise ValidationError('Latitude must be between -90 and 90.')
        return value

    def clean_map_default_longitude(self):
        value = self.cleaned_data.get('map_default_longitude')
        if value is not None and not (-180 <= value <= 180):
            raise ValidationError('Longitude must be between -180 and 180.')
        return value

    def clean_map_default_zoom(self):
        value = self.cleaned_data.get('map_default_zoom')
        if value is not None and not (1 <= value <= 18):
            raise ValidationError('Zoom must be between 1 and 18.')
        return value
