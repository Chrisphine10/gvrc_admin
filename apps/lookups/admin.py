# -*- encoding: utf-8 -*-
"""
Admin configuration for lookup models
"""

from django.contrib import admin
from .models import (
    OperationalStatus, ContactType, ServiceCategory, OwnerType,
    GBVCategory, InfrastructureType, ConditionStatus, DocumentType
)


@admin.register(OperationalStatus)
class OperationalStatusAdmin(admin.ModelAdmin):
    """Admin configuration for OperationalStatus model"""
    list_display = ('status_name', 'description', 'sort_order')
    list_filter = ('sort_order',)
    search_fields = ('status_name', 'description')
    readonly_fields = ('operational_status_id',)
    ordering = ('sort_order', 'status_name')


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    """Admin configuration for ContactType model"""
    list_display = ('type_name', 'validation_regex')
    search_fields = ('type_name',)
    readonly_fields = ('contact_type_id',)
    ordering = ('type_name',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceCategory model"""
    list_display = ('category_name', 'description')
    search_fields = ('category_name', 'description')
    readonly_fields = ('service_category_id',)
    ordering = ('category_name',)


@admin.register(OwnerType)
class OwnerTypeAdmin(admin.ModelAdmin):
    """Admin configuration for OwnerType model"""
    list_display = ('type_name', 'description')
    search_fields = ('type_name', 'description')
    readonly_fields = ('owner_type_id',)
    ordering = ('type_name',)


@admin.register(GBVCategory)
class GBVCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for GBVCategory model"""
    list_display = ('category_name', 'description')
    search_fields = ('category_name', 'description')
    readonly_fields = ('gbv_category_id',)
    ordering = ('category_name',)


@admin.register(InfrastructureType)
class InfrastructureTypeAdmin(admin.ModelAdmin):
    """Admin configuration for InfrastructureType model"""
    list_display = ('type_name', 'description')
    search_fields = ('type_name', 'description')
    readonly_fields = ('infrastructure_type_id',)
    ordering = ('type_name',)


@admin.register(ConditionStatus)
class ConditionStatusAdmin(admin.ModelAdmin):
    """Admin configuration for ConditionStatus model"""
    list_display = ('status_name', 'description')
    search_fields = ('status_name', 'description')
    readonly_fields = ('condition_status_id',)
    ordering = ('status_name',)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    """Admin configuration for DocumentType model"""
    list_display = ('type_name', 'allowed_extensions', 'max_file_size_mb', 'description')
    list_filter = ('max_file_size_mb',)
    search_fields = ('type_name', 'description')
    readonly_fields = ('document_type_id',)
    ordering = ('type_name',)