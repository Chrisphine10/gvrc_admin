# -*- encoding: utf-8 -*-
"""
Analytics and tracking models for GVRC Admin
"""

from django.db import models
from django.utils import timezone


class ContactInteraction(models.Model):
    """Contact interaction tracking for analytics"""
    interaction_id = models.AutoField(primary_key=True)
    device = models.ForeignKey('mobile_sessions.MobileSession', on_delete=models.CASCADE, db_column='device_id', null=True, blank=True)
    contact = models.ForeignKey('facilities.FacilityContact', on_delete=models.CASCADE, db_column='contact_id', null=False)
    user_latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    user_longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    is_helpful = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    
    def __str__(self):
        device_id = self.device.device_id if self.device else "Unknown"
        return f"Interaction {self.interaction_id} from device {device_id}"
    
    class Meta:
        verbose_name_plural = "Contact Interactions"
        db_table = 'contact_interactions'


class AuditTrail(models.Model):
    """Comprehensive audit trail for all system activities"""
    audit_id = models.BigAutoField(primary_key=True)
    table_name = models.CharField(max_length=50, null=False)
    record_id = models.BigIntegerField(null=False)
    action_type = models.CharField(max_length=20, null=False)  # INSERT, UPDATE, DELETE, LOGIN, LOGOUT, READ, EXPORT
    event_category = models.CharField(max_length=20, null=False)  # DATA, AUTH, SYSTEM, SECURITY, ACCESS
    session = models.ForeignKey('authentication.UserSession', on_delete=models.SET_NULL, blank=True, null=True, db_column='session_id')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    changed_fields = models.JSONField(default=list, blank=True)  # Array of field names
    severity_level = models.CharField(max_length=10, default='INFO', null=False)  # DEBUG, INFO, WARN, ERROR, CRITICAL
    description = models.TextField(blank=True)
    justification = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    
    def __str__(self):
        return f"{self.action_type} on {self.table_name}.{self.record_id}"
    
    class Meta:
        verbose_name_plural = "Audit Trail"
        db_table = 'audit_trail'