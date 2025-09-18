#!/usr/bin/env python
"""
Server Database Configuration Fix Script
Run this script on your server to fix the database configuration issue.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.postgres')
django.setup()

def fix_database_config():
    """Fix the database configuration issue"""
    print("🔧 Fixing database configuration...")
    
    # Check current environment variables
    print("\n📋 Current environment variables:")
    print(f"DB_ENGINE: {os.getenv('DB_ENGINE', 'Not set')}")
    print(f"DB_NAME: {os.getenv('DB_NAME', 'Not set')}")
    print(f"DB_USERNAME: {os.getenv('DB_USERNAME', 'Not set')}")
    print(f"DB_HOST: {os.getenv('DB_HOST', 'Not set')}")
    print(f"DB_PORT: {os.getenv('DB_PORT', 'Not set')}")
    
    # Fix the DB_ENGINE variable
    print("\n🔧 Setting correct DB_ENGINE...")
    os.environ['DB_ENGINE'] = 'postgresql'
    
    # Set other database variables if not set
    os.environ.setdefault('DB_NAME', 'gvrc_db')
    os.environ.setdefault('DB_USERNAME', 'postgres')
    os.environ.setdefault('DB_PASS', 'postgres123#')
    os.environ.setdefault('DB_HOST', 'database-postgres.cn2uqm2iclii.eu-north-1.rds.amazonaws.com')
    os.environ.setdefault('DB_PORT', '5432')
    
    print("\n✅ Updated environment variables:")
    print(f"DB_ENGINE: {os.environ['DB_ENGINE']}")
    print(f"DB_NAME: {os.environ['DB_NAME']}")
    print(f"DB_USERNAME: {os.environ['DB_USERNAME']}")
    print(f"DB_HOST: {os.environ['DB_HOST']}")
    print(f"DB_PORT: {os.environ['DB_PORT']}")
    
    # Test database connection
    print("\n🔍 Testing database connection...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'check', '--database', 'default'])
        print("✅ Database connection successful!")
        
        # Test the fix_admin_permissions command
        print("\n🚀 Testing fix_admin_permissions command...")
        execute_from_command_line(['manage.py', 'fix_admin_permissions'])
        print("✅ Admin permissions fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Server Database Configuration Fix Script")
    print("=" * 50)
    
    success = fix_database_config()
    
    if success:
        print("\n🎉 SUCCESS! Database configuration has been fixed!")
        print("✅ You can now run your Django commands normally.")
        print("✅ Admin permissions have been set up.")
        print("\n📝 Next steps:")
        print("1. Try logging in with admin@hodi.ke")
        print("2. Test the chat assignment functionality")
        print("3. Check that all features are working properly")
    else:
        print("\n❌ FAILED! Please check the error messages above.")
        print("🔧 Manual fix required:")
        print("1. Set DB_ENGINE=postgresql (not django.db.backends.postgresql)")
        print("2. Ensure database credentials are correct")
        print("3. Check database server connectivity")
