# -*- encoding: utf-8 -*-
"""
Views for authentication app
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, IntegrityError
from django.contrib.auth import authenticate, login
import logging
import traceback
import json
from .models import User, UserSession, UserRole, Permission, UserRoleAssignment, UserProfile
from .forms import LoginForm, SignUpForm, PasswordResetRequestForm, PasswordResetConfirmForm, ProfileEditForm, PasswordChangeForm
from .backends import create_user_session, CustomUserBackend
from apps.facilities.models import Facility
import hashlib
import json

# Set up logger for authentication
logger = logging.getLogger(__name__)


def login_view(request):
    """
    Custom login view using email-based authentication with comprehensive error logging
    """
    logger.info(f"Login attempt from IP: {request.META.get('REMOTE_ADDR', 'Unknown')}")
    
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                try:
                    user = form.get_user()
                    if user:
                        # Log successful authentication
                        logger.info(f"Successful login for user: {user.email} (ID: {user.user_id})")
                        
                        # Check if user is active
                        if not user.is_active:
                            logger.warning(f"Login attempt for inactive user: {user.email}")
                            messages.error(request, 'Your account has been deactivated. Please contact an administrator.')
                            return render(request, 'accounts/login.html', {
                                'form': form,
                                'msg': 'Account deactivated'
                            })
                        
                        # Check if user is staff (for admin access)
                        if not user.is_staff:
                            logger.warning(f"Non-staff user login attempt: {user.email}")
                            messages.warning(request, 'You do not have administrative privileges.')
                        
                        try:
                            # Create user session for tracking
                            user_session = create_user_session(user, request)
                            logger.debug(f"User session created: {user_session.session_id}")
                        except Exception as session_error:
                            logger.error(f"Failed to create user session for {user.email}: {str(session_error)}")
                            # Continue with login even if session creation fails
                        
                        # Use Django's built-in login function
                        login(request, user)
                        
                        # Set additional session data for our custom tracking
                        if user_session:
                            request.session['session_id'] = user_session.session_id
                        
                        messages.success(request, f'Welcome back, {user.full_name}!')
                        logger.info(f"User {user.email} successfully logged in and redirected")
                        
                        # Redirect to next page or dashboard
                        next_page = request.GET.get('next', '/dashboard/')
                        return redirect(next_page)
                    else:
                        logger.warning(f"Invalid credentials for email: {form.cleaned_data.get('email', 'Unknown')}")
                        messages.error(request, 'Invalid email or password. Please try again.')
                except Exception as auth_error:
                    logger.error(f"Authentication error: {str(auth_error)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    messages.error(request, 'An error occurred during authentication. Please try again.')
            else:
                # Form validation errors
                email = form.data.get('email', 'Unknown')
                logger.warning(f"Form validation failed for email: {email}")
                logger.debug(f"Form errors: {form.errors}")
                
                # Check for specific validation errors
                if 'email' in form.errors:
                    messages.error(request, 'Please enter a valid email address.')
                elif 'password' in form.errors:
                    messages.error(request, 'Password is required.')
                else:
                    messages.error(request, 'Please correct the errors below.')
                    
        except ValidationError as ve:
            logger.error(f"Validation error in login form: {str(ve)}")
            messages.error(request, 'Invalid form data. Please check your input.')
        except DatabaseError as db_error:
            logger.error(f"Database error during login: {str(db_error)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            messages.error(request, 'A system error occurred. Please try again later.')
        except IntegrityError as ie:
            logger.error(f"Integrity error during login: {str(ie)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            messages.error(request, 'A system error occurred. Please try again later.')
        except PermissionDenied as pd:
            logger.error(f"Permission denied during login: {str(pd)}")
            messages.error(request, 'Access denied. Please contact an administrator.')
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            messages.error(request, 'An unexpected error occurred. Please try again later.')
    else:
        form = LoginForm()
        logger.debug("Login page accessed")
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'msg': None
    })


def register_view(request):
    """
    Custom registration view
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                f'Account created successfully for {user.full_name}! You can now <a href="{reverse("login")}">sign in</a>.'
            )
            return render(request, 'accounts/register.html', {
                'form': SignUpForm(),  # Reset form
                'success': True,
                'msg': f'Account created successfully for {user.full_name}! You can now <a href="{reverse("login")}">sign in</a>.'
            })
        else:
            # Form has errors, they will be displayed in the template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'success': False,
        'msg': None
    })


def logout_view(request):
    """
    Custom logout view
    """
    # Get current session and mark it as expired
    session_id = request.session.get('session_id')
    if session_id:
        try:
            user_session = UserSession.objects.get(session_id=session_id)
            user_session.expires_at = timezone.now()
            user_session.save()
        except UserSession.DoesNotExist:
            pass
    
    # Use Django's built-in logout function
    from django.contrib.auth import logout
    logout(request)
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')


