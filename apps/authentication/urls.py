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
    
    # User management views
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('analytics/', views.user_analytics, name='user_analytics'),
]
