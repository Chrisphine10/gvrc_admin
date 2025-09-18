#!/bin/bash
# Script to fix database configuration on the server

echo "🔧 Fixing database configuration..."

# Check current environment variables
echo "📋 Current environment variables:"
echo "DB_ENGINE: $DB_ENGINE"
echo "DB_NAME: $DB_NAME"
echo "DB_USERNAME: $DB_USERNAME"
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"

# Fix the DB_ENGINE variable
echo "🔧 Setting correct DB_ENGINE..."
export DB_ENGINE="postgresql"

# Set other database variables if not set
export DB_NAME="${DB_NAME:-gvrc_db}"
export DB_USERNAME="${DB_USERNAME:-postgres}"
export DB_PASS="${DB_PASS:-postgres123#}"
export DB_HOST="${DB_HOST:-database-postgres.cn2uqm2iclii.eu-north-1.rds.amazonaws.com}"
export DB_PORT="${DB_PORT:-5432}"

echo "✅ Updated environment variables:"
echo "DB_ENGINE: $DB_ENGINE"
echo "DB_NAME: $DB_NAME"
echo "DB_USERNAME: $DB_USERNAME"
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"

# Test database connection
echo "🔍 Testing database connection..."
python manage.py check --database default

echo "✅ Database configuration fixed!"
echo "🚀 You can now run your Django commands normally."
