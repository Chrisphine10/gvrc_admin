import logging
import traceback
import uuid
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger('api_errors')

def custom_exception_handler(exc, context):
    """Custom exception handler for API errors"""
    
    # Generate unique error ID for tracking
    error_id = str(uuid.uuid4())[:8]
    
    # Get the standard error response first
    response = exception_handler(exc, context)
    
    # Build error context
    error_context = {
        'error_id': error_id,
        'path': context['request'].path,
        'method': context['request'].method,
        'user_id': getattr(context['request'].user, 'id', None),
        'error_type': type(exc).__name__,
        'error_message': str(exc),
        'traceback': traceback.format_exc()
    }
    
    if response is not None:
        # Customize response based on exception type
        if isinstance(exc, ValidationError):
            error_response = {
                'status': 'error',
                'error_code': 'VALIDATION_ERROR',
                'error_id': error_id,
                'message': 'Validation failed',
                'details': response.data,
                'timestamp': timezone.now().isoformat()
            }
            
        elif isinstance(exc, PermissionDenied):
            error_response = {
                'status': 'error',
                'error_code': 'PERMISSION_DENIED',
                'error_id': error_id,
                'message': 'You do not have permission to perform this action',
                'timestamp': timezone.now().isoformat()
            }
            
        elif isinstance(exc, IntegrityError):
            error_response = {
                'status': 'error',
                'error_code': 'DATA_INTEGRITY_ERROR',
                'error_id': error_id,
                'message': 'Data integrity constraint violation',
                'timestamp': timezone.now().isoformat()
            }
            
        else:
            error_response = {
                'status': 'error',
                'error_code': 'API_ERROR',
                'error_id': error_id,
                'message': 'An error occurred processing your request',
                'timestamp': timezone.now().isoformat()
            }
        
        # Log error with context
        logger.error('API Error occurred', extra=error_context)
        
        response.data = error_response
    
    else:
        # Handle non-DRF exceptions
        error_response = {
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'error_id': error_id,
            'message': 'Internal server error',
            'timestamp': timezone.now().isoformat()
        }
        
        logger.error('Internal Error occurred', extra=error_context)
        
        response = Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response

class APIExceptionMiddleware:
    """Middleware to catch and handle API exceptions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            if request.path.startswith('/api/'):
                return self.handle_api_exception(exc, request)
            raise
    
    def handle_api_exception(self, exc, request):
        """Handle exceptions for API requests"""
        error_id = str(uuid.uuid4())[:8]
        
        error_context = {
            'error_id': error_id,
            'path': request.path,
            'method': request.method,
            'error_type': type(exc).__name__,
            'error_message': str(exc),
            'traceback': traceback.format_exc()
        }
        
        logger.error('Unhandled API Exception', extra=error_context)
        
        return JsonResponse({
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'error_id': error_id,
            'message': 'An unexpected error occurred',
            'timestamp': timezone.now().isoformat()
        }, status=500)