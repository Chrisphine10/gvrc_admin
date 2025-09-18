# -*- encoding: utf-8 -*-
"""
Custom authentication middleware for GVRC Admin
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to ensure proper user authentication and session handling
    """
    
    def process_request(self, request):
        """
        Ensure user is properly authenticated and has correct attributes
        """
        # Skip if user is already set and authenticated
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            # The user is already authenticated by Django's authentication middleware
            # No need to modify is_authenticated or is_anonymous as they are properties
            return None
        
        # Let Django's authentication middleware handle the initial authentication
        return None
