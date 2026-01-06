#!/bin/bash
# Preparation script for API fixes
# Ensures all backups and safety measures are in place

set -e  # Exit on error

echo "=========================================="
echo "API Fixes Preparation Script"
echo "=========================================="

# Create directories
echo "Creating backup directories..."
mkdir -p backups
mkdir -p scripts/fixes
mkdir -p scripts/rollback
mkdir -p scripts/verify
mkdir -p logs

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "Timestamp: $TIMESTAMP"

# Git operations
echo "Creating Git backup tag..."
git tag "backup-pre-api-fixes-$TIMESTAMP"
echo "✓ Git tag created: backup-pre-api-fixes-$TIMESTAMP"

# Database backup (if PostgreSQL)
if [ -n "$DB_HOST" ]; then
    echo "Backing up PostgreSQL database..."
    pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" > "backups/db_backup_$TIMESTAMP.sql"
    echo "✓ Database backup created"
elif [ -f "db.sqlite3" ]; then
    echo "Backing up SQLite database..."
    cp db.sqlite3 "backups/db_backup_$TIMESTAMP.sqlite3"
    echo "✓ SQLite backup created"
fi

# Media files backup
if [ -d "media" ]; then
    echo "Backing up media files..."
    tar -czf "backups/media_backup_$TIMESTAMP.tar.gz" media/
    echo "✓ Media backup created"
fi

# Requirements backup
echo "Backing up requirements..."
pip list > "backups/requirements_backup_$TIMESTAMP.txt"
echo "✓ Requirements backup created"

# Create change log
echo "Creating change log..."
cat > "CHANGES_API_FIXES_$(date +%Y%m%d).md" << EOF
# API Fixes Change Log - $(date +%Y-%m-%d)

## Preparation
- **Timestamp**: $TIMESTAMP
- **Git Tag**: backup-pre-api-fixes-$TIMESTAMP
- **Backups Created**: Yes

## Changes Applied

EOF
echo "✓ Change log created"

# Create baseline test results
echo "Creating baseline test results..."
if [ -f "test_all_apis.py" ]; then
    python test_all_apis.py > "logs/test_baseline_$TIMESTAMP.log" 2>&1 || true
    echo "✓ Baseline test results saved"
fi

echo "=========================================="
echo "Preparation Complete!"
echo "=========================================="
echo "All backups and safety measures are in place."
echo "You can now proceed with the fixes."



