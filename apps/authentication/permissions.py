# -*- encoding: utf-8 -*-
"""
Permission utilities and decorators for role-based access control
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

from .models import User, UserRole, Permission, UserRoleAssignment, RolePermission


def has_permission(user, permission_name):
    """
    Check if a user has a specific permission through their roles
    
    Args:
        user: User instance
        permission_name: String permission name (e.g., 'view_facilities')
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    # Superusers have all permissions
    if user.is_superuser:
        return True
    
    # Check if user has permission through their roles
    user_roles = UserRoleAssignment.objects.filter(
        user=user,
        expires_at__isnull=True  # Non-expired roles only
    ).values_list('role', flat=True)
    
    return RolePermission.objects.filter(
        role__in=user_roles,
        permission__permission_name=permission_name
    ).exists()


def has_role(user, role_name):
    """
    Check if a user has a specific role
    
    Args:
        user: User instance
        role_name: String role name (e.g., 'Facility Manager')
    
    Returns:
        bool: True if user has role, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    # Superusers have all roles
    if user.is_superuser:
        return True
    
    return UserRoleAssignment.objects.filter(
        user=user,
        role__role_name=role_name,
        expires_at__isnull=True  # Non-expired roles only
    ).exists()


def has_any_role(user, role_names):
    """
    Check if a user has any of the specified roles
    
    Args:
        user: User instance
        role_names: List of role names
    
    Returns:
        bool: True if user has any of the roles, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    # Superusers have all roles
    if user.is_superuser:
        return True
    
    return UserRoleAssignment.objects.filter(
        user=user,
        role__role_name__in=role_names,
        expires_at__isnull=True  # Non-expired roles only
    ).exists()


def get_user_permissions(user):
    """
    Get all permissions for a user through their roles
    
    Args:
        user: User instance
    
    Returns:
        QuerySet: Permissions the user has
    """
    if not user or not user.is_authenticated:
        return Permission.objects.none()
    
    # Superusers have all permissions
    if user.is_superuser:
        return Permission.objects.all()
    
    user_roles = UserRoleAssignment.objects.filter(
        user=user,
        expires_at__isnull=True  # Non-expired roles only
    ).values_list('role', flat=True)
    
    return Permission.objects.filter(
        rolepermission__role__in=user_roles
    ).distinct()


def get_user_roles(user):
    """
    Get all roles for a user
    
    Args:
        user: User instance
    
    Returns:
        QuerySet: Roles the user has
    """
    if not user or not user.is_authenticated:
        return UserRole.objects.none()
    
    # Superusers have all roles
    if user.is_superuser:
        return UserRole.objects.all()
    
    return UserRole.objects.filter(
        userroleassignment__user=user,
        userroleassignment__expires_at__isnull=True  # Non-expired roles only
    ).distinct()


