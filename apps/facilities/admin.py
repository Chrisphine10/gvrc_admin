# -*- encoding: utf-8 -*-
"""
Admin configuration for facilities app models
"""

from django.contrib import admin
from .models import (
    Facility, FacilityContact, FacilityCoordinate, 
    FacilityService, FacilityInfrastructure, FacilityOwner, FacilityGBVCategory
)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_id', 'facility_name', 'facility_code', 'registration_number', 'operational_status', 'ward', 'is_active')
    list_filter = ('operational_status', 'ward__constituency__county', 'is_active')
    search_fields = ('facility_name', 'facility_code', 'registration_number', 'ward__ward_name')
    ordering = ('facility_name',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    fieldsets = (
        ('Basic Information', {
            'fields': ('facility_name', 'facility_code', 'registration_number', 'operational_status', 'ward')
        }),
        ('Location', {
            'fields': ('address_line_1', 'address_line_2')
        }),
        ('Details', {
            'fields': ('description', 'website_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'operational_status', 'ward__constituency__county'
        )


@admin.register(FacilityContact)
class FacilityContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'facility', 'contact_type', 'contact_value', 'contact_person_name', 'is_primary', 'is_active')
    list_filter = ('contact_type', 'is_primary', 'is_active', 'facility__ward__constituency__county')
    search_fields = ('contact_value', 'contact_person_name', 'facility__facility_name')
    ordering = ('facility__facility_name', 'contact_type__type_name')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'contact_type'
        )


@admin.register(FacilityCoordinate)
class FacilityCoordinateAdmin(admin.ModelAdmin):
    list_display = ('coordinate_id', 'facility', 'latitude', 'longitude', 'collection_date', 'data_source')
    list_filter = ('collection_date', 'data_source', 'facility__ward__constituency__county')
    search_fields = ('facility__facility_name',)
    ordering = ('-collection_date',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility'
        )


@admin.register(FacilityService)
class FacilityServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'facility', 'service_category', 'service_name', 'is_free', 'is_active')
    list_filter = ('service_category', 'is_free', 'is_active', 'facility__ward__constituency__county')
    search_fields = ('service_name', 'facility__facility_name', 'service_description')
    ordering = ('facility__facility_name', 'service_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('facility', 'service_category', 'service_name', 'service_description')
        }),
        ('Availability', {
            'fields': ('is_free', 'cost_range', 'currency', 'availability_hours', 'availability_days')
        }),
        ('Settings', {
            'fields': ('appointment_required', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'service_category'
        )


@admin.register(FacilityInfrastructure)
class FacilityInfrastructureAdmin(admin.ModelAdmin):
    list_display = ('infrastructure_id', 'facility', 'infrastructure_type', 'condition_status', 'capacity', 'is_available', 'is_active')
    list_filter = ('infrastructure_type', 'condition_status', 'is_available', 'is_active', 'facility__ward__constituency__county')
    search_fields = ('facility__facility_name', 'infrastructure_type__type_name', 'description')
    ordering = ('facility__facility_name', 'infrastructure_type__type_name')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    fieldsets = (
        ('Basic Information', {
            'fields': ('facility', 'infrastructure_type', 'condition_status', 'description')
        }),
        ('Capacity', {
            'fields': ('capacity', 'current_utilization', 'is_available')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'infrastructure_type', 'condition_status'
        )


@admin.register(FacilityOwner)
class FacilityOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'facility', 'owner_name', 'owner_type', 'created_at')
    list_filter = ('owner_type', 'facility__ward__constituency__county', 'created_at')
    search_fields = ('owner_name', 'facility__facility_name')
    ordering = ('facility__facility_name', 'owner_name')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'owner_type'
        )


@admin.register(FacilityGBVCategory)
class FacilityGBVCategoryAdmin(admin.ModelAdmin):
    list_display = ('facility', 'gbv_category', 'created_at', 'created_by')
    list_filter = ('gbv_category', 'facility__ward__constituency__county', 'created_at')
    search_fields = ('facility__facility_name', 'gbv_category__category_name')
    ordering = ('facility__facility_name', 'gbv_category__category_name')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'gbv_category'
        )
