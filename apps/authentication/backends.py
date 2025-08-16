# -*- encoding: utf-8 -*-
"""
Custom authentication backend for the custom User model
"""

import hashlib
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from .models import User, UserSession
from django.utils import timezone
from datetime import timedelta
import secrets


class CustomUserBackend(BaseBackend):
    """
    Custom authentication backend for email-based authentication
    """
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate user using email and password
        """
        if email is None or password is None:
            return None
        
        try:
            user = User.objects.get(email=email, is_active=True)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if user.password_hash == password_hash:
                return user
        except User.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(user_id=user_id, is_active=True)
        except User.DoesNotExist:
            return None


class SessionMiddleware:
    """
    Middleware to handle custom user sessions
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Create or update user session when user logs in
        """
        if hasattr(request, 'user') and hasattr(request.user, 'user_id'):
            self.create_or_update_session(request)
    
    def create_or_update_session(self, request):
        """
        Create or update a UserSession for the authenticated user
        """
        if not hasattr(request.user, 'user_id'):
            return
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR', '')
        
        # Get or create session
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        # Create or update UserSession
        user_session, created = UserSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                'user': request.user,
                'ip_address': ip_address,
                'created_at': timezone.now(),
                'expires_at': timezone.now() + timedelta(hours=24)
            }
        )
        
        if not created:
            # Update existing session
            user_session.expires_at = timezone.now() + timedelta(hours=24)
            user_session.save()


def create_user_session(user, request):
    """
    Helper function to create a user session
    """
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
    
    # Generate session ID
    session_id = secrets.token_urlsafe(32)
    
    # Create UserSession
    user_session = UserSession.objects.create(
        session_id=session_id,
        user=user,
        ip_address=ip_address,
        created_at=timezone.now(),
        expires_at=timezone.now() + timedelta(hours=24)
    )
    
    return user_session


class CustomTokenAuthentication:
    """
    Custom token authentication for DRF that works with our User model
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth = self.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            return None
        elif len(auth) > 2:
            return None

        try:
            token = auth[1].decode()
        except UnicodeError:
            return None

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        """
        Authenticate the token.
        """
        from .models import CustomToken
        
        try:
            token = CustomToken.objects.select_related('user').get(key=key)
        except CustomToken.DoesNotExist:
            return None

        if not token.user.is_active:
            return None

        return (token.user, token)

    def get_authorization_header(self, request):
        """
        Return request's 'Authorization:' header, as a bytestring.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            auth = auth.encode('iso-8859-1')
        return auth