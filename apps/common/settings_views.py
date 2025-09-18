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
    
    context = {
        'form': form,
        'settings': settings_obj,
        'segment': 'settings',
        'page_title': 'Application Settings',
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
    debug_info = []
    
    try:
        # Test database connection first
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        debug_info.append("✓ Database connection: OK")
        
        # Test model imports
        from apps.authentication.models import UserRole, Permission, RolePermission
        debug_info.append("✓ Model imports: OK")
        
        # Test current state
        initial_roles = UserRole.objects.count()
        initial_permissions = Permission.objects.count()
        debug_info.append(f"✓ Initial state: {initial_roles} roles, {initial_permissions} permissions")
        
        # Create system roles
        roles_data = [
            {'role_name': 'Super Admin', 'description': 'Full system access with all permissions', 'is_system_role': True},
            {'role_name': 'System Administrator', 'description': 'System administration with user and role management', 'is_system_role': True},
            {'role_name': 'Facility Manager', 'description': 'Can manage facilities and related data', 'is_system_role': True},
            {'role_name': 'Data Analyst', 'description': 'Can view analytics and reports', 'is_system_role': True},
            {'role_name': 'Regular User', 'description': 'Basic user access to view data', 'is_system_role': True},
            {'role_name': 'Content Manager', 'description': 'Can manage documents and content', 'is_system_role': True}
        ]
        
        roles_created = 0
        for i, role_data in enumerate(roles_data):
            try:
                role, created = UserRole.objects.get_or_create(
                    role_name=role_data['role_name'],
                    defaults=role_data
                )
                if created:
                    roles_created += 1
                    debug_info.append(f"✓ Created role: {role.role_name}")
                else:
                    debug_info.append(f"- Role already exists: {role.role_name}")
            except Exception as role_error:
                debug_info.append(f"✗ Error creating role {role_data['role_name']}: {str(role_error)}")
        
        # Create system permissions
        permissions_data = [
            # User management permissions
            {'permission_name': 'view_users', 'resource_name': 'users', 'action_name': 'view', 'description': 'Can view user list and details'},
            {'permission_name': 'add_users', 'resource_name': 'users', 'action_name': 'add', 'description': 'Can create new users'},
            {'permission_name': 'change_users', 'resource_name': 'users', 'action_name': 'change', 'description': 'Can edit user information'},
            {'permission_name': 'delete_users', 'resource_name': 'users', 'action_name': 'delete', 'description': 'Can delete users'},
            
            # Role management permissions
            {'permission_name': 'view_roles', 'resource_name': 'roles', 'action_name': 'view', 'description': 'Can view roles and permissions'},
            {'permission_name': 'add_roles', 'resource_name': 'roles', 'action_name': 'add', 'description': 'Can create new roles'},
            {'permission_name': 'change_roles', 'resource_name': 'roles', 'action_name': 'change', 'description': 'Can edit roles and permissions'},
            {'permission_name': 'delete_roles', 'resource_name': 'roles', 'action_name': 'delete', 'description': 'Can delete roles'},
            
            # Facility management permissions
            {'permission_name': 'view_facilities', 'resource_name': 'facilities', 'action_name': 'view', 'description': 'Can view facilities'},
            {'permission_name': 'add_facilities', 'resource_name': 'facilities', 'action_name': 'add', 'description': 'Can create new facilities'},
            {'permission_name': 'change_facilities', 'resource_name': 'facilities', 'action_name': 'change', 'description': 'Can edit facility information'},
            {'permission_name': 'delete_facilities', 'resource_name': 'facilities', 'action_name': 'delete', 'description': 'Can delete facilities'},
            
            # Analytics permissions
            {'permission_name': 'view_analytics', 'resource_name': 'analytics', 'action_name': 'view', 'description': 'Can view analytics and reports'},
            
            # Document management permissions
            {'permission_name': 'view_documents', 'resource_name': 'documents', 'action_name': 'view', 'description': 'Can view documents'},
            {'permission_name': 'add_documents', 'resource_name': 'documents', 'action_name': 'add', 'description': 'Can upload documents'},
            {'permission_name': 'change_documents', 'resource_name': 'documents', 'action_name': 'change', 'description': 'Can edit documents'},
            {'permission_name': 'delete_documents', 'resource_name': 'documents', 'action_name': 'delete', 'description': 'Can delete documents'},
            
            # Admin permissions
            {'permission_name': 'view_admin', 'resource_name': 'admin', 'action_name': 'view', 'description': 'Can access admin interface'},
            {'permission_name': 'manage_system', 'resource_name': 'system', 'action_name': 'manage', 'description': 'Can manage system settings'},
        ]
        
        permissions_created = 0
        for i, perm_data in enumerate(permissions_data):
            try:
                permission, created = Permission.objects.get_or_create(
                    permission_name=perm_data['permission_name'],
                    defaults=perm_data
                )
                if created:
                    permissions_created += 1
                    debug_info.append(f"✓ Created permission: {permission.permission_name}")
                else:
                    debug_info.append(f"- Permission already exists: {permission.permission_name}")
            except Exception as perm_error:
                debug_info.append(f"✗ Error creating permission {perm_data['permission_name']}: {str(perm_error)}")
        
        # Assign all permissions to Super Admin role
        role_permissions_created = 0
        try:
            super_admin_role = UserRole.objects.get(role_name='Super Admin')
            all_permissions = Permission.objects.all()
            
            for permission in all_permissions:
                try:
                    role_perm, created = RolePermission.objects.get_or_create(
                        role=super_admin_role,
                        permission=permission,
                        defaults={'granted_by': request.user}
                    )
                    if created:
                        role_permissions_created += 1
                except Exception as rp_error:
                    debug_info.append(f"✗ Error assigning permission {permission.permission_name}: {str(rp_error)}")
            
            debug_info.append(f"✓ Assigned {role_permissions_created} permissions to Super Admin role")
            
        except UserRole.DoesNotExist:
            debug_info.append("✗ Super Admin role not found for permission assignment")
        
        # Final state
        final_roles = UserRole.objects.count()
        final_permissions = Permission.objects.count()
        debug_info.append(f"✓ Final state: {final_roles} roles, {final_permissions} permissions")
        
        messages.success(
            request, 
            f'Success! Created {roles_created} roles, {permissions_created} permissions, '
            f'and {role_permissions_created} role-permission assignments.<br><br>'
            f'<strong>Debug Info:</strong><br>' + '<br>'.join(debug_info)
        )
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        messages.error(
            request, 
            f'Error creating roles and permissions: {str(e)}<br><br>'
            f'<strong>Debug Info:</strong><br>' + '<br>'.join(debug_info) + '<br><br>'
            f'<strong>Full Error:</strong><br><pre>{error_details}</pre>'
        )
    
    return redirect('common:application_settings')


@login_required
@require_http_methods(["POST"])
def test_roles_permissions(request):
    """Test current roles and permissions state"""
    try:
        from apps.authentication.models import UserRole, Permission, RolePermission
        
        # Get counts
        roles_count = UserRole.objects.count()
        permissions_count = Permission.objects.count()
        role_permissions_count = RolePermission.objects.count()
        
        # Get role names
        role_names = list(UserRole.objects.values_list('role_name', flat=True))
        
        # Get permission names (first 10)
        permission_names = list(Permission.objects.values_list('permission_name', flat=True)[:10])
        
        # Check Super Admin role
        super_admin_info = "Not found"
        try:
            super_admin = UserRole.objects.get(role_name='Super Admin')
            super_admin_perms = RolePermission.objects.filter(role=super_admin).count()
            super_admin_info = f"Exists with {super_admin_perms} permissions"
        except UserRole.DoesNotExist:
            pass
        
        messages.info(
            request,
            f'<strong>Current State:</strong><br>'
            f'Roles: {roles_count} ({", ".join(role_names) if role_names else "None"})<br>'
            f'Permissions: {permissions_count} ({", ".join(permission_names) if permission_names else "None"})<br>'
            f'Role-Permissions: {role_permissions_count}<br>'
            f'Super Admin: {super_admin_info}'
        )
        
    except Exception as e:
        messages.error(request, f'Error testing state: {str(e)}')
    
    return redirect('common:application_settings')
