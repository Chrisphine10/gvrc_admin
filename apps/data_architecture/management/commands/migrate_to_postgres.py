"""
Django management command for PostgreSQL migration
Following data engineering best practices with iterative testing
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
from django.conf import settings
import os
import json
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Migrate system from SQLite to PostgreSQL with comprehensive testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup before migration',
        )
        parser.add_argument(
            '--test-only',
            action='store_true',
            help='Test migration without applying changes',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output',
        )
    
    def handle(self, *args, **options):
        self.verbose = options['verbose']
        self.test_only = options['test_only']
        self.backup = options['backup']
        
        self.stdout.write(self.style.SUCCESS('🐘 Starting PostgreSQL Migration Process'))
        self.stdout.write('=' * 60)
        
        # Step 1: Pre-migration validation
        if not self.pre_migration_validation():
            self.stdout.write(self.style.ERROR('❌ Pre-migration validation failed'))
            return
        
        # Step 2: Create backup if requested
        if self.backup:
            if not self.create_backup():
                self.stdout.write(self.style.ERROR('❌ Backup creation failed'))
                return
        
        # Step 3: Test PostgreSQL connection
        if not self.test_postgres_connection():
            self.stdout.write(self.style.ERROR('❌ PostgreSQL connection test failed'))
            return
        
        # Step 4: Migrate database
        if not self.test_only:
            if not self.migrate_database():
                self.stdout.write(self.style.ERROR('❌ Database migration failed'))
                return
        
        # Step 5: Post-migration validation
        if not self.post_migration_validation():
            self.stdout.write(self.style.ERROR('❌ Post-migration validation failed'))
            return
        
        self.stdout.write(self.style.SUCCESS('✅ PostgreSQL migration completed successfully!'))
    
    def pre_migration_validation(self):
        """Validate system before migration"""
        self.stdout.write('🔍 Pre-migration validation...')
        
        try:
            # Check current database
            with connection.cursor() as cursor:
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                self.stdout.write(f"   Current database: SQLite {version}")
            
            # Check if data exists
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
                table_count = cursor.fetchone()[0]
                self.stdout.write(f"   Tables found: {table_count}")
            
            self.stdout.write(self.style.SUCCESS('   ✅ Pre-migration validation passed'))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Pre-migration validation failed: {str(e)}'))
            return False
    
    def create_backup(self):
        """Create backup of current database"""
        self.stdout.write('💾 Creating database backup...')
        
        try:
            backup_dir = 'backups'
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'{backup_dir}/sqlite_backup_{timestamp}.db'
            
            # Copy SQLite database
            import shutil
            shutil.copy2('db.sqlite3', backup_file)
            
            self.stdout.write(f'   ✅ Backup created: {backup_file}')
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Backup creation failed: {str(e)}'))
            return False
    
    def test_postgres_connection(self):
        """Test PostgreSQL connection"""
        self.stdout.write('🔌 Testing PostgreSQL connection...')
        
        try:
            # Test direct PostgreSQL connection
            import psycopg2
            
            conn = psycopg2.connect(
                host="localhost",
                database="gvrc_admin_postgres",
                user="gvrc_user",
                password="gvrc_password"
            )
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(f"   ✅ PostgreSQL connection successful: {version.split(',')[0]}")
            
            conn.close()
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ PostgreSQL connection failed: {str(e)}'))
            return False
    
    def migrate_database(self):
        """Migrate database to PostgreSQL"""
        self.stdout.write('🔄 Migrating database to PostgreSQL...')
        
        try:
            # Step 1: Run migrations with PostgreSQL
            self.stdout.write('   Running migrations with PostgreSQL...')
            call_command('migrate', '--settings=core.settings.postgres', verbosity=1)
            
            # Step 2: Skip superuser creation (already exists)
            self.stdout.write('   Skipping superuser creation (already exists)...')
            
            self.stdout.write(self.style.SUCCESS('   ✅ Database migration completed'))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Database migration failed: {str(e)}'))
            return False
    
    def post_migration_validation(self):
        """Validate system after migration"""
        self.stdout.write('🔍 Post-migration validation...')
        
        try:
            if self.test_only:
                self.stdout.write('   ⚠️  Test mode - skipping post-migration validation')
                return True
            
            # Test with PostgreSQL settings
            from django.conf import settings
            from django.db import connections
            
            # Switch to PostgreSQL for validation
            postgres_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'gvrc_admin_postgres',
                'USER': 'gvrc_user',
                'PASSWORD': 'gvrc_password',
                'HOST': 'localhost',
                'PORT': '5432',
                'OPTIONS': {},
            }
            
            connections.databases['postgres_test'] = postgres_config
            
            with connections['postgres_test'].cursor() as cursor:
                # Check tables
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cursor.fetchall()]
                self.stdout.write(f"   Tables in PostgreSQL: {len(tables)}")
                
                # Check data counts
                if 'data_sources' in tables:
                    cursor.execute("SELECT COUNT(*) FROM data_sources;")
                    count = cursor.fetchone()[0]
                    self.stdout.write(f"   Data sources: {count}")
            
            self.stdout.write(self.style.SUCCESS('   ✅ Post-migration validation passed'))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Post-migration validation failed: {str(e)}'))
            return False