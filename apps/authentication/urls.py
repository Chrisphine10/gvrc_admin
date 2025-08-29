# -*- encoding: utf-8 -*-
"""
URL patterns for authentication app
"""

from django.urls import path
from . import views

# Note: No app_name so URLs are available globally (e.g., 'login' instead of 'authentication:login')

urlpatterns = [
    # Authentication views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password reset views
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/confirm/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
    
    # Profile views
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # User management views
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('analytics/', views.user_analytics, name='user_analytics'),
    
    # Role management views
    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/<int:role_id>/', views.role_detail, name='role_detail'),
    path('roles/<int:role_id>/edit/', views.role_edit, name='role_edit'),
    path('roles/<int:role_id>/delete/', views.role_delete, name='role_delete'),
    
    # Permission management views
    path('permissions/', views.permission_list, name='permission_list'),
    path('permissions/create/', views.permission_create, name='permission_create'),
    path('permissions/<int:permission_id>/edit/', views.permission_edit, name='permission_edit'),
    path('permissions/<int:permission_id>/delete/', views.permission_delete, name='permission_delete'),
    
    # AJAX endpoints for role and permission management
    path('roles/<int:role_id>/assign-permission/', views.assign_permission_to_role, name='assign_permission_to_role'),
    path('roles/<int:role_id>/remove-permission/<int:permission_id>/', views.remove_permission_from_role, name='remove_permission_from_role'),
    path('users/<int:user_id>/assign-role/', views.assign_role_to_user, name='assign_role_to_user'),
    path('users/<int:user_id>/remove-role/<int:role_id>/', views.remove_role_from_user, name='remove_role_from_user'),
]
