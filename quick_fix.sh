#!/bin/bash
# Quick fix for the database configuration issue

echo "🔧 Quick Database Fix"
echo "===================="

# Clear problematic environment variables
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

echo "✅ Environment variables set:"
echo "DB_ENGINE: $DB_ENGINE"
echo "DB_NAME: $DB_NAME"
echo "DB_USERNAME: $DB_USERNAME"
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"

echo ""
echo "🚀 Running admin permissions fix..."
python manage.py fix_admin_permissions

echo ""
echo "✅ Done! Try logging in with admin@hodi.ke now."
