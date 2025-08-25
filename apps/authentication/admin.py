# -*- encoding: utf-8 -*-
"""
Admin configuration for authentication app models
"""

from django.contrib import admin
from .models import (
    User, UserRole, Permission, RolePermission, UserRoleAssignment,
    UserProfile, UserSession, ApiToken, CustomToken
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'email', 'phone_number', 'is_active', 'verified', 'created_at')
    list_filter = ('is_active', 'verified', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at', 'password_changed_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Status', {
            'fields': ('is_active', 'verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'password_changed_at'),
            'classes': ('collapse',)
        }),
        ('Django Admin', {
            'fields': ('is_staff', 'is_superuser', 'username'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'is_system_role', 'created_at')
    list_filter = ('is_system_role', 'created_at')
    search_fields = ('role_name', 'description')
    ordering = ('role_name',)
    readonly_fields = ('created_at',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_id', 'permission_name', 'resource_name', 'action_name')
    list_filter = ('resource_name', 'action_name')
    search_fields = ('permission_name', 'resource_name', 'description')
    ordering = ('resource_name', 'action_name')


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'granted_at', 'granted_by')
    list_filter = ('role', 'permission', 'granted_at')
    search_fields = ('role__role_name', 'permission__permission_name')
    ordering = ('role__role_name', 'permission__permission_name')
    readonly_fields = ('granted_at',)


@admin.register(UserRoleAssignment)
class UserRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_at', 'assigned_by', 'expires_at')
    list_filter = ('role', 'assigned_at', 'expires_at')
    search_fields = ('user__full_name', 'role__role_name')
    ordering = ('user__full_name', 'role__role_name')
    readonly_fields = ('assigned_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'user', 'department', 'job_title', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('user__full_name', 'department', 'job_title')
    ordering = ('user__full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'ip_address', 'game_high_score', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('session_id', 'user__full_name', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('session_id', 'created_at', 'last_activity_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')





@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ('token_id', 'user', 'token_name', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('token_name', 'user__full_name')
    ordering = ('-created_at',)
    readonly_fields = ('token_hash', 'created_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')





@admin.register(CustomToken)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    search_fields = ('user__full_name', 'key')
    ordering = ('-created',)
    readonly_fields = ('key', 'created')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
