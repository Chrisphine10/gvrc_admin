# -*- encoding: utf-8 -*-
"""
Admin configuration for facilities
"""

from django.contrib import admin
from .models import Facility, Facility_Services, Facility_HumanResources, Facility_Infrastructure


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'ownership', 'county', 'ward', 'is_active', 'registration_number')
    list_filter = ('facility_type', 'ownership', 'county', 'is_active')
    search_fields = ('name', 'registration_number', 'contact_person', 'phone', 'email', 'target_population')
    readonly_fields = ('created_at', 'modified_at')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'facility_type', 'ownership', 'registration_number', 'is_active')
        }),
        ('Location Information', {
            'fields': ('county', 'ward', 'location', 'latitude', 'longitude'),
            'description': 'Enter the facility location details including GPS coordinates for mapping purposes.'
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'phone', 'email', 'emergency_contact')
        }),
        ('Services & Operations', {
            'fields': ('target_population', 'services_offered', 'operating_hours')
        }),
        ('System Information', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Facility_Services)
class FacilityServicesAdmin(admin.ModelAdmin):
    list_display = ('facility', 'service_name', 'category', 'is_available')
    list_filter = ('category', 'is_available', 'facility__facility_type')
    search_fields = ('service_name', 'facility__name', 'description')
    readonly_fields = ('created_at', 'modified_at')
    list_per_page = 25


@admin.register(Facility_HumanResources)
class FacilityHumanResourcesAdmin(admin.ModelAdmin):
    list_display = ('facility', 'full_name', 'position', 'staff_category', 'is_active')
    list_filter = ('staff_category', 'is_active', 'facility__facility_type')
    search_fields = ('full_name', 'position', 'facility__name', 'license_number')
    readonly_fields = ('created_at', 'modified_at')
    list_per_page = 25


@admin.register(Facility_Infrastructure)
class FacilityInfrastructureAdmin(admin.ModelAdmin):
    list_display = ('facility', 'equipment_name', 'category', 'quantity', 'condition', 'is_operational', 'get_operational_status_display')
    list_filter = ('category', 'condition', 'is_operational', 'facility__facility_type')
    search_fields = ('equipment_name', 'facility__name', 'registration_number', 'notes')
    readonly_fields = ('created_at', 'modified_at')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('facility', 'equipment_name', 'category', 'quantity', 'is_operational')
        }),
        ('Equipment Details', {
            'fields': ('condition', 'capacity', 'model_year', 'notes'),
            'description': 'Equipment specifications and condition details.'
        }),
        ('Vehicle Information', {
            'fields': ('registration_number', 'fuel_type', 'insurance_expiry'),
            'description': 'Vehicle-specific information (only applicable for vehicles).',
            'classes': ('collapse',)
        }),
        ('Maintenance Schedule', {
            'fields': ('last_maintenance', 'next_maintenance'),
            'description': 'Maintenance tracking for equipment and vehicles.',
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_operational_status_display(self, obj):
        """Display operational status with color coding"""
        status = obj.get_operational_status()
        if status == "Operational":
            return f'<span style="color: green;">{status}</span>'
        elif status == "Needs Maintenance":
            return f'<span style="color: orange;">{status}</span>'
        else:
            return f'<span style="color: red;">{status}</span>'
    get_operational_status_display.short_description = 'Status'
    get_operational_status_display.allow_tags = True
