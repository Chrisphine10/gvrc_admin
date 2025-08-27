# apps/health/views.py (Health check endpoints)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.core.cache import cache
import logging
import time

logger = logging.getLogger('myproject')


@require_http_methods(["GET"])
def health_check(request):
    """Basic health check endpoint"""
    try:
        return JsonResponse({
            'status': 'healthy',
            'timestamp': time.time(),
            'service': 'myproject-api'
        })
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def health_detailed(request):
    """Detailed health check with database and Redis/cache status"""
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'service': 'myproject-api',
        'checks': {}
    }

    overall_status = 200

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = {
            'status': 'healthy',
            'response_time_ms': 0  # TODO: measure query time if needed
        }
    except Exception as e:
        logger.error(f'Database health check failed: {str(e)}')
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        overall_status = 503

    # Redis / Cache check
    try:
        cache.set('health_check', 'test', timeout=10)
        cached_value = cache.get('health_check')
        cache.delete('health_check')

        if cached_value == 'test':
            health_status['checks']['redis'] = {'status': 'healthy'}
        else:
            health_status['checks']['redis'] = {
                'status': 'unhealthy',
                'error': 'Cache test failed'
            }
            overall_status = 503
    except Exception as e:
        # Gracefully handle missing Redis or cache backend issues
        logger.error(f'Redis health check failed: {str(e)}')
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        overall_status = 503

    # Update overall status
    if overall_status != 200:
        health_status['status'] = 'unhealthy'

    return JsonResponse(health_status, status=overall_status)
