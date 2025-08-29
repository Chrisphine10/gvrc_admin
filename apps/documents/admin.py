# -*- encoding: utf-8 -*-
"""
Admin configuration for documents app
"""

from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model"""
    list_display = ('title', 'document_type', 'is_public', 'is_active', 'uploaded_at', 'uploaded_by')
    list_filter = ('document_type', 'is_public', 'is_active', 'uploaded_at')
    search_fields = ('title', 'description', 'file_name', 'content')
    readonly_fields = ('document_id', 'uploaded_at')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'document_type')
        }),
        ('File Information', {
            'fields': ('file_url', 'file_name', 'file_size_bytes', 'content')
        }),
        ('Media & Links', {
            'fields': ('gbv_category', 'image_url', 'external_url')
        }),
        ('Settings', {
            'fields': ('is_public', 'is_active', 'uploaded_by')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'document_type', 'uploaded_by'
        )