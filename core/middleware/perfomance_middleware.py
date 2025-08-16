import time
import logging
import threading
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from core.services.cache_service import CacheService

logger = logging.getLogger('performance')

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Monitor API performance and add metrics headers"""
    
    def process_request(self, request):
        """Start performance tracking"""
        request._start_time = time.time()
        request._queries_before = len(connection.queries)
        request._thread_id = threading.get_ident()
    
    def process_response(self, request, response):
        """Add performance metrics to response"""
        if not hasattr(request, '_start_time'):
            return response
        
        # Calculate metrics
        end_time = time.time()
        response_time = (end_time - request._start_time) * 1000
        queries_count = len(connection.queries) - getattr(request, '_queries_before', 0)
        
        # Get cache stats
        cache_stats = CacheService.get_cache_stats()
        
        metrics = {
            'url': request.get_full_path(),
            'method': request.method,
            'response_time_ms': round(response_time, 2),
            'query_count': queries_count,
            'status_code': response.status_code,
            'cache_hit_rate': cache_stats.get('hit_rate', 0),
            'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None
        }
        
        # Log slow requests
        if response_time > 1000:
            logger.warning("Slow request detected", extra=metrics)
        
        # Log all API requests
        if request.path.startswith('/api/'):
            logger.info("API Request", extra=metrics)
        
        # Add performance headers
        response['X-Response-Time'] = f"{metrics['response_time_ms']}ms"
        response['X-Query-Count'] = str(metrics['query_count'])
        response['X-Cache-Hit-Rate'] = f"{metrics['cache_hit_rate']}%"
        
        # Add debug info in development
        if settings.DEBUG:
            response['X-Debug-Queries'] = json.dumps([
                {
                    'sql': query['sql'][:100] + '...' if len(query['sql']) > 100 else query['sql'],
                    'time': query['time']
                }
                for query in connection.queries[-queries_count:] if queries_count > 0
            ])
        
        return response

class CacheMiddleware(MiddlewareMixin):
    """Cache API responses automatically"""
    
    CACHEABLE_METHODS = ['GET']
    CACHE_TTL = 300  # 5 minutes default
    
    def process_request(self, request):
        """Check for cached response"""
        if (request.method in self.CACHEABLE_METHODS and 
            request.path.startswith('/api/') and
            not request.user.is_authenticated):  # Only cache for anonymous users
            
            cache_key = CacheService.generate_key('api', 
                path=request.path,
                query=request.GET.urlencode(),
                method=request.method
            )
            
            cached_response = CacheService.get(cache_key)
            if cached_response:
                response = JsonResponse(cached_response)
                response['X-Cache-Status'] = 'HIT'
                return response
        
        return None
    
    def process_response(self, request, response):
        """Cache successful API responses"""
        if (hasattr(response, 'status_code') and
            response.status_code == 200 and
            request.method in self.CACHEABLE_METHODS and
            request.path.startswith('/api/') and
            not request.user.is_authenticated and
            'application/json' in response.get('Content-Type', '')):
            
            cache_key = CacheService.generate_key('api',
                path=request.path,
                query=request.GET.urlencode(),
                method=request.method
            )
            
            try:
                response_data = response.json() if hasattr(response, 'json') else None
                if response_data:
                    CacheService.set(cache_key, response_data, self.CACHE_TTL)
                    response['X-Cache-Status'] = 'MISS'
            except:
                pass
        
        return response