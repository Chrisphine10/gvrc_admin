# -*- encoding: utf-8 -*-
"""
Music admin interface
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Music, MusicPlay


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    """Admin interface for Music model"""
    list_display = ['name', 'artist', 'genre', 'duration', 'total_listens', 'is_active', 'created_at']
    list_filter = ['is_active', 'genre', 'created_at', 'artist']
    search_fields = ['name', 'artist', 'description', 'genre']
    readonly_fields = ['total_listens', 'created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'artist', 'description', 'genre', 'duration')
        }),
        ('Media', {
            'fields': ('music_file', 'link'),
            'description': 'Upload a music file directly or provide an external link. If both are provided, the uploaded file takes precedence.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MusicPlay)
class MusicPlayAdmin(admin.ModelAdmin):
    """Admin interface for MusicPlay model"""
    list_display = ['music', 'user', 'played_at', 'session_duration', 'ip_address']
    list_filter = ['played_at', 'music', 'user']
    search_fields = ['music__name', 'user__full_name', 'ip_address']
    readonly_fields = ['played_at']
    list_per_page = 50
    
    fieldsets = (
        ('Play Information', {
            'fields': ('music', 'user', 'played_at')
        }),
        ('Session Details', {
            'fields': ('session_duration', 'ip_address', 'user_agent')
        }),
    )
    
    def has_add_permission(self, request):
        """Music plays are typically created automatically, not manually"""
        return False
