# -*- encoding: utf-8 -*-
"""
Monitoring views for live system monitoring
"""

import psutil
import time
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import os
import json
from datetime import datetime, timedelta


@login_required
def monitoring_dashboard(request):
    """Monitoring dashboard page"""
    context = {
        'segment': 'monitoring',
        'page_title': 'System Monitoring',
    }
    return render(request, 'monitoring/dashboard.html', context)


@require_http_methods(["GET"])
def health_check(request):
    """Basic health check endpoint"""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return JsonResponse({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'database': db_status,
        'service': 'gvrc_admin'
    })


@require_http_methods(["GET"])
@login_required
def system_metrics(request):
    """Get system resource metrics"""
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        
        # Network metrics
        net_io = psutil.net_io_counters()
        
        # Process metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        
        return JsonResponse({
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency_mhz': cpu_freq.current if cpu_freq else None,
            },
            'memory': {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'percent': memory.percent,
            },
            'disk': {
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'percent': round((disk.used / disk.total) * 100, 2),
            },
            'network': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
            },
            'process': {
                'memory_mb': round(process_memory.rss / (1024**2), 2),
                'cpu_percent': process.cpu_percent(interval=0.1),
            }
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)


@require_http_methods(["GET"])
@login_required
def database_metrics(request):
    """Get database connection and performance metrics"""
    try:
        with connection.cursor() as cursor:
            # Check connection
            cursor.execute("SELECT 1")
            
            # Get database size (PostgreSQL)
            try:
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database())) as size
                """)
                db_size = cursor.fetchone()[0]
            except:
                db_size = "unknown"
            
            # Get active connections
            try:
                cursor.execute("""
                    SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()
                """)
                active_connections = cursor.fetchone()[0]
            except:
                active_connections = "unknown"
            
            # Get connection pool info
            pool_info = {
                'max_connections': getattr(settings, 'CONN_MAX_AGE', 'N/A'),
            }
            
        return JsonResponse({
            'timestamp': datetime.now().isoformat(),
            'status': 'connected',
            'database_size': db_size,
            'active_connections': active_connections,
            'connection_pool': pool_info,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)


@require_http_methods(["GET"])
@login_required
def application_metrics(request):
    """Get application-specific metrics"""
    try:
        # Check cache
        cache_status = "working"
        try:
            cache.set('health_check', 'ok', 10)
            cache_result = cache.get('health_check')
            if cache_result != 'ok':
                cache_status = "degraded"
        except:
            cache_status = "not_working"
        
        # Check static files
        static_root = getattr(settings, 'STATIC_ROOT', None)
        static_exists = os.path.exists(static_root) if static_root else False
        
        # Check media files
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        media_exists = os.path.exists(media_root) if media_root else False
        
        # Get log file sizes
        log_files = {
            'gunicorn_error': '/var/log/gvrc_admin/gunicorn_error.log',
            'gunicorn_access': '/var/log/gvrc_admin/gunicorn_access.log',
            'django': '/var/log/gvrc_admin/django.log',
        }
        
        log_sizes = {}
        for name, path in log_files.items():
            if os.path.exists(path):
                size = os.path.getsize(path)
                log_sizes[name] = {
                    'size_mb': round(size / (1024**2), 2),
                    'exists': True
                }
            else:
                log_sizes[name] = {'exists': False}
        
        return JsonResponse({
            'timestamp': datetime.now().isoformat(),
            'cache': cache_status,
            'static_files': {
                'exists': static_exists,
                'path': static_root
            },
            'media_files': {
                'exists': media_exists,
                'path': media_root
            },
            'logs': log_sizes,
            'debug_mode': settings.DEBUG,
            'allowed_hosts_count': len(getattr(settings, 'ALLOWED_HOSTS', [])),
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)


@require_http_methods(["GET"])
@login_required
def full_status(request):
    """Get complete system status"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "healthy"
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
        
        # Cache check
        cache_status = "working"
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') != 'ok':
                cache_status = "degraded"
        except:
            cache_status = "not_working"
        
        # Overall status
        overall_status = "healthy"
        if db_status != "healthy" or memory.percent > 90 or disk.percent > 90:
            overall_status = "degraded"
        if db_status != "healthy" or memory.percent > 95 or disk.percent > 95:
            overall_status = "critical"
        
        return JsonResponse({
            'timestamp': datetime.now().isoformat(),
            'status': overall_status,
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
            },
            'services': {
                'database': db_status,
                'cache': cache_status,
            },
            'alerts': _generate_alerts(cpu_percent, memory.percent, disk.percent, db_status)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)


def _generate_alerts(cpu, memory, disk, db_status):
    """Generate alerts based on metrics"""
    alerts = []
    
    if cpu > 90:
        alerts.append({
            'level': 'warning',
            'message': f'High CPU usage: {cpu}%',
            'timestamp': datetime.now().isoformat()
        })
    if memory > 90:
        alerts.append({
            'level': 'warning',
            'message': f'High memory usage: {memory}%',
            'timestamp': datetime.now().isoformat()
        })
    if disk > 90:
        alerts.append({
            'level': 'warning',
            'message': f'High disk usage: {disk}%',
            'timestamp': datetime.now().isoformat()
        })
    if db_status != "healthy":
        alerts.append({
            'level': 'critical',
            'message': f'Database issue: {db_status}',
            'timestamp': datetime.now().isoformat()
        })
    
    return alerts
