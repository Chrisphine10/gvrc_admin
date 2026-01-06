#!/bin/bash
# Emergency rollback script
# Use this if something goes wrong during implementation

set -e

echo "=========================================="
echo "EMERGENCY ROLLBACK SCRIPT"
echo "=========================================="
echo ""
echo "WARNING: This will rollback all changes!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Get the latest backup tag
LATEST_TAG=$(git tag -l "backup-pre-api-fixes-*" | sort -r | head -1)

if [ -z "$LATEST_TAG" ]; then
    echo "ERROR: No backup tag found!"
    exit 1
fi

echo "Rolling back to: $LATEST_TAG"

# Restore from Git
echo "Restoring code from Git..."
git checkout "$LATEST_TAG"
echo "✓ Code restored"

# Restore database (if backup exists)
LATEST_DB_BACKUP=$(ls -t backups/db_backup_*.sql 2>/dev/null | head -1)
if [ -n "$LATEST_DB_BACKUP" ] && [ -n "$DB_HOST" ]; then
    echo "Restoring database..."
    echo "WARNING: This will overwrite current database!"
    read -p "Continue? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" < "$LATEST_DB_BACKUP"
        echo "✓ Database restored"
    fi
fi

# Restore media files (if backup exists)
LATEST_MEDIA_BACKUP=$(ls -t backups/media_backup_*.tar.gz 2>/dev/null | head -1)
if [ -n "$LATEST_MEDIA_BACKUP" ]; then
    echo "Restoring media files..."
    tar -xzf "$LATEST_MEDIA_BACKUP"
    echo "✓ Media files restored"
fi

echo ""
echo "=========================================="
echo "Rollback Complete!"
echo "=========================================="
echo "Please verify the system is working correctly."



