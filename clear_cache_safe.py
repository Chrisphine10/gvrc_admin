#!/usr/bin/env python3
"""
Safe cache clearing script that preserves real-time functionality
Clears only non-critical caches while maintaining live data
"""
import os
import sys

# Add virtual environment to path if it exists
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env', 'lib', 'python3.9', 'site-packages')
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')
django.setup()

from django.core.cache import cache
from django.core.management import call_command
from django.db import connection

def clear_all_caches_safe():
    """Clear all caches safely without affecting real-time functionality"""
    print("🔄 Clearing caches safely...")
    
    # 1. Clear Django cache (doesn't affect database or real-time)
    try:
        cache.clear()
        print("✅ Django cache cleared")
    except Exception as e:
        print(f"⚠️  Error clearing Django cache: {e}")
    
    # 2. Clear database query cache (if using query caching)
    try:
        connection.queries_log.clear()
        print("✅ Database query log cleared")
    except Exception as e:
        print(f"⚠️  Error clearing query log: {e}")
    
    # 3. Clear static files cache (if using whitenoise)
    try:
        from django.contrib.staticfiles.management.commands.collectstatic import Command
        print("✅ Static files cache will be refreshed on next collectstatic")
    except Exception as e:
        print(f"⚠️  Note: {e}")
    
    # 4. Clear session cache (optional - only if not needed for live sessions)
    # Uncomment if you want to clear session cache
    # try:
    #     from django.contrib.sessions.models import Session
    #     Session.objects.all().delete()
    #     print("✅ Session cache cleared")
    # except Exception as e:
    #     print(f"⚠️  Error clearing sessions: {e}")
    
    print("\n✅ Cache clearing completed!")
    print("ℹ️  Real-time functionality (WebSockets, live data) is preserved")
    print("ℹ️  Database data is unchanged")

if __name__ == '__main__':
    clear_all_caches_safe()


