### 📁 `core/views/health_views.py`
```python
import os
import tempfile
import psutil
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.contrib.auth import get_user_model
from ..models import Post, Category
from ..services.cache_service import CacheService

User = get_user_model()

def health_check(request):
    """Comprehensive health check endpoint"""
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        'storage': check_storage(),
        'system': check_system_resources()
    }
    
    # Overall status
    status_code = 200 if all(check['status'] == 'ok' for check in checks.values()) else 503
    overall_status = 'healthy' if status_code == 200 else 'unhealthy'
    
    return JsonResponse({
        'status': overall_status,
        'timestamp': datetime.now().isoformat(),
        'checks': checks,
        'version': '1.0.0',
        'environment': os.getenv('DJANGO_ENV', 'development')
    }, status=status_code)

def check_database():
    """Check PostgreSQL database connectivity and performance"""
    try:
        start_time = datetime.now()
        
        # Test basic connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        # Test query performance
        cursor.execute("SELECT COUNT(*) FROM auth_user")
        user_count = cursor.fetchone()[0]
        
        query_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Check database size
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size
        """)
        db_size = cursor.fetchone()[0]
        
        return {
            'status': 'ok',
            'message': 'Database connection successful',
            'details': {
                'query_time_ms': round(query_time, 2),
                'user_count': user_count,
                'database_size': db_size
            }
        }
    except Exception as e:
        return {
            'status': 'fail', 
            'message': f'Database connection failed: {str(e)}'
        }

def check_cache():
    """Check Redis cache connectivity and stats"""
    try:
        # Test basic operations
        test_key = 'health_check_test'
        cache.set(test_key, 'ok', 10)
        result = cache.get(test_key)
        
        # Get cache stats
        cache_stats = CacheService.get_cache_stats()
        
        return {
            'status': 'ok' if result == 'ok' else 'fail',
            'message': 'Cache working properly' if result == 'ok' else 'Cache test failed',
            'details': cache_stats
        }
    except Exception as e:
        return {
            'status': 'fail',
            'message': f'Cache connection failed: {str(e)}'
        }

def check_storage():
    """Check file system storage"""
    try:
        # Test write/read operations
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write('health_check_test')
            temp_path = f.name
        
        # Read back the file
        with open(temp_path, 'r') as f:
            result = f.read()
        
        # Clean up
        os.unlink(temp_path)
        
        # Check disk space
        disk_usage = psutil.disk_usage('/')
        free_space_gb = disk_usage.free / (1024**3)
        
        return {
            'status': 'ok' if result == 'health_check_test' else 'fail',
            'message': 'Storage working properly' if result == 'health_check_test' else 'Storage test failed',
            'details': {
                'free_space_gb': round(free_space_gb, 2),
                'disk_usage_percent': round((disk_usage.used / disk_usage.total) * 100, 2)
            }
        }
    except Exception as e:
        return {
            'status': 'fail',
            'message': f'Storage access failed: {str(e)}'
        }

def check_system_resources():
    """Check system resource usage"""
    try:
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            'status': 'ok',
            'message': 'System resources normal',
            'details': {
                'cpu_usage_percent': cpu_percent,
                'memory_usage_percent': memory.percent,
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2)
            }
        }
    except Exception as e:
        return {
            'status': 'fail',
            'message': f'System resource check failed: {str(e)}'
        }

def metrics_endpoint(request):
    """Detailed metrics for monitoring"""
    # Cache key for metrics
    cache_key = CacheService.generate_key('query', type='metrics')
    
    def fetch_metrics():
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        
        return {
            'api_metrics': {
                'total_requests_24h': get_api_requests_count(last_24h),
                'avg_response_time_24h': get_avg_response_time(last_24h),
                'error_rate_24h': get_error_rate(last_24h)
            },
            'database_metrics': {
                'active_connections': get_db_connections_count(),
                'slow_queries_24h': get_slow_queries_count(last_24h),
                'database_size': get_database_size()
            },
            'cache_metrics': CacheService.get_cache_stats(),
            'content_metrics': {
                'users_total': User.objects.filter(is_active=True).count(),
                'users_new_7d': User.objects.filter(date_joined__gte=last_7d).count(),
                'posts_total': Post.objects.filter(status='published').count(),
                'posts_new_7d': Post.objects.filter(created_at__gte=last_7d, status='published').count(),
                'categories_total': Category.objects.filter(is_active=True).count()
            }
        }
    
    result = CacheService.get_or_set(cache_key, fetch_metrics, 60)  # Cache for 1 minute
    
    return JsonResponse({
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'metrics': result
    })

# Helper functions for metrics
def get_api_requests_count(since):
    """Get API request count from logs - implement based on your logging system"""
    return 0  # Placeholder

def get_avg_response_time(since):
    """Get average response time from logs"""
    return 0  # Placeholder

def get_error_rate(since):
    """Get error rate from logs"""
    return 0  # Placeholder

def get_db_connections_count():
    """Get active database connections"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM pg_stat_activity")
            return cursor.fetchone()[0]
    except:
        return 0

def get_slow_queries_count(since):
    """Get slow queries count"""
    return 0  # Placeholder

def get_database_size():
    """Get database size in MB"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_database_size(current_database())")
            size_bytes = cursor.fetchone()[0]
            return round(size_bytes / (1024**2), 2)  # Convert to MB
    except:
        return 0