def permission_required(permission_name, redirect_url=None, message=None):
    """
    Decorator to require a specific permission for a view
    
    Args:
        permission_name: String permission name required
        redirect_url: URL to redirect to if permission denied (default: '/dashboard/')
        message: Error message to show (default: generic message)
    
    Usage:
        @permission_required('view_facilities')
        def facility_list(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission_name):
                if message:
                    messages.error(request, message)
                else:
                    messages.error(request, f'You do not have permission to access this page. Required permission: {permission_name}')
                
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def role_required(role_name, redirect_url=None, message=None):
    """
    Decorator to require a specific role for a view
    
    Args:
        role_name: String role name required
        redirect_url: URL to redirect to if role denied (default: '/dashboard/')
        message: Error message to show (default: generic message)
    
    Usage:
        @role_required('Facility Manager')
        def facility_create(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not has_role(request.user, role_name):
                if message:
                    messages.error(request, message)
                else:
                    messages.error(request, f'You do not have the required role to access this page. Required role: {role_name}')
                
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def any_role_required(role_names, redirect_url=None, message=None):
    """
    Decorator to require any of the specified roles for a view
    
    Args:
        role_names: List of role names (user needs at least one)
        redirect_url: URL to redirect to if role denied (default: '/dashboard/')
        message: Error message to show (default: generic message)
    
    Usage:
        @any_role_required(['Facility Manager', 'System Administrator'])
        def facility_edit(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not has_any_role(request.user, role_names):
                if message:
                    messages.error(request, message)
                else:
                    roles_str = ', '.join(role_names)
                    messages.error(request, f'You do not have the required role to access this page. Required roles: {roles_str}')
                
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def staff_required(redirect_url=None, message=None):
    """
    Decorator to require staff status for a view
    
    Args:
        redirect_url: URL to redirect to if not staff (default: '/dashboard/')
        message: Error message to show (default: generic message)
    
    Usage:
        @staff_required()
        def admin_panel(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.is_staff:
                if message:
                    messages.error(request, message)
                else:
                    messages.error(request, 'You must be a staff member to access this page.')
                
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def superuser_required(redirect_url=None, message=None):
    """
    Decorator to require superuser status for a view
    
    Args:
        redirect_url: URL to redirect to if not superuser (default: '/dashboard/')
        message: Error message to show (default: generic message)
    
    Usage:
        @superuser_required()
        def system_settings(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.is_superuser:
                if message:
                    messages.error(request, message)
                else:
                    messages.error(request, 'You must be a superuser to access this page.')
                
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# REST Framework Permission Classes

class HasPermissionPermission(BasePermission):
    """
    DRF permission class to check for specific permissions
    """
    
    def __init__(self, permission_name):
        self.permission_name = permission_name
    
    def has_permission(self, request, view):
        return has_permission(request.user, self.permission_name)


class HasRolePermission(BasePermission):
    """
    DRF permission class to check for specific roles
    """
    
    def __init__(self, role_name):
        self.role_name = role_name
    
    def has_permission(self, request, view):
        return has_role(request.user, self.role_name)


class HasAnyRolePermission(BasePermission):
    """
    DRF permission class to check for any of the specified roles
    """
    
    def __init__(self, role_names):
        self.role_names = role_names
    
    def has_permission(self, request, view):
        return has_any_role(request.user, self.role_names)


class StaffPermission(BasePermission):
    """
    DRF permission class to check for staff status
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class SuperuserPermission(BasePermission):
    """
    DRF permission class to check for superuser status
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


# Template context processors and utilities

def user_permissions_context(request):
    """
    Template context processor to add user permissions to template context
    """
    if request.user.is_authenticated:
        return {
            'user_permissions': get_user_permissions(request.user),
            'user_roles': get_user_roles(request.user),
            'has_permission': has_permission,
            'has_role': has_role,
            'has_any_role': has_any_role,
        }
    return {}


# AJAX permission checking utilities

def ajax_permission_required(permission_name):
    """
    Decorator for AJAX views that require specific permissions
    Returns JSON response instead of redirect
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission_name):
                return JsonResponse({
                    'success': False,
                    'error': f'Permission denied. Required permission: {permission_name}'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def ajax_role_required(role_name):
    """
    Decorator for AJAX views that require specific roles
    Returns JSON response instead of redirect
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not has_role(request.user, role_name):
                return JsonResponse({
                    'success': False,
                    'error': f'Permission denied. Required role: {role_name}'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Permission checking for API views

def check_api_permission(user, permission_name):
    """
    Check permission for API views and return appropriate response
    """
    if not has_permission(user, permission_name):
        return Response({
            'error': 'Permission denied',
            'message': f'Required permission: {permission_name}'
        }, status=status.HTTP_403_FORBIDDEN)
    return None


def check_api_role(user, role_name):
    """
    Check role for API views and return appropriate response
    """
    if not has_role(user, role_name):
        return Response({
            'error': 'Permission denied',
            'message': f'Required role: {role_name}'
        }, status=status.HTTP_403_FORBIDDEN)
    return None
