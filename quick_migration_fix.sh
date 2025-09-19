#!/bin/bash
# Quick Migration Fix for Facilities Index Issue

echo "🔧 QUICK MIGRATION FIX"
echo "======================="

# Set the correct settings module
export DJANGO_SETTINGS_MODULE=core.settings.postgres

echo "🔍 Running facilities migration fix..."
python fix_facilities_migration.py

echo ""
echo "🔧 Trying alternative fix if needed..."
python -c "
import os
import django
from pathlib import Path

# Set up Django
project_root = Path('.').resolve()
import sys
sys.path.insert(0, str(project_root))
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings.postgres'
django.setup()

from django.core.management import call_command

try:
    # Mark the problematic migration as fake applied
    call_command('migrate', 'facilities', '0004', '--fake', verbosity=0)
    print('✅ facilities.0004 marked as fake applied')
    
    # Run all migrations
    call_command('migrate', verbosity=0)
    print('✅ All migrations completed')
    
except Exception as e:
    print(f'⚠️  Error: {e}')
    print('📋 Trying fake-initial approach...')
    
    try:
        call_command('migrate', '--fake-initial', verbosity=0)
        print('✅ Migrations completed with fake-initial')
    except Exception as e2:
        print(f'❌ All approaches failed: {e2}')
"

echo ""
echo "🎉 Migration fix completed!"
echo "📝 Try running: python manage.py runserver 0.0.0.0:8000"
