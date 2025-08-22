# -*- encoding: utf-8 -*-
"""
Mobile Session models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from apps.authentication.models import User


class MobileSession(models.Model):
    """Mobile app session tracking model"""
    device_id = models.CharField(max_length=128, primary_key=True, help_text="Device UUID")
    notification_enabled = models.BooleanField(default=True, null=False, help_text="Whether notifications are enabled")
    dark_mode_enabled = models.BooleanField(default=False, null=False, help_text="Whether dark mode is enabled")
    preferred_language = models.CharField(max_length=5, default='en-US', null=False, help_text="Preferred language code")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, help_text="Device latitude")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True, help_text="Device longitude")
    location_updated_at = models.DateTimeField(null=True, blank=True, help_text="When location was last updated")
    location_permission_granted = models.BooleanField(default=False, help_text="Whether location permission is granted")
    is_active = models.BooleanField(default=True, null=False, help_text="Whether the device session is active")
    last_active_at = models.DateTimeField(default=timezone.now, null=False, help_text="Last time device was active")
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"Device {self.device_id} ({'Active' if self.is_active else 'Inactive'})"
    
    def update_location(self, latitude, longitude):
        """Update device location"""
        self.latitude = latitude
        self.longitude = longitude
        self.location_updated_at = timezone.now()
        self.save(update_fields=['latitude', 'longitude', 'location_updated_at', 'updated_at'])
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_active_at = timezone.now()
        self.save(update_fields=['last_active_at', 'updated_at'])
    
    class Meta:
        verbose_name_plural = "Mobile Sessions"
        db_table = 'mobile_device_sessions'
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['last_active_at']),
            models.Index(fields=['location_permission_granted']),
            models.Index(fields=['preferred_language']),
        ]


class MobileAppUsage(models.Model):
    """Mobile app feature usage tracking"""
    usage_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(MobileSession, on_delete=models.CASCADE, db_column='device_id', null=False, to_field='device_id')
    feature_name = models.CharField(max_length=100, null=False, help_text="Name of the feature used")
    feature_category = models.CharField(max_length=50, blank=True, help_text="Category of the feature")
    usage_count = models.IntegerField(default=1, help_text="Number of times feature was used")
    first_used = models.DateTimeField(default=timezone.now, null=False, help_text="First time feature was used")
    last_used = models.DateTimeField(default=timezone.now, null=False, help_text="Last time feature was used")
    additional_data = models.JSONField(default=dict, help_text="Additional usage data")
    created_at = models.DateTimeField(default=timezone.now, null=False)
    
    def __str__(self):
        return f"{self.feature_name} - {self.session.device_id}"
    
    class Meta:
        verbose_name_plural = "Mobile App Usage"
        db_table = 'mobile_device_usage'
        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['feature_name']),
            models.Index(fields=['feature_category']),
            models.Index(fields=['first_used']),
        ]
        unique_together = ['session', 'feature_name']
