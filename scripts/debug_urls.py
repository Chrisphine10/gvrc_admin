#!/usr/bin/env python
"""
Debug script to check all URL patterns and identify conflicts
"""

import os
import sys
import django

def main():
    """Debug URL patterns"""
    print("Setting up Django environment...")
    
    try:
        # Setup Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
        print("✅ Django setup successful")
        
        # Check all URL patterns
        print("\n🔍 Checking all URL patterns...")
        
        from django.urls import get_resolver
        from django.urls.resolvers import URLPattern, URLResolver
        
        def print_urls(urls, level=0):
            indent = "  " * level
            for url in urls:
                if isinstance(url, URLPattern):
                    print(f"{indent}• {url.pattern} -> {url.callback.__name__ if hasattr(url, 'callback') else 'Unknown'}")
                elif isinstance(url, URLResolver):
                    print(f"{indent}📁 {url.pattern} (Namespace: {url.namespace})")
                    print_urls(url.url_patterns, level + 1)
        
        # Get the main URL resolver
        resolver = get_resolver()
        print_urls(resolver.url_patterns)
        
        # Check specific authentication URLs
        print("\n🔐 Checking authentication URLs...")
        
        from django.urls import reverse
        try:
            login_url = reverse('login')
            print(f"✅ Login URL: {login_url}")
        except Exception as e:
            print(f"❌ Login URL error: {e}")
        
        try:
            logout_url = reverse('logout')
            print(f"✅ Logout URL: {logout_url}")
        except Exception as e:
            print(f"❌ Logout URL error: {e}")
        
        # Check if there are any accounts-related URLs
        print("\n🔍 Checking for accounts-related URLs...")
        
        all_urls = []
        def collect_urls(urls, prefix=""):
            for url in urls:
                if isinstance(url, URLPattern):
                    pattern = prefix + str(url.pattern)
                    all_urls.append(pattern)
                elif isinstance(url, URLResolver):
                    new_prefix = prefix + str(url.pattern)
                    collect_urls(url.url_patterns, new_prefix)
        
        collect_urls(resolver.url_patterns)
        
        accounts_urls = [url for url in all_urls if 'accounts' in url or 'auth' in url]
        if accounts_urls:
            print("⚠️  Found potential conflicting URLs:")
            for url in accounts_urls:
                print(f"   - {url}")
        else:
            print("✅ No conflicting accounts/auth URLs found")
        
        # Check settings
        print("\n⚙️  Checking authentication settings...")
        
        from django.conf import settings
        print(f"   LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Not set')}")
        print(f"   LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Not set')}")
        print(f"   LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'Not set')}")
        print(f"   AUTH_USER_MODEL: {getattr(settings, 'AUTH_USER_MODEL', 'Not set')}")
        
        # Check installed apps
        print(f"\n📱 Installed apps:")
        for app in settings.INSTALLED_APPS:
            print(f"   - {app}")
        
        print("\n🎯 Debug complete!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
