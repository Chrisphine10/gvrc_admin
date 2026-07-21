# -*- encoding: utf-8 -*-
"""
Admin configuration for documents app
"""

from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model"""
    list_display = ('title', 'document_type', 'is_public', 'is_active', 'uploaded_at', 'uploaded_by', 'file_preview')
    list_filter = ('document_type', 'is_public', 'is_active', 'uploaded_at')
    search_fields = ('title', 'description', 'file_name', 'content')
    readonly_fields = ('document_id', 'uploaded_at', 'file_preview', 'file_info')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'document_type')
        }),
        ('File Upload', {
            'fields': ('file', 'file_preview', 'file_info'),
            'description': 'Upload a document file. Supported formats depend on document type. Maximum file size: 10MB (or as configured for document type).'
        }),
        ('Legacy File Information', {
            'fields': ('file_url', 'file_name', 'file_size_bytes', 'content'),
            'classes': ('collapse',),
            'description': 'Legacy fields for backward compatibility. Use file upload above for new documents.'
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
    
    def file_preview(self, obj):
        """Display file preview and download link"""
        if obj.file:
            from django.utils.html import format_html
            file_size = obj.get_file_size_mb()
            file_ext = obj.get_file_extension()
            return format_html(
                '<div style="margin: 10px 0;">'
                '<strong>Current File:</strong><br>'
                '<a href="{}" target="_blank" style="color: #5e72e4; text-decoration: none;">'
                '<i class="fas fa-file"></i> {}'
                '</a><br>'
                '<small style="color: #8392ab;">'
                'Size: {} MB | Type: {}'
                '</small>'
                '</div>',
                obj.file.url,
                obj.file_name or "Download File",
                file_size,
                file_ext or "Unknown"
            )
        return '<span style="color: #8392ab;">No file uploaded</span>'
    file_preview.short_description = 'File Preview'
    
    def file_info(self, obj):
        """Display file information"""
        if obj.file:
            return f'File: {obj.file_name} ({obj.get_file_size_mb()} MB)'
        return 'No file uploaded'
    file_info.short_description = 'File Information'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'document_type', 'uploaded_by'
        )
    
    def save_model(self, request, obj, form, change):
        """Set uploaded_by to current user if not set"""
        if not change:  # New object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)