# -*- encoding: utf-8 -*-
"""
Admin configuration for authentication app models
"""

from django.contrib import admin
from .models import (
    User, UserLocation, AuthenticationMethod, UserAuthMethod,
    AccessLevel, UserAccessLevel, UserSession, ApiToken, 
    ResetToken, ContactClick
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'email', 'phone_number', 'is_active', 'facility')
    list_filter = ('is_active', 'facility__ward__constituency__county')
    search_fields = ('full_name', 'email', 'phone_number')
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'facility__ward__constituency__county'
        )


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'user', 'ward', 'captured_at')
    list_filter = ('ward__constituency__county', 'captured_at')
    search_fields = ('user__full_name', 'ward__ward_name')
    ordering = ('-captured_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'ward__constituency__county'
        )


@admin.register(AuthenticationMethod)
class AuthenticationMethodAdmin(admin.ModelAdmin):
    list_display = ('auth_id', 'method_name', 'description')
    search_fields = ('method_name', 'description')
    ordering = ('method_name',)


@admin.register(UserAuthMethod)
class UserAuthMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_method')
    list_filter = ('auth_method',)
    search_fields = ('user__full_name', 'auth_method__method_name')
    ordering = ('user__full_name', 'auth_method__method_name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'auth_method'
        )


@admin.register(AccessLevel)
class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ('access_id', 'level_name', 'description')
    search_fields = ('level_name', 'description')
    ordering = ('level_name',)


@admin.register(UserAccessLevel)
class UserAccessLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_level')
    list_filter = ('access_level',)
    search_fields = ('user__full_name', 'access_level__level_name')
    ordering = ('user__full_name', 'access_level__level_name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'access_level'
        )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'ip_address', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('session_id', 'user__full_name', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('session_id',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ('token_id', 'session', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('token_hash', 'session__user__full_name')
    ordering = ('-created_at',)
    readonly_fields = ('token_hash',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'session__user'
        )


@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ('reset_id', 'user', 'created_at', 'expires_at', 'used')
    list_filter = ('used', 'created_at', 'expires_at')
    search_fields = ('token_hash', 'user__full_name')
    ordering = ('-created_at',)
    readonly_fields = ('token_hash',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(ContactClick)
class ContactClickAdmin(admin.ModelAdmin):
    list_display = ('click_id', 'user', 'facility', 'contact', 'clicked_at', 'helpful')
    list_filter = ('helpful', 'clicked_at', 'facility__ward__constituency__county')
    search_fields = ('user__full_name', 'facility__facility_name')
    ordering = ('-clicked_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'facility', 'contact'
        )
