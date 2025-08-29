# -*- encoding: utf-8 -*-
"""
Custom authentication middleware for GVRC Admin
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import User


class CustomAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to set request.user based on custom authentication
    """
    
    def process_request(self, request):
        """
        Set request.user based on session data
        """
        # Skip if user is already set (e.g., by decorator)
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            return None
            
        user_id = request.session.get('user_id')
        
        if user_id:
            try:
                user = User.objects.get(user_id=user_id, is_active=True)
                request.user = user
                # Add convenience properties to match Django User model
                request.user.is_authenticated = True
                request.user.is_anonymous = False
            except User.DoesNotExist:
                request.user = AnonymousUser()
                # Clear invalid session
                request.session.flush()
        else:
            request.user = AnonymousUser()
        
        return None
