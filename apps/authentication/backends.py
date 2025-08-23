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
import logging
import traceback

# Set up logger for authentication backend
logger = logging.getLogger(__name__)


class CustomUserBackend(BaseBackend):
    """
    Custom authentication backend for email-based authentication
    """
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate user using email and password
        """
        if email is None or password is None:
            logger.debug("Authentication attempt with missing email or password")
            return None
        
        try:
            logger.debug(f"Attempting to authenticate user with email: {email}")
            user = User.objects.get(email=email, is_active=True)
            
            if user.check_password(password):
                logger.info(f"Password verification successful for user: {email}")
                return user
            else:
                logger.warning(f"Password verification failed for user: {email}")
                return None
                
        except User.DoesNotExist:
            logger.warning(f"Authentication failed - User not found or inactive: {email}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during authentication for {email}: {str(e)}")
            return None
        
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            user = User.objects.get(user_id=user_id, is_active=True)
            logger.debug(f"Retrieved user by ID: {user_id}")
            return user
        except User.DoesNotExist:
            logger.warning(f"User not found or inactive for ID: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving user by ID {user_id}: {str(e)}")
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
    try:
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
        
        logger.debug(f"Creating user session for user: {user.email} from IP: {ip_address}")
        
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
        
        logger.info(f"User session created successfully: {session_id} for user: {user.email}")
        return user_session
        
    except Exception as e:
        logger.error(f"Failed to create user session for {user.email}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


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


class AuthenticationErrorMiddleware:
    """
    Middleware to capture and log authentication-related errors
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Log authentication-related exceptions
        """
        if hasattr(request, 'path') and 'login' in request.path:
            self.logger.error(f"Authentication error on {request.path}: {str(exception)}")
            self.logger.error(f"User agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
            self.logger.error(f"IP address: {request.META.get('REMOTE_ADDR', 'Unknown')}")
        
        return None