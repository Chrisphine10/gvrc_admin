# -*- encoding: utf-8 -*-
"""
Settings views for common app
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from .models import ApplicationSettings
from .forms import ApplicationSettingsForm, ThemePreviewForm


@login_required
def application_settings(request):
    """Display and manage application settings"""
    # Get or create settings instance
    settings_obj = ApplicationSettings.get_settings()
    
    if request.method == 'POST':
        form = ApplicationSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Application settings updated successfully!')
                return redirect('common:application_settings')
            except Exception as e:
                messages.error(request, f'Error updating settings: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationSettingsForm(instance=settings_obj)
    
    # Get current roles and permissions count for debugging
    from apps.authentication.models import UserRole, Permission
    roles_count = UserRole.objects.count()
    permissions_count = Permission.objects.count()
    
    context = {
        'form': form,
        'settings': settings_obj,
        'segment': 'settings',
        'page_title': 'Application Settings',
        'roles_count': roles_count,
        'permissions_count': permissions_count,
    }
    
    return render(request, 'common/application_settings.html', context)


@login_required
@require_http_methods(["POST"])
def preview_theme(request):
    """Preview theme colors without saving"""
    form = ThemePreviewForm(request.POST)
    
    if form.is_valid():
        # Generate CSS variables for preview
        css_variables = {
            '--primary-color': form.cleaned_data.get('primary_color', '#5e72e4'),
            '--secondary-color': form.cleaned_data.get('secondary_color', '#8392ab'),
            '--success-color': form.cleaned_data.get('success_color', '#2dce89'),
            '--warning-color': form.cleaned_data.get('warning_color', '#fb6340'),
            '--danger-color': form.cleaned_data.get('danger_color', '#f5365c'),
            '--info-color': form.cleaned_data.get('info_color', '#11cdef'),
            '--dark-color': form.cleaned_data.get('dark_color', '#212529'),
            '--light-color': form.cleaned_data.get('light_color', '#f8f9fe'),
        }
        
        return JsonResponse({
            'success': True,
            'css_variables': css_variables
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


@login_required
@require_http_methods(["POST"])
def reset_theme_colors(request):
    """Reset theme colors to default values"""
    try:
        settings_obj = ApplicationSettings.get_settings()
        
        # Reset to default colors
        settings_obj.primary_color = '#5e72e4'
        settings_obj.secondary_color = '#8392ab'
        settings_obj.success_color = '#2dce89'
        settings_obj.warning_color = '#fb6340'
        settings_obj.danger_color = '#f5365c'
        settings_obj.info_color = '#11cdef'
        settings_obj.dark_color = '#212529'
        settings_obj.light_color = '#f8f9fe'
        
        settings_obj.save()
        messages.success(request, 'Theme colors reset to default values!')
        
    except Exception as e:
        messages.error(request, f'Error resetting theme colors: {str(e)}')
    
    return redirect('common:application_settings')


@login_required
@require_http_methods(["POST"])
def delete_logo(request):
    """Delete current logo"""
    try:
        settings_obj = ApplicationSettings.get_settings()
        
        if settings_obj.logo:
            # Delete the file from storage
            if default_storage.exists(settings_obj.logo.name):
                default_storage.delete(settings_obj.logo.name)
            
            # Clear the field
            settings_obj.logo = None
            settings_obj.save()
            
            messages.success(request, 'Logo deleted successfully!')
        else:
            messages.info(request, 'No logo to delete.')
            
    except Exception as e:
        messages.error(request, f'Error deleting logo: {str(e)}')
    
    return redirect('common:application_settings')


@login_required
@require_http_methods(["POST"])
def delete_favicon(request):
    """Delete current favicon"""
    try:
        settings_obj = ApplicationSettings.get_settings()
        
        if settings_obj.favicon:
            # Delete the file from storage
            if default_storage.exists(settings_obj.favicon.name):
                default_storage.delete(settings_obj.favicon.name)
            
            # Clear the field
            settings_obj.favicon = None
            settings_obj.save()
            
            messages.success(request, 'Favicon deleted successfully!')
        else:
            messages.info(request, 'No favicon to delete.')
            
    except Exception as e:
        messages.error(request, f'Error deleting favicon: {str(e)}')
    
    return redirect('common:application_settings')


@login_required
@require_http_methods(["POST"])
def delete_apple_touch_icon(request):
    """Delete current apple touch icon"""
    try:
        settings_obj = ApplicationSettings.get_settings()
        
        if settings_obj.apple_touch_icon:
            # Delete the file from storage
            if default_storage.exists(settings_obj.apple_touch_icon.name):
                default_storage.delete(settings_obj.apple_touch_icon.name)
            
            # Clear the field
            settings_obj.apple_touch_icon = None
            settings_obj.save()
            
            messages.success(request, 'Apple touch icon deleted successfully!')
        else:
            messages.info(request, 'No apple touch icon to delete.')
            
    except Exception as e:
        messages.error(request, f'Error deleting apple touch icon: {str(e)}')
    
    return redirect('common:application_settings')


@login_required
@require_http_methods(["POST"])
def load_default_roles_permissions(request):
    """Load default roles and permissions system"""
    # All authenticated users can access this functionality
    
    try:
        # Try the management command first
        from django.core.management import call_command
        from io import StringIO
        import sys
        
        # Capture the output from the management command
        output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        
        try:
            call_command('setup_user_roles', verbosity=2)
            command_output = output.getvalue()
            sys.stdout = old_stdout
            
            messages.success(
                request, 
                f'Default roles and permissions loaded successfully! '
                f'Command output: {command_output}'
            )
            
        except Exception as cmd_error:
            sys.stdout = old_stdout
            messages.error(
                request, 
                f'Management command failed: {str(cmd_error)}. '
                f'Trying direct creation method...'
            )
            
            # Fallback: Try direct creation
            try:
                direct_result = create_roles_permissions_directly(request.user)
                messages.success(
                    request, 
                    f'Default roles and permissions created directly! '
                    f'Result: {direct_result}'
                )
            except Exception as direct_error:
                messages.error(
                    request, 
                    f'Both methods failed. Management command error: {str(cmd_error)}. '
                    f'Direct creation error: {str(direct_error)}'
                )
        
    except Exception as e:
        messages.error(
            request, 
            f'Error loading default roles and permissions: {str(e)}. '
            'Please check the logs for more details.'
        )
    
    return redirect('common:application_settings')


def create_roles_permissions_directly(user):
    """Direct method to create roles and permissions without management command"""
    from apps.authentication.models import UserRole, Permission, RolePermission, UserRoleAssignment
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    result = []
    
    # Create basic roles
    roles_data = [
        {'role_name': 'Super Admin', 'description': 'Full system access', 'is_system_role': True},
        {'role_name': 'System Administrator', 'description': 'System administration', 'is_system_role': True},
        {'role_name': 'Facility Manager', 'description': 'Can manage facilities', 'is_system_role': True},
        {'role_name': 'Data Analyst', 'description': 'Can view analytics', 'is_system_role': True},
        {'role_name': 'Regular User', 'description': 'Basic user access', 'is_system_role': True},
        {'role_name': 'Content Manager', 'description': 'Can manage documents', 'is_system_role': True}
    ]
    
    roles_created = 0
    for role_data in roles_data:
        role, created = UserRole.objects.get_or_create(
            role_name=role_data['role_name'],
            defaults=role_data
        )
        if created:
            roles_created += 1
            result.append(f'Created role: {role.role_name}')
    
    # Create basic permissions
    permissions_data = [
        {'permission_name': 'view_users', 'resource_name': 'users', 'action_name': 'view', 'description': 'Can view users'},
        {'permission_name': 'add_users', 'resource_name': 'users', 'action_name': 'add', 'description': 'Can add users'},
        {'permission_name': 'change_users', 'resource_name': 'users', 'action_name': 'change', 'description': 'Can change users'},
        {'permission_name': 'delete_users', 'resource_name': 'users', 'action_name': 'delete', 'description': 'Can delete users'},
        {'permission_name': 'view_facilities', 'resource_name': 'facilities', 'action_name': 'view', 'description': 'Can view facilities'},
        {'permission_name': 'add_facilities', 'resource_name': 'facilities', 'action_name': 'add', 'description': 'Can add facilities'},
        {'permission_name': 'change_facilities', 'resource_name': 'facilities', 'action_name': 'change', 'description': 'Can change facilities'},
        {'permission_name': 'delete_facilities', 'resource_name': 'facilities', 'action_name': 'delete', 'description': 'Can delete facilities'},
    ]
    
    permissions_created = 0
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            permission_name=perm_data['permission_name'],
            defaults=perm_data
        )
        if created:
            permissions_created += 1
            result.append(f'Created permission: {permission.permission_name}')
    
    # Assign all permissions to Super Admin role
    try:
        super_admin_role = UserRole.objects.get(role_name='Super Admin')
        all_permissions = Permission.objects.all()
        role_perms_created = 0
        
        for permission in all_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=super_admin_role,
                permission=permission,
                defaults={'granted_by': user}
            )
            if created:
                role_perms_created += 1
        
        result.append(f'Assigned {role_perms_created} permissions to Super Admin role')
        
    except Exception as e:
        result.append(f'Error assigning permissions: {str(e)}')
    
    result.append(f'Summary: Created {roles_created} roles, {permissions_created} permissions')
    return '; '.join(result)
