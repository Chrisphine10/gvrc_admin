# -*- encoding: utf-8 -*-
"""
Lookup table models for various categories and types (Master Data Tables)
"""

from django.db import models
from django.utils import timezone


class OperationalStatus(models.Model):
    """Operational status lookup table"""
    operational_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True, null=False)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0, null=False)
    
    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name_plural = "Operational Statuses"
        db_table = 'operational_statuses'
        ordering = ['sort_order']
        indexes = [
            models.Index(fields=['status_name']),
            models.Index(fields=['sort_order']),
        ]


class ContactType(models.Model):
    """Contact type lookup table"""
    contact_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True, null=False)
    validation_regex = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Contact Types"
        db_table = 'contact_types'
        indexes = [
            models.Index(fields=['type_name']),
        ]


class ServiceCategory(models.Model):
    """Service category lookup table"""
    service_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True, null=False)
    description = models.CharField(max_length=500, blank=True)
    icon_url = models.URLField(max_length=500, blank=True, help_text="URL to the icon for this service category")
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Service Categories"
        db_table = 'service_categories'
        indexes = [
            models.Index(fields=['category_name']),
        ]


class OwnerType(models.Model):
    """Owner type lookup table"""
    owner_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True, null=False)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Owner Types"
        db_table = 'owner_types'
        indexes = [
            models.Index(fields=['type_name']),
        ]


class GBVCategory(models.Model):
    """GBV category lookup table"""
    gbv_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True, null=False)
    description = models.CharField(max_length=500, blank=True)
    icon_url = models.URLField(max_length=500, blank=True, help_text="URL to the icon for this GBV category")
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "GBV Categories"
        db_table = 'gbv_categories'
        indexes = [
            models.Index(fields=['category_name']),
        ]


class InfrastructureType(models.Model):
    """Infrastructure type lookup table"""
    infrastructure_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, null=False)
    description = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Infrastructure Types"
        db_table = 'infrastructure_types'
        indexes = [
            models.Index(fields=['type_name']),
        ]


class ConditionStatus(models.Model):
    """Condition status lookup table"""
    condition_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True, null=False)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name_plural = "Condition Statuses"
        db_table = 'condition_statuses'
        indexes = [
            models.Index(fields=['status_name']),
        ]


class DocumentType(models.Model):
    """Document type lookup table"""
    document_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True, null=False)
    allowed_extensions = models.CharField(max_length=255, null=False)  # JSON array: ["pdf","jpg","png"]
    max_file_size_mb = models.IntegerField(default=10, null=False)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Document Types"
        db_table = 'document_types'
        indexes = [
            models.Index(fields=['type_name']),
        ]