def password_reset_view(request):
    """
    Password reset request view
    """
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            token, reset_token = form.create_reset_token()
            
            if token and reset_token:
                # Send reset email (for now, just show a message)
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'token': token})
                )
                
                # In a real app, you would send an email here
                # For demo purposes, we'll just show a success message with the link
                messages.success(
                    request,
                    f'Password reset link has been generated. '
                    f'<a href="{reset_url}" target="_blank">Click here to reset your password</a>'
                )
                
                return render(request, 'accounts/password_reset_done.html', {
                    'reset_url': reset_url  # For demo purposes
                })
            else:
                messages.error(request, 'Failed to create reset token.')
        else:
            # Form has errors
            pass
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset.html', {
        'form': form
    })


def password_reset_confirm_view(request, token):
    """
    Password reset confirmation view
    """
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST, token=token)
        if form.is_valid():
            user = form.save()
            if user:
                messages.success(
                    request,
                    f'Password reset successful for {user.full_name}! '
                    f'You can now <a href="{reverse("login")}">sign in</a> with your new password.'
                )
                return render(request, 'accounts/password_reset_complete.html')
            else:
                messages.error(request, 'Failed to reset password.')
        else:
            # Form has errors
            pass
    else:
        # Validate token first
        # Note: ResetToken functionality needs to be implemented with the new schema
        messages.error(request, 'Password reset functionality is being updated.')
        return redirect('password_reset')
    
    return render(request, 'accounts/password_reset_confirm.html', {
        'form': form,
        'token': token
    })


def password_reset_done_view(request):
    """
    Password reset done view
    """
    return render(request, 'accounts/password_reset_done.html')


def password_reset_complete_view(request):
    """
    Password reset complete view
    """
    return render(request, 'accounts/password_reset_complete.html')


# Custom login required decorator that works with Django's authentication system
def custom_login_required(view_func):
    """
    Custom login required decorator that works with Django's authentication system
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


@custom_login_required
def user_list(request):
    """List all users with comprehensive data"""
    users = User.objects.filter(is_active=True).order_by('full_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Get statistics
    active_users_count = users.count()
    total_sessions = UserSession.objects.filter(expires_at__gt=timezone.now()).count()
    
    context = {
        'users': users,
        'search_query': search_query,
        'active_users_count': active_users_count,
        'total_sessions': total_sessions,
    }
    
    return render(request, 'authentication/user_list.html', context)


@custom_login_required
def user_detail(request, user_id):
    """Show user details with all related data"""
    user = get_object_or_404(
        User.objects.select_related(),
        user_id=user_id, 
        is_active=True
    )
    
    # Get related data efficiently
    sessions = user.usersession_set.order_by('-created_at')[:10]
    
    # Get user statistics
    total_sessions = user.usersession_set.count()
    active_sessions = user.usersession_set.filter(expires_at__gt=timezone.now()).count()
    
    context = {
        'user': user,
        'sessions': sessions,
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
    }
    
    return render(request, 'authentication/user_detail.html', context)


@custom_login_required
def user_analytics(request):
    """Show user analytics and statistics"""
    total_users = User.objects.filter(is_active=True).count()
    active_sessions = UserSession.objects.filter(expires_at__gt=timezone.now()).count()
    
    # Get users by facility (placeholder for future implementation)
    users_by_facility = []
    
    # Get users by county (placeholder for future implementation)
    users_by_county = []
    
    # Get recent user activity
    # Note: UserLocation functionality needs to be implemented with the new schema
    recent_locations = []
    
    context = {
        'total_users': total_users,
        'active_sessions': active_sessions,
        'users_by_facility': users_by_facility,
        'users_by_county': users_by_county,
        'recent_locations': recent_locations,
    }
    
    return render(request, 'authentication/user_analytics.html', context)


@custom_login_required
def profile_view(request):
    """User profile view - allows viewing and editing profile information"""
    user = request.user
    
    if request.method == 'POST':
        if 'profile_form' in request.POST:
            # Handle profile update
            form = ProfileEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        elif 'password_form' in request.POST:
            # Handle password change
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password changed successfully! Please log in again with your new password.')
                return redirect('logout')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = ProfileEditForm(instance=user)
        password_form = PasswordChangeForm(user)
    
    # Get or create user profile
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    except AttributeError:
        # Handle case where userprofile relationship doesn't exist yet
        profile = None
    
    context = {
        'user': user,
        'profile': profile,
        'form': form,
        'password_form': password_form,
    }
    
    return render(request, 'authentication/profile.html', context)


@custom_login_required
def change_password_view(request):
    """Separate view for changing password"""
    user = request.user
    
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully! Please log in again with your new password.')
            return redirect('logout')
    else:
        form = PasswordChangeForm(user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'authentication/change_password.html', context)


# New views for user role management

@custom_login_required
def role_list(request):
    """List all user roles with their permissions"""
    roles = UserRole.objects.annotate(
        user_count=Count('userroleassignment'),
        permission_count=Count('rolepermission')
    ).order_by('role_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        roles = roles.filter(
            Q(role_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'roles': roles,
        'search_query': search_query,
    }
    
    return render(request, 'authentication/role_list.html', context)


@custom_login_required
def role_detail(request, role_id):
    """Show role details with assigned permissions and users"""
    role = get_object_or_404(UserRole, role_id=role_id)
    
    # Get permissions for this role
    role_permissions = role.rolepermission_set.select_related('permission').order_by('permission__resource_name', 'permission__action_name')
    
    # Get users with this role
    users_with_role = role.userroleassignment_set.select_related('user').order_by('user__full_name')
    
    # Get all available permissions for potential assignment
    all_permissions = Permission.objects.exclude(
        rolepermission__role=role
    ).order_by('resource_name', 'action_name')
    
    context = {
        'role': role,
        'role_permissions': role_permissions,
        'users_with_role': users_with_role,
        'all_permissions': all_permissions,
    }
    
    return render(request, 'authentication/role_detail.html', context)


@custom_login_required
def role_create(request):
    """Create a new user role"""
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        description = request.POST.get('description', '')
        is_system_role = request.POST.get('is_system_role') == 'on'
        
        if role_name:
            try:
                role = UserRole.objects.create(
                    role_name=role_name,
                    description=description,
                    is_system_role=is_system_role
                )
                messages.success(request, f'Role "{role.role_name}" created successfully!')
                return redirect('role_detail', role_id=role.role_id)
            except Exception as e:
                messages.error(request, f'Error creating role: {str(e)}')
        else:
            messages.error(request, 'Role name is required.')
    
    return render(request, 'authentication/role_form.html', {
        'action': 'Create',
        'role': None
    })


@custom_login_required
def role_edit(request, role_id):
    """Edit an existing user role"""
    role = get_object_or_404(UserRole, role_id=role_id)
    
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        description = request.POST.get('description', '')
        is_system_role = request.POST.get('is_system_role') == 'on'
        
        if role_name:
            try:
                role.role_name = role_name
                role.description = description
                role.is_system_role = is_system_role
                role.save()
                messages.success(request, f'Role "{role.role_name}" updated successfully!')
                return redirect('role_detail', role_id=role.role_id)
            except Exception as e:
                messages.error(request, f'Error updating role: {str(e)}')
        else:
            messages.error(request, 'Role name is required.')
    
    return render(request, 'authentication/role_form.html', {
        'action': 'Edit',
        'role': role
    })


@custom_login_required
def role_delete(request, role_id):
    """Delete a user role"""
    role = get_object_or_404(UserRole, role_id=role_id)
    
    if request.method == 'POST':
        try:
            role_name = role.role_name
            role.delete()
            messages.success(request, f'Role "{role_name}" deleted successfully!')
            return redirect('role_list')
        except Exception as e:
            messages.error(request, f'Error deleting role: {str(e)}')
    
    return render(request, 'authentication/role_confirm_delete.html', {
        'role': role
    })


@custom_login_required
def permission_list(request):
    """List all available permissions"""
    permissions = Permission.objects.annotate(
        role_count=Count('rolepermission')
    ).order_by('resource_name', 'action_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        permissions = permissions.filter(
            Q(permission_name__icontains=search_query) |
            Q(resource_name__icontains=search_query) |
            Q(action_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Group by resource
    permissions_by_resource = {}
    for permission in permissions:
        resource = permission.resource_name
        if resource not in permissions_by_resource:
            permissions_by_resource[resource] = []
        permissions_by_resource[resource].append(permission)
    
    context = {
        'permissions': permissions,
        'permissions_by_resource': permissions_by_resource,
        'search_query': search_query,
    }
    
    return render(request, 'authentication/permission_list.html', context)


@custom_login_required
def permission_create(request):
    """Create a new permission"""
    if request.method == 'POST':
        permission_name = request.POST.get('permission_name')
        resource_name = request.POST.get('resource_name')
        action_name = request.POST.get('action_name')
        description = request.POST.get('description', '')
        
        if permission_name and resource_name and action_name:
            try:
                permission = Permission.objects.create(
                    permission_name=permission_name,
                    resource_name=resource_name,
                    action_name=action_name,
                    description=description
                )
                messages.success(request, f'Permission "{permission.permission_name}" created successfully!')
                return redirect('permission_list')
            except Exception as e:
                messages.error(request, f'Error creating permission: {str(e)}')
        else:
            messages.error(request, 'Permission name, resource name, and action name are required.')
    
    return render(request, 'authentication/permission_form.html', {
        'action': 'Create',
        'permission': None
    })


@custom_login_required
def permission_edit(request, permission_id):
    """Edit an existing permission"""
    permission = get_object_or_404(Permission, permission_id=permission_id)
    
    if request.method == 'POST':
        permission_name = request.POST.get('permission_name')
        resource_name = request.POST.get('resource_name')
        action_name = request.POST.get('action_name')
        description = request.POST.get('description', '')
        
        if permission_name and resource_name and action_name:
            try:
                permission.permission_name = permission_name
                permission.resource_name = resource_name
                permission.action_name = action_name
                permission.description = description
                permission.save()
                messages.success(request, f'Permission "{permission.permission_name}" updated successfully!')
                return redirect('permission_list')
            except Exception as e:
                messages.error(request, f'Error updating permission: {str(e)}')
        else:
            messages.error(request, 'Permission name, resource name, and action name are required.')
    
    return render(request, 'authentication/permission_form.html', {
        'action': 'Edit',
        'permission': permission
    })


@custom_login_required
def permission_delete(request, permission_id):
    """Delete a permission"""
    permission = get_object_or_404(Permission, permission_id=permission_id)
    
    if request.method == 'POST':
        try:
            permission_name = permission.permission_name
            permission.delete()
            messages.success(request, f'Permission "{permission_name}" deleted successfully!')
            return redirect('permission_list')
        except Exception as e:
            messages.error(request, f'Error deleting permission: {str(e)}')
    
    return render(request, 'authentication/permission_confirm_delete.html', {
        'permission': permission
    })


@custom_login_required
@require_http_methods(["POST"])
def assign_permission_to_role(request, role_id):
    """Assign a permission to a role via AJAX"""
    try:
        data = json.loads(request.body)
        permission_id = data.get('permission_id')
        
        if not permission_id:
            return JsonResponse({'success': False, 'error': 'Permission ID is required'})
        
        role = get_object_or_404(UserRole, role_id=role_id)
        permission = get_object_or_404(Permission, permission_id=permission_id)
        
        # Check if permission is already assigned
        existing = role.rolepermission_set.filter(permission=permission).first()
        if existing:
            return JsonResponse({'success': False, 'error': 'Permission already assigned to this role'})
        
        # Assign permission
        role.rolepermission_set.create(
            permission=permission,
            granted_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Permission "{permission.permission_name}" assigned to role "{role.role_name}"'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@custom_login_required
@require_http_methods(["POST"])
def remove_permission_from_role(request, role_id, permission_id):
    """Remove a permission from a role via AJAX"""
    try:
        role = get_object_or_404(UserRole, role_id=role_id)
        permission = get_object_or_404(Permission, permission_id=permission_id)
        
        # Remove permission
        role.rolepermission_set.filter(permission=permission).delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Permission "{permission.permission_name}" removed from role "{role.role_name}"'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@custom_login_required
@require_http_methods(["POST"])
def assign_role_to_user(request, user_id):
    """Assign a role to a user via AJAX"""
    try:
        data = json.loads(request.body)
        role_id = data.get('role_id')
        
        if not role_id:
            return JsonResponse({'success': False, 'error': 'Role ID is required'})
        
        user = get_object_or_404(User, user_id=user_id)
        role = get_object_or_404(UserRole, role_id=role_id)
        
        # Check if role is already assigned
        existing = user.userroleassignment_set.filter(role=role).first()
        if existing:
            return JsonResponse({'success': False, 'error': 'User already has this role'})
        
        # Assign role
        user.userroleassignment_set.create(
            role=role,
            assigned_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Role "{role.role_name}" assigned to user "{user.full_name}"'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@custom_login_required
@require_http_methods(["POST"])
def remove_role_from_user(request, user_id, role_id):
    """Remove a role from a user via AJAX"""
    try:
        user = get_object_or_404(User, user_id=user_id)
        role = get_object_or_404(UserRole, role_id=role_id)
        
        # Remove role
        user.userroleassignment_set.filter(role=role).delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Role "{role.role_name}" removed from user "{user.full_name}"'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@custom_login_required
def user_edit(request, user_id):
    """Edit user information"""
    user = get_object_or_404(User, user_id=user_id)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user.full_name}" updated successfully!')
            return redirect('user_detail', user_id=user.user_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=user)
    
    # Get user's current roles
    user_roles = user.userroleassignment_set.select_related('role').order_by('role__role_name')
    
    # Get all available roles for potential assignment
    all_roles = UserRole.objects.exclude(
        userroleassignment__user=user
    ).order_by('role_name')
    
    context = {
        'user': user,
        'form': form,
        'user_roles': user_roles,
        'all_roles': all_roles,
    }
    
    return render(request, 'authentication/user_edit.html', context)
