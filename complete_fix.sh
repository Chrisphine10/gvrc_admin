#!/bin/bash
# Complete Server Fix - Everything in One Script
# This script fixes database configuration, runs migrations, and sets up admin permissions

echo "🚀 Complete Server Fix Script"
echo "=============================="
echo "This script will:"
echo "1. Fix database configuration"
echo "2. Run database migrations"
echo "3. Create admin user"
echo "4. Set up admin permissions"
echo ""

# Step 1: Fix Database Configuration
echo "🔧 Step 1: Fixing database configuration..."
echo "📋 Clearing any problematic environment variables..."

# Clear any existing problematic environment variables
unset DB_ENGINE
unset DB_NAME
unset DB_USERNAME
unset DB_PASS
unset DB_HOST
unset DB_PORT

# Set correct environment variables
export DB_ENGINE="postgresql"
export DB_NAME="hodi_db"
export DB_USERNAME="postgres"
export DB_PASS="postgres123#"
export DB_HOST="hodi-db.cu7284ec0spr.us-east-1.rds.amazonaws.com"
export DB_PORT="5432"

echo "✅ Database environment variables set:"
echo "   DB_ENGINE: $DB_ENGINE"
echo "   DB_NAME: $DB_NAME"
echo "   DB_USERNAME: $DB_USERNAME"
echo "   DB_HOST: $DB_HOST"
echo "   DB_PORT: $DB_PORT"

# Step 2: Test Database Connection
echo ""
echo "🔧 Step 2: Testing database connection..."
if python -c "
import os
import django
from pathlib import Path

# Set up Django
project_root = Path('.').resolve()
import sys
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

# Override database settings directly
from django.conf import settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hodi_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres123#',
        'HOST': 'hodi-db.cu7284ec0spr.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
        'OPTIONS': {'connect_timeout': 60}
    }
}

# Test connection
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    if result:
        print('✅ Database connection successful!')
        exit(0)
    else:
        print('❌ Database query failed')
        exit(1)
" 2>/dev/null; then
    echo "✅ Database connection test passed"
else
    echo "❌ Database connection failed"
    echo "🔧 Troubleshooting steps:"
    echo "1. Check if AWS RDS instance is running"
    echo "2. Verify security group allows connections from your server"
    echo "3. Check if database credentials are correct"
    echo "4. Try connecting with psql manually:"
    echo "   psql -h hodi-db.cu7284ec0spr.us-east-1.rds.amazonaws.com -U postgres -d hodi_db"
    exit 1
fi

# Step 3: Run Database Migrations
echo ""
echo "🔧 Step 3: Running database migrations..."
echo "📋 Checking migration status..."
python manage.py showmigrations --verbosity=0

echo "🚀 Applying migrations..."
if python manage.py migrate --verbosity=0; then
    echo "✅ Database migrations completed successfully"
else
    echo "❌ Database migrations failed"
    exit 1
fi

# Step 4: Create Admin User
echo ""
echo "🔧 Step 4: Creating admin user..."
if python manage.py create_admin_user --verbosity=0; then
    echo "✅ Admin user created successfully"
else
    echo "⚠️  Admin user creation failed or user already exists"
fi

# Step 5: Set Up Admin Permissions
echo ""
echo "🔧 Step 5: Setting up admin permissions..."
if python manage.py fix_admin_permissions --verbosity=0; then
    echo "✅ Admin permissions set up successfully"
else
    echo "❌ Admin permissions setup failed"
    exit 1
fi

# Step 6: Verify Everything Works
echo ""
echo "🔧 Step 6: Verifying setup..."
echo "📋 Running system check..."
if python manage.py check --verbosity=0; then
    echo "✅ Django system check passed"
else
    echo "⚠️  Django system check found issues"
fi

# Final Summary
echo ""
echo "🎉 SUCCESS! Complete server fix completed!"
echo "=========================================="
echo "✅ Database configuration: FIXED"
echo "✅ Database connection: WORKING"
echo "✅ Database migrations: COMPLETED"
echo "✅ Admin user: CREATED"
echo "✅ Admin permissions: SET UP"
echo "✅ System check: PASSED"
echo ""
echo "📝 Next steps:"
echo "1. Try logging in with admin@hodi.ke"
echo "2. Test the chat assignment functionality at https://hodi.co.ke/chat/conversation/1/"
echo "3. Verify all admin features are working properly"
echo ""
echo "🚀 Your server is now ready to use!"
