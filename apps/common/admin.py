# -*- encoding: utf-8 -*-
"""
Admin configuration for common app models
"""

from django.contrib import admin
from .geography import County, Constituency, Ward
from .lookups import (
    OperationalStatus, ContactType, ServiceCategory,
    OwnerType, GBVCategory, DocumentType
)
from .documents import Document


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('county_id', 'county_name')
    search_fields = ('county_name',)
    ordering = ('county_name',)


@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('constituency_id', 'constituency_name', 'county')
    list_filter = ('county',)
    search_fields = ('constituency_name', 'county__county_name')
    ordering = ('county__county_name', 'constituency_name')


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_id', 'ward_name', 'constituency', 'county')
    list_filter = ('constituency__county', 'constituency')
    search_fields = ('ward_name', 'constituency__constituency_name', 'constituency__county__county_name')
    ordering = ('constituency__county__county_name', 'constituency__constituency_name', 'ward_name')
    
    def county(self, obj):
        return obj.constituency.county.county_name
    county.short_description = 'County'


@admin.register(OperationalStatus)
class OperationalStatusAdmin(admin.ModelAdmin):
    list_display = ('operational_status_id', 'status_name')
    search_fields = ('status_name',)
    ordering = ('status_name',)


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    list_display = ('contact_type_id', 'type_name')
    search_fields = ('type_name',)
    ordering = ('type_name',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('service_category_id', 'category_name')
    search_fields = ('category_name',)
    ordering = ('category_name',)


@admin.register(OwnerType)
class OwnerTypeAdmin(admin.ModelAdmin):
    list_display = ('owner_type_id', 'type_name')
    search_fields = ('type_name',)
    ordering = ('type_name',)


@admin.register(GBVCategory)
class GBVCategoryAdmin(admin.ModelAdmin):
    list_display = ('gbv_category_id', 'category_name', 'description')
    search_fields = ('category_name', 'description')
    ordering = ('category_name',)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('document_type_id', 'type_name', 'description')
    search_fields = ('type_name', 'description')
    ordering = ('type_name',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'title', 'facility', 'gbv_category', 'document_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('gbv_category', 'document_type', 'facility__ward__constituency__county')
    search_fields = ('title', 'description', 'facility__facility_name')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility', 'gbv_category', 'document_type', 'uploaded_by'
        )
