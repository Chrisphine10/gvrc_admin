# -*- encoding: utf-8 -*-
"""
Admin configuration for geography models
"""

from django.contrib import admin
from .models import County, Constituency, Ward


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    """Admin configuration for County model"""
    list_display = ('county_name', 'county_code', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('county_name', 'county_code')
    readonly_fields = ('county_id', 'created_at', 'updated_at')
    ordering = ('county_name',)


@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    """Admin configuration for Constituency model"""
    list_display = ('constituency_name', 'county', 'constituency_code', 'created_at')
    list_filter = ('county', 'created_at', 'updated_at')
    search_fields = ('constituency_name', 'constituency_code', 'county__county_name')
    readonly_fields = ('constituency_id', 'created_at', 'updated_at')
    ordering = ('constituency_name',)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    """Admin configuration for Ward model"""
    list_display = ('ward_name', 'constituency', 'ward_code', 'created_at')
    list_filter = ('constituency__county', 'constituency', 'created_at', 'updated_at')
    search_fields = ('ward_name', 'ward_code', 'constituency__constituency_name', 'constituency__county__county_name')
    readonly_fields = ('ward_id', 'created_at', 'updated_at')
    ordering = ('ward_name',)