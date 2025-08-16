# -*- encoding: utf-8 -*-
"""
Views for authentication app
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User, UserLocation, UserSession, ResetToken
from .forms import LoginForm, SignUpForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .backends import create_user_session, CustomUserBackend
from apps.facilities.models import Facility
import hashlib


def login_view(request):
    """
    Custom login view using email-based authentication
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                # Create user session
                user_session = create_user_session(user, request)
                
                # Set session data
                request.session['user_id'] = user.user_id
                request.session['user_email'] = user.email
                request.session['user_name'] = user.full_name
                request.session['session_id'] = user_session.session_id
                
                messages.success(request, f'Welcome back, {user.full_name}!')
                
                # Redirect to next page or home
                next_page = request.GET.get('next', '/')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid credentials')
        else:
            # Form has errors, they will be displayed in the template
            pass
    else:
        form = LoginForm()
    
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
    
    # Clear session
    request.session.flush()
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/login/')


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
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        try:
            reset_token = ResetToken.objects.get(
                token_hash=token_hash,
                used=False,
                expires_at__gt=timezone.now()
            )
            form = PasswordResetConfirmForm(token=token)
        except ResetToken.DoesNotExist:
            messages.error(request, 'Invalid or expired reset token.')
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


# Custom login required decorator that works with our custom User model
def custom_login_required(view_func):
    """
    Custom login required decorator for our custom authentication system
    """
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        
        try:
            user = User.objects.get(user_id=user_id, is_active=True)
            request.user = user
        except User.DoesNotExist:
            request.session.flush()
            return redirect('/login/')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


@custom_login_required
def user_list(request):
    """List all users with comprehensive data"""
    users = User.objects.filter(is_active=True).select_related('facility').order_by('full_name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Filter by facility
    facility_id = request.GET.get('facility')
    if facility_id:
        users = users.filter(facility_id=facility_id)
    
    # Get statistics
    active_users_count = users.count()
    users_with_facilities = users.filter(facility__isnull=False).count()
    total_sessions = UserSession.objects.filter(expires_at__gt=timezone.now()).count()
    
    # Get filter options
    facilities = Facility.objects.filter(active_status=True).order_by('facility_name')
    
    context = {
        'users': users,
        'search_query': search_query,
        'selected_facility': facility_id,
        'active_users_count': active_users_count,
        'users_with_facilities': users_with_facilities,
        'total_sessions': total_sessions,
        'facilities': facilities,
    }
    
    return render(request, 'authentication/user_list.html', context)


@custom_login_required
def user_detail(request, user_id):
    """Show user details with all related data"""
    user = get_object_or_404(
        User.objects.select_related('facility__ward__constituency__county'),
        user_id=user_id, 
        is_active=True
    )
    
    # Get related data efficiently
    locations = user.userlocation_set.select_related('ward__constituency__county').order_by('-captured_at')[:10]
    sessions = user.usersession_set.order_by('-created_at')[:10]
    
    # Get user statistics
    total_locations = user.userlocation_set.count()
    total_sessions = user.usersession_set.count()
    active_sessions = user.usersession_set.filter(expires_at__gt=timezone.now()).count()
    
    context = {
        'user': user,
        'locations': locations,
        'sessions': sessions,
        'total_locations': total_locations,
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
    }
    
    return render(request, 'authentication/user_detail.html', context)


@custom_login_required
def user_analytics(request):
    """Show user analytics and statistics"""
    total_users = User.objects.filter(is_active=True).count()
    active_sessions = UserSession.objects.filter(expires_at__gt=timezone.now()).count()
    
    # Get users by facility
    users_by_facility = User.objects.filter(
        is_active=True, 
        facility__isnull=False
    ).values('facility__facility_name').annotate(
        user_count=Count('user_id')
    ).order_by('-user_count')[:10]
    
    # Get users by county
    users_by_county = User.objects.filter(
        is_active=True,
        facility__ward__constituency__county__isnull=False
    ).values('facility__ward__constituency__county__county_name').annotate(
        user_count=Count('user_id')
    ).order_by('-user_count')[:10]
    
    # Get recent user activity
    recent_locations = UserLocation.objects.select_related(
        'user', 'ward__constituency__county'
    ).order_by('-captured_at')[:10]
    
    context = {
        'total_users': total_users,
        'active_sessions': active_sessions,
        'users_by_facility': users_by_facility,
        'users_by_county': users_by_county,
        'recent_locations': recent_locations,
    }
    
    return render(request, 'authentication/user_analytics.html', context)
