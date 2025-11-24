# -*- encoding: utf-8 -*-
"""
Context processors for common app
"""

from .models import ApplicationSettings


def chat_notifications(request):
    """
    Add chat notifications to template context
    """
    if not request.user.is_authenticated:
        return {'chat_notifications': []}
    
    try:
        from apps.chat.models import ChatNotification
        notifications = ChatNotification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')[:10]  # Limit to 10 most recent unread notifications
        
        return {
            'chat_notifications': notifications,
            'unread_chat_count': notifications.count(),
        }
    except Exception:
        # Return empty list if there's any error
        return {
            'chat_notifications': [],
            'unread_chat_count': 0,
        }


def application_settings(request):
    """
    Add application settings to template context
    """
    try:
        settings = ApplicationSettings.get_settings()
        return {
            'app_settings': settings,
            'theme_css_variables': settings.get_theme_css_variables(),
        }
    except Exception:
        # Return default values if settings can't be loaded
        return {
            'app_settings': None,
            'theme_css_variables': {
                '--primary-color': '#5e72e4',
                '--secondary-color': '#8392ab',
                '--success-color': '#2dce89',
                '--warning-color': '#fb6340',
                '--danger-color': '#f5365c',
                '--info-color': '#11cdef',
                '--dark-color': '#212529',
                '--light-color': '#f8f9fe',
            },
        }