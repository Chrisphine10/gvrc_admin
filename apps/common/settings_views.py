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
    # Only superusers can access this functionality
    if not request.user.is_superuser:
        raise PermissionDenied("Only superusers can load default roles and permissions.")
    
    try:
        # Call the management command to set up roles and permissions
        call_command('setup_user_roles', verbosity=0)
        
        messages.success(
            request, 
            'Default roles and permissions loaded successfully! '
            'All system roles, permissions, and assignments have been created/updated.'
        )
        
    except Exception as e:
        messages.error(
            request, 
            f'Error loading default roles and permissions: {str(e)}. '
            'Please check the logs for more details.'
        )
    
    return redirect('common:application_settings')
