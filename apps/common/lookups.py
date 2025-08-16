# -*- encoding: utf-8 -*-
"""
Lookup table models for various categories and types
"""

from django.db import models


class OperationalStatus(models.Model):
    """Operational status lookup table"""
    operational_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name_plural = "Operational Statuses"
        db_table = 'operational_statuses'


class ContactType(models.Model):
    """Contact type lookup table"""
    contact_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Contact Types"
        db_table = 'contact_types'


class ServiceCategory(models.Model):
    """Service category lookup table"""
    service_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Service Categories"
        db_table = 'service_categories'


class OwnerType(models.Model):
    """Owner type lookup table"""
    owner_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Owner Types"
        db_table = 'owner_types'


class GBVCategory(models.Model):
    """GBV category lookup table"""
    gbv_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "GBV Categories"
        db_table = 'gbv_categories'


class DocumentType(models.Model):
    """Document type lookup table"""
    document_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Document Types"
        db_table = 'document_types'
