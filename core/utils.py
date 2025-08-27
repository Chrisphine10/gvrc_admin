import json
import logging
from functools import wraps
from django.http import JsonResponse

logger = logging.getLogger('myproject')

def handle_errors(view_func):
    """Decorator for consistent error handling"""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Unhandled error in {view_func.__name__}: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error'
            }, status=500)
    return wrapper

def validate_json(request_body):
    """Validate and parse JSON request body"""
    try:
        return json.loads(request_body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f'JSON validation error: {str(e)}')
        raise json.JSONDecodeError(f'Invalid JSON: {str(e)}', '', 0)

def log_api_request(request, response_data=None):
    """Log API requests for monitoring"""
    logger.info(f'API Request: {request.method} {request.path} - User: {getattr(request.user, "username", "Anonymous")}')
    if response_data:
        logger.debug(f'Response data: {response_data}')
