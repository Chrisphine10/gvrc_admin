import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

User = get_user_model()
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log API requests
    """
    
    def process_request(self, request):
        if request.path.startswith('/api/'):
            user = getattr(request, 'user', None)
            user_info = f"User: {user.email}" if user and hasattr(user, 'email') else "Anonymous"
            
            logger.info(
                f"API Request - Method: {request.method}, "
                f"Path: {request.path}, "
                f"{user_info}, "
                f"IP: {self.get_client_ip(request)}"
            )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SessionTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track user sessions and locations
    """
    
    def process_request(self, request):
        if request.user.is_authenticated and request.path.startswith('/api/'):
            # Track session information
            from facilities.models import UserSession
            import uuid
            from datetime import datetime, timedelta
            
            # Get or create session
            session_id = request.session.get('api_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['api_session_id'] = session_id
                
                # Create UserSession record
                UserSession.objects.get_or_create(
                    session_id=session_id,
                    defaults={
                        'user': request.user,
                        'ip_address': self.get_client_ip(request),
                        'expires_at': datetime.now() + timedelta(hours=24)
                    }
                )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RateLimitMiddleware(MiddlewareMixin):
    """
    Simple rate limiting middleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
        super().__init__(get_response)
    
    def process_request(self, request):
        if request.path.startswith('/api/'):
            ip = self.get_client_ip(request)
            current_time = int(time.time() / 60)  # Per minute
            
            key = f"{ip}:{current_time}"
            
            if key in self.request_counts:
                self.request_counts[key] += 1
            else:
                self.request_counts[key] = 1
                # Clean old entries
                self.cleanup_old_entries(current_time)
            
            # Rate limit: 100 requests per minute per IP
            if self.request_counts[key] > 100:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Please try again later.'},
                    status=429
                )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def cleanup_old_entries(self, current_time):
        keys_to_remove = []
        for key in self.request_counts:
            key_time = int(key.split(':')[1])
            if current_time - key_time > 5:  # Remove entries older than 5 minutes
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.request_counts[key]