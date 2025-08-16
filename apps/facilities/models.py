# -*- encoding: utf-8 -*-
"""
Facility models for GVRC Admin
"""

from django.db import models
from apps.common.models import ActiveStatusModel
from apps.common.geography import Ward
from apps.common.lookups import OperationalStatus, ContactType, ServiceCategory, OwnerType, GBVCategory


class Facility(ActiveStatusModel):
    """Community-based facility model"""
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=200, null=False)
    registration_number = models.CharField(max_length=50, unique=True)
    operational_status = models.ForeignKey('common.OperationalStatus', on_delete=models.CASCADE, db_column='operational_status_id', null=True, blank=True)
    ward = models.ForeignKey('common.Ward', on_delete=models.CASCADE, db_column='ward_id', null=True, blank=True)
    
    def __str__(self):
        return f"{self.facility_name} - {self.ward.ward_name}"
    
    class Meta:
        verbose_name_plural = "Facilities"
        db_table = 'facilities'
        indexes = [
            models.Index(fields=['ward']),
        ]


class FacilityContact(ActiveStatusModel):
    """Facility contact information"""
    contact_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id')
    contact_type = models.ForeignKey('common.ContactType', on_delete=models.CASCADE, db_column='contact_type_id', null=True, blank=True)
    contact_value = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.contact_type.type_name}: {self.contact_value}"
    
    class Meta:
        verbose_name_plural = "Facility Contacts"
        db_table = 'facility_contacts'


class FacilityCoordinate(ActiveStatusModel):
    """Facility geographical coordinates"""
    coordinate_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    coordinates_string = models.CharField(max_length=100, blank=True)
    collection_date = models.DateField(null=True, blank=True)
    data_source = models.CharField(max_length=100, blank=True)
    collection_method = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.latitude}, {self.longitude}"
    
    class Meta:
        verbose_name_plural = "Facility Coordinates"
        db_table = 'facility_coordinates'


class FacilityService(ActiveStatusModel):
    """Services offered by facilities"""
    service_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id')
    service_category = models.ForeignKey('common.ServiceCategory', on_delete=models.CASCADE, db_column='service_category_id', null=True, blank=True)
    service_description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.service_category.category_name}"
    
    class Meta:
        verbose_name_plural = "Facility Services"
        db_table = 'facility_services'


class FacilityOwner(ActiveStatusModel):
    """Facility ownership information"""
    owner_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id')
    owner_name = models.CharField(max_length=200)
    owner_type = models.ForeignKey('common.OwnerType', on_delete=models.CASCADE, db_column='owner_type_id', null=True, blank=True)
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.owner_name} ({self.owner_type.type_name})"
    
    class Meta:
        verbose_name_plural = "Facility Owners"
        db_table = 'facility_owners'


class FacilityGBVCategory(models.Model):
    """Many-to-many relationship between facilities and GBV categories"""
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, db_column='facility_id')
    gbv_category = models.ForeignKey('common.GBVCategory', on_delete=models.CASCADE, db_column='gbv_category_id', null=True, blank=True)
    
    class Meta:
        db_table = 'facility_gbv_categories'
        unique_together = ('facility', 'gbv_category')
