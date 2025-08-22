# -*- encoding: utf-8 -*-
"""
Facility models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from apps.geography.models import Ward
from apps.lookups.models import (
    OperationalStatus, ContactType, ServiceCategory, OwnerType, 
    GBVCategory, InfrastructureType, ConditionStatus
)


class Facility(models.Model):
    """Community-based facility model"""
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=200, null=False)
    facility_code = models.CharField(max_length=50, unique=True, blank=True)
    registration_number = models.CharField(max_length=100, unique=True)
    operational_status = models.ForeignKey(OperationalStatus, on_delete=models.CASCADE, db_column='operational_status_id', null=False)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, db_column='ward_id', null=False)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, null=False)
    description = models.TextField(blank=True)
    website_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='facilities_created', db_column='created_by', null=False)
    updated_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='facilities_updated', db_column='updated_by')
    
    def __str__(self):
        return f"{self.facility_name} - {self.ward.ward_name}"
    
    class Meta:
        verbose_name_plural = "Facilities"
        db_table = 'facilities'
        indexes = [
            models.Index(fields=['ward']),
            models.Index(fields=['operational_status']),
            models.Index(fields=['is_active']),
        ]


class FacilityContact(models.Model):
    """Facility contact information"""
    contact_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id', null=False)
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE, db_column='contact_type_id', null=False)
    contact_value = models.CharField(max_length=255, null=False)
    contact_person_name = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='facility_contacts_created', db_column='created_by', null=False)
    updated_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='facility_contacts_updated', db_column='updated_by')
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.contact_type.type_name}: {self.contact_value}"
    
    class Meta:
        verbose_name_plural = "Facility Contacts"
        db_table = 'facility_contacts'
        indexes = [
            models.Index(fields=['facility']),
            models.Index(fields=['contact_type']),
            models.Index(fields=['is_primary']),
        ]


class FacilityCoordinate(models.Model):
    """Facility geographical coordinates"""
    coordinate_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id', null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=False)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=False)
    collection_date = models.DateField(null=False)
    data_source = models.CharField(max_length=100, blank=True)
    collection_method = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.latitude}, {self.longitude}"
    
    class Meta:
        verbose_name_plural = "Facility Coordinates"
        db_table = 'facility_coordinates'
        indexes = [
            models.Index(fields=['facility']),
            models.Index(fields=['collection_date']),
        ]


class FacilityService(models.Model):
    """Services offered by facilities"""
    service_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id', null=False)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, db_column='service_category_id', null=False)
    service_name = models.CharField(max_length=200, null=False)
    service_description = models.TextField(blank=True)
    is_free = models.BooleanField(default=False, null=False)
    cost_range = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=3, default='KES')
    availability_hours = models.CharField(max_length=200, blank=True)
    availability_days = models.CharField(max_length=100, blank=True)  # JSON or comma-separated
    appointment_required = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.service_name}"
    
    class Meta:
        verbose_name_plural = "Facility Services"
        db_table = 'facility_services'
        indexes = [
            models.Index(fields=['facility']),
            models.Index(fields=['service_category']),
            models.Index(fields=['is_active']),
        ]


class FacilityInfrastructure(models.Model):
    """Facility infrastructure and equipment"""
    infrastructure_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id', null=False)
    infrastructure_type = models.ForeignKey(InfrastructureType, on_delete=models.CASCADE, db_column='infrastructure_type_id', null=False)
    condition_status = models.ForeignKey(ConditionStatus, on_delete=models.CASCADE, db_column='condition_status_id', null=False)
    description = models.TextField(blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    current_utilization = models.IntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.infrastructure_type.type_name}"
    
    class Meta:
        verbose_name_plural = "Facility Infrastructure"
        db_table = 'facility_infrastructure'
        indexes = [
            models.Index(fields=['facility']),
            models.Index(fields=['infrastructure_type']),
            models.Index(fields=['condition_status']),
        ]


class FacilityOwner(models.Model):
    """Facility ownership information"""
    owner_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id', null=False)
    owner_name = models.CharField(max_length=200, null=False)
    owner_type = models.ForeignKey(OwnerType, on_delete=models.CASCADE, db_column='owner_type_id', null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='facility_owners_created', db_column='created_by', null=False)
    updated_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='facility_owners_updated', db_column='updated_by')
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.owner_name} ({self.owner_type.type_name})"
    
    class Meta:
        verbose_name_plural = "Facility Owners"
        db_table = 'facility_owners'
        indexes = [
            models.Index(fields=['facility']),
            models.Index(fields=['owner_type']),
        ]


class FacilityGBVCategory(models.Model):
    """Many-to-many relationship between facilities and GBV categories"""
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id', null=False)
    gbv_category = models.ForeignKey(GBVCategory, on_delete=models.CASCADE, db_column='gbv_category_id', null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='facility_gbv_categories_created', db_column='created_by', null=False)
    
    class Meta:
        db_table = 'facility_gbv_categories'
        unique_together = ('facility', 'gbv_category')
        indexes = [
            models.Index(fields=['facility']),
            models.Index(fields=['gbv_category']),
        ]
