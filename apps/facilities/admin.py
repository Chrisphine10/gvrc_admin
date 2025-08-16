# -*- encoding: utf-8 -*-
"""
Admin configuration for facilities app models
"""

from django.contrib import admin
from .models import (
    Facility, FacilityContact, FacilityCoordinate, 
    FacilityService, FacilityOwner, FacilityGBVCategory
)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_id', 'facility_name', 'registration_number', 'operational_status', 'ward', 'active_status')
    list_filter = ('operational_status', 'ward__constituency__county', 'active_status')
    search_fields = ('facility_name', 'registration_number', 'ward__ward_name')
    ordering = ('facility_name',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'operational_status', 'ward__constituency__county'
        )


@admin.register(FacilityContact)
class FacilityContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'facility', 'contact_type', 'contact_value', 'active_status')
    list_filter = ('contact_type', 'active_status', 'facility__ward__constituency__county')
    search_fields = ('contact_value', 'facility__facility_name')
    ordering = ('facility__facility_name', 'contact_type__type_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'contact_type'
        )


@admin.register(FacilityCoordinate)
class FacilityCoordinateAdmin(admin.ModelAdmin):
    list_display = ('coordinate_id', 'facility', 'latitude', 'longitude', 'collection_date', 'active_status')
    list_filter = ('active_status', 'collection_date', 'facility__ward__constituency__county')
    search_fields = ('facility__facility_name', 'coordinates_string')
    ordering = ('-collection_date',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility'
        )


@admin.register(FacilityService)
class FacilityServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'facility', 'service_category', 'active_status')
    list_filter = ('service_category', 'active_status', 'facility__ward__constituency__county')
    search_fields = ('facility__facility_name', 'service_description')
    ordering = ('facility__facility_name', 'service_category__category_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'service_category'
        )


@admin.register(FacilityOwner)
class FacilityOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'facility', 'owner_name', 'owner_type', 'active_status')
    list_filter = ('owner_type', 'active_status', 'facility__ward__constituency__county')
    search_fields = ('owner_name', 'facility__facility_name')
    ordering = ('facility__facility_name', 'owner_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'owner_type'
        )


@admin.register(FacilityGBVCategory)
class FacilityGBVCategoryAdmin(admin.ModelAdmin):
    list_display = ('facility', 'gbv_category')
    list_filter = ('gbv_category', 'facility__ward__constituency__county')
    search_fields = ('facility__facility_name', 'gbv_category__category_name')
    ordering = ('facility__facility_name', 'gbv_category__category_name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'gbv_category'
        )
