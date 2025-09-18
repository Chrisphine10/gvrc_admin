#!/bin/bash
# Script to fix admin permissions on the server
# Run this script on your server to fix the admin user permissions

echo "🔧 Fixing admin user permissions on server..."

# Activate virtual environment (adjust path as needed)
if [ -d "env" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
elif [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found, using system Python"
fi

# Run the management command
echo "🚀 Running fix_admin_permissions command..."
python manage.py fix_admin_permissions

echo "✅ Done! Try logging in again with your admin account."
