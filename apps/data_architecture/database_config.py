"""
PostgreSQL-Only Database Configuration
Ensures all data architecture components use PostgreSQL
"""

from django.conf import settings
from django.db import connections
import logging

logger = logging.getLogger(__name__)


class PostgreSQLOnlyConfig:
    """PostgreSQL-only configuration for data architecture"""
    
    def __init__(self):
        self.required_databases = ['default']
        self.postgres_required = True
    
    def validate_postgres_only(self):
        """Validate that all databases are PostgreSQL"""
        try:
            for db_alias in self.required_databases:
                if db_alias in connections.databases:
                    db_config = connections.databases[db_alias]
                    engine = db_config.get('ENGINE', '')
                    
                    if 'postgresql' not in engine.lower():
                        raise ValueError(f"Database {db_alias} is not PostgreSQL: {engine}")
                    
                    logger.info(f"✅ Database {db_alias} is PostgreSQL: {engine}")
            
            logger.info("✅ All databases are PostgreSQL")
            return True
            
        except Exception as e:
            logger.error(f"❌ PostgreSQL validation failed: {e}")
            return False
    
    def get_postgres_connection(self, db_alias='default'):
        """Get PostgreSQL connection"""
        try:
            connection = connections[db_alias]
            if 'postgresql' not in connection.settings_dict['ENGINE'].lower():
                raise ValueError(f"Database {db_alias} is not PostgreSQL")
            return connection
        except Exception as e:
            logger.error(f"Failed to get PostgreSQL connection: {e}")
            raise
    
    def create_data_architecture_tables(self):
        """Create data architecture tables in PostgreSQL"""
        try:
            connection = self.get_postgres_connection()
            
            with connection.cursor() as cursor:
                # Create data architecture schema if it doesn't exist
                cursor.execute("""
                    CREATE SCHEMA IF NOT EXISTS data_architecture;
                """)
                
                # Create data sources table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS data_architecture.data_sources (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        source_type VARCHAR(50) NOT NULL,
                        description TEXT,
                        is_active BOOLEAN DEFAULT TRUE,
                        configuration JSONB DEFAULT '{}',
                        last_sync TIMESTAMP,
                        sync_frequency VARCHAR(20) DEFAULT 'manual',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Create raw data records table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS data_architecture.raw_data_records (
                        id SERIAL PRIMARY KEY,
                        source_id INTEGER REFERENCES data_architecture.data_sources(id),
                        data_id VARCHAR(100) UNIQUE NOT NULL,
                        raw_data JSONB NOT NULL,
                        metadata JSONB DEFAULT '{}',
                        checksum VARCHAR(64) UNIQUE NOT NULL,
                        file_path VARCHAR(500),
                        processing_status VARCHAR(20) DEFAULT 'pending',
                        error_message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Create indexes
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_raw_data_source_status 
                    ON data_architecture.raw_data_records(source_id, processing_status);
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_raw_data_created_at 
                    ON data_architecture.raw_data_records(created_at);
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_raw_data_checksum 
                    ON data_architecture.raw_data_records(checksum);
                """)
                
                logger.info("✅ Data architecture tables created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Failed to create data architecture tables: {e}")
            return False
    
    def test_postgres_connection(self):
        """Test PostgreSQL connection and functionality"""
        try:
            connection = self.get_postgres_connection()
            
            with connection.cursor() as cursor:
                # Test basic query
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                logger.info(f"✅ PostgreSQL version: {version}")
                
                # Test JSONB functionality
                cursor.execute("SELECT '{\"test\": \"data\"}'::jsonb;")
                result = cursor.fetchone()[0]
                logger.info(f"✅ JSONB test successful: {result}")
                
                # Test schema creation
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = 'data_architecture';
                """)
                schema_exists = cursor.fetchone()
                if schema_exists:
                    logger.info("✅ Data architecture schema exists")
                else:
                    logger.info("ℹ️  Data architecture schema will be created")
                
                return True
                
        except Exception as e:
            logger.error(f"PostgreSQL connection test failed: {e}")
            return False


def ensure_postgres_only():
    """Ensure the entire system uses PostgreSQL only"""
    config = PostgreSQLOnlyConfig()
    
    # Validate PostgreSQL only
    if not config.validate_postgres_only():
        raise ValueError("System must use PostgreSQL only")
    
    # Test connection
    if not config.test_postgres_connection():
        raise ValueError("PostgreSQL connection test failed")
    
    # Create tables
    if not config.create_data_architecture_tables():
        raise ValueError("Failed to create data architecture tables")
    
    logger.info("✅ PostgreSQL-only configuration validated successfully")
    return True

