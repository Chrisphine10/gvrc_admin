# Technical Implementation Guide: GVRC ETL Pipeline

## Quick Start Guide

### 1. Prerequisites
```bash
# System Requirements
- Python 3.12+
- PostgreSQL 16.9+
- Redis (optional, for caching)
- 4GB RAM minimum
- 10GB disk space

# Install Dependencies
pip install -r config/etl_requirements.txt
```

### 2. Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres createdb gvrc_admin_production
sudo -u postgres psql -c "CREATE USER gvrc_user WITH PASSWORD 'gvrc_password123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gvrc_admin_production TO gvrc_user;"

# Run migrations
DJANGO_SETTINGS_MODULE=core.settings.production python manage.py migrate

# Load data
DJANGO_SETTINGS_MODULE=core.settings.production python manage.py loaddata sqlite_data_export.json
```

### 3. Run ETL Pipeline
```bash
# Execute production importer
python src/scripts/production_json_importer.py

# Or run specific components
python -m src.etl_pipeline.pipeline --config config/production.yaml
```

## Implementation Details

### 1. Core ETL Pipeline
```python
# src/etl_pipeline/pipeline.py
class ETLPipeline:
    def __init__(self, config_path: str = None):
        self.config = ConfigManager(config_path)
        self.logger = structlog.get_logger()
        self.metrics = MetricsCollector()
        self.circuit_breaker = CircuitBreaker()
    
    def run(self, data_sources: list) -> dict:
        """Execute complete ETL pipeline"""
        try:
            self.metrics.start_processing()
            
            # Extract phase
            raw_data = self.extract_data(data_sources)
            
            # Transform phase
            transformed_data = self.transform_data(raw_data)
            
            # Load phase
            load_result = self.load_data(transformed_data)
            
            self.metrics.end_processing()
            
            return {
                'success': True,
                'processed_count': len(transformed_data),
                'error_count': 0,
                'metrics': self.metrics.get_metrics_summary()
            }
            
        except Exception as e:
            self.logger.error("ETL pipeline failed", error=str(e))
            return {
                'success': False,
                'error': str(e),
                'metrics': self.metrics.get_metrics_summary()
            }
```

### 2. Data Extraction
```python
# src/etl_pipeline/extractors/json_extractor.py
class JSONExtractor:
    def __init__(self):
        self.schema_validator = JSONSchemaValidator()
        self.logger = structlog.get_logger()
    
    def extract_facilities(self, file_path: str) -> list:
        """Extract facilities from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Validate schema
            if not self.schema_validator.validate(data):
                raise DataValidationError("Invalid JSON schema")
            
            # Extract facilities based on file structure
            facilities = self._extract_facilities_by_structure(data)
            
            self.logger.info("Extraction completed", 
                           file_path=file_path, 
                           facility_count=len(facilities))
            
            return facilities
            
        except Exception as e:
            self.logger.error("Extraction failed", 
                            file_path=file_path, 
                            error=str(e))
            return []
    
    def _extract_facilities_by_structure(self, data: dict) -> list:
        """Extract facilities based on JSON structure"""
        if isinstance(data, list):
            return data
        elif 'facilities' in data:
            return data['facilities']
        elif 'data' in data:
            return data['data']
        else:
            return [data]
```

### 3. Data Transformation
```python
# src/etl_pipeline/transformers/facility_transformer.py
class FacilityTransformer:
    def __init__(self):
        self.geographic_mapper = GeographicMapper()
        self.data_enricher = DataEnricher()
        self.validator = DataValidator()
    
    def transform_facility(self, raw_facility: dict) -> dict:
        """Transform raw facility data to standardized format"""
        try:
            # Standardize schema
            standardized = self._standardize_schema(raw_facility)
            
            # Map geographic data
            geo_mapped = self.geographic_mapper.map_location(standardized)
            
            # Enrich data
            enriched = self.data_enricher.enrich_facility(geo_mapped)
            
            # Validate transformed data
            validation_result = self.validator.validate_facility(enriched)
            
            if not validation_result.is_valid:
                raise DataValidationError(f"Validation failed: {validation_result.errors}")
            
            return enriched
            
        except Exception as e:
            self.logger.error("Transformation failed", 
                            facility=raw_facility.get('name', 'Unknown'),
                            error=str(e))
            raise DataTransformationError(f"Failed to transform facility: {e}")
    
    def _standardize_schema(self, raw_data: dict) -> dict:
        """Standardize field names and structure"""
        mapping = {
            'name': 'facility_name',
            'facility_name': 'facility_name',
            'code': 'facility_code',
            'facility_code': 'facility_code',
            'location': 'location',
            'contacts': 'contacts',
            'services': 'services'
        }
        
        standardized = {}
        for raw_key, standard_key in mapping.items():
            if raw_key in raw_data:
                standardized[standard_key] = raw_data[raw_key]
        
        return standardized
```

### 4. Data Loading
```python
# src/etl_pipeline/loaders/database_loader.py
class DatabaseLoader:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self.connection_pool = self._create_connection_pool()
        self.logger = structlog.get_logger()
    
    def load_facilities(self, facilities: list) -> dict:
        """Load facilities into database"""
        success_count = 0
        error_count = 0
        errors = []
        
        # Process in batches
        batch_size = self.db_config.batch_size
        for i in range(0, len(facilities), batch_size):
            batch = facilities[i:i + batch_size]
            
            try:
                self._load_facility_batch(batch)
                success_count += len(batch)
                
                self.logger.info("Batch loaded successfully", 
                               batch_size=len(batch),
                               total_processed=i + len(batch))
                
            except Exception as e:
                error_count += len(batch)
                errors.append({
                    'batch_start': i,
                    'batch_size': len(batch),
                    'error': str(e)
                })
                
                self.logger.error("Batch loading failed", 
                                batch_start=i,
                                batch_size=len(batch),
                                error=str(e))
        
        return {
            'success_count': success_count,
            'error_count': error_count,
            'errors': errors
        }
    
    def _load_facility_batch(self, facilities: list):
        """Load a batch of facilities"""
        with self.connection_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                # Use transaction for atomicity
                cursor.execute("BEGIN")
                
                try:
                    for facility in facilities:
                        self._insert_facility(cursor, facility)
                    
                    cursor.execute("COMMIT")
                    
                except Exception as e:
                    cursor.execute("ROLLBACK")
                    raise e
    
    def _insert_facility(self, cursor, facility: dict):
        """Insert single facility"""
        cursor.execute("""
            INSERT INTO facilities (
                facility_code, registration_number, facility_name,
                facility_type, operational_status_id, ward_id,
                created_by, updated_by, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (facility_code) DO UPDATE SET
                registration_number = EXCLUDED.registration_number,
                facility_name = EXCLUDED.facility_name,
                updated_at = CURRENT_TIMESTAMP
        """, (
            facility['facility_code'],
            facility.get('registration_number', ''),
            facility['facility_name'],
            facility.get('facility_type'),
            facility.get('operational_status_id'),
            facility.get('ward_id'),
            facility.get('created_by'),
            facility.get('updated_by'),
            facility.get('is_active', True)
        ))
```

## Performance Optimization

### 1. Database Indexing
```sql
-- Essential indexes for performance
CREATE INDEX CONCURRENTLY idx_facilities_facility_code ON facilities(facility_code);
CREATE INDEX CONCURRENTLY idx_facilities_registration_number ON facilities(registration_number);
CREATE INDEX CONCURRENTLY idx_facilities_ward_id ON facilities(ward_id);
CREATE INDEX CONCURRENTLY idx_facilities_operational_status ON facilities(operational_status_id);
CREATE INDEX CONCURRENTLY idx_facilities_active ON facilities(facility_id) WHERE is_active = TRUE;

-- Composite indexes for common queries
CREATE INDEX CONCURRENTLY idx_facilities_location_status ON facilities(ward_id, operational_status_id);
CREATE INDEX CONCURRENTLY idx_facilities_created_updated ON facilities(created_at, updated_at);
```

### 2. Memory Management
```python
# src/etl_pipeline/utils/memory_manager.py
class MemoryManager:
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_mb = max_memory_mb
        self.process = psutil.Process()
    
    def check_memory_usage(self):
        """Check and manage memory usage"""
        memory_usage = self.process.memory_info().rss / 1024 / 1024
        
        if memory_usage > self.max_memory_mb:
            self.logger.warning("High memory usage detected", 
                              memory_usage_mb=memory_usage,
                              max_memory_mb=self.max_memory_mb)
            
            # Force garbage collection
            gc.collect()
            
            # Check again after GC
            memory_usage = self.process.memory_info().rss / 1024 / 1024
            if memory_usage > self.max_memory_mb:
                raise MemoryError(f"Memory usage exceeded limit: {memory_usage}MB")
    
    def process_in_chunks(self, data: list, chunk_size: int = 1000):
        """Process data in memory-efficient chunks"""
        for i in range(0, len(data), chunk_size):
            self.check_memory_usage()
            yield data[i:i + chunk_size]
```

## Monitoring & Alerting

### 1. Health Checks
```python
# src/etl_pipeline/monitoring/health_checker.py
class HealthChecker:
    def __init__(self):
        self.checks = {
            'database': self.check_database_connection,
            'memory': self.check_memory_usage,
            'disk': self.check_disk_space,
            'etl_pipeline': self.check_etl_pipeline_status
        }
    
    def run_health_checks(self) -> dict:
        """Run all health checks"""
        results = {}
        overall_status = 'healthy'
        
        for check_name, check_func in self.checks.items():
            try:
                result = check_func()
                results[check_name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'details': result
                }
                if not result:
                    overall_status = 'unhealthy'
            except Exception as e:
                results[check_name] = {
                    'status': 'error',
                    'details': str(e)
                }
                overall_status = 'unhealthy'
        
        return {
            'overall_status': overall_status,
            'checks': results,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def check_database_connection(self) -> bool:
        """Check database connectivity"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1
        except Exception:
            return False
```

### 2. Metrics Collection
```python
# src/etl_pipeline/monitoring/metrics.py
class MetricsCollector:
    def __init__(self):
        self.metrics = {
            'records_processed': 0,
            'processing_time': 0.0,
            'error_count': 0,
            'quality_score': 0.0
        }
        self.start_time = None
    
    def start_processing(self):
        """Start processing timer"""
        self.start_time = time.time()
    
    def end_processing(self):
        """End processing timer"""
        if self.start_time:
            self.metrics['processing_time'] = time.time() - self.start_time
    
    def record_batch_processing(self, batch_size: int, errors: list):
        """Record batch processing metrics"""
        self.metrics['records_processed'] += batch_size
        self.metrics['error_count'] += len(errors)
        
        # Calculate quality score
        if self.metrics['records_processed'] > 0:
            error_rate = self.metrics['error_count'] / self.metrics['records_processed']
            self.metrics['quality_score'] = max(0, (1 - error_rate) * 100)
    
    def get_metrics_summary(self) -> dict:
        """Get metrics summary"""
        return {
            'total_records_processed': self.metrics['records_processed'],
            'total_processing_time': round(self.metrics['processing_time'], 2),
            'average_processing_time_per_record': round(
                self.metrics['processing_time'] / max(1, self.metrics['records_processed']), 4
            ),
            'total_errors': self.metrics['error_count'],
            'error_rate': round(
                self.metrics['error_count'] / max(1, self.metrics['records_processed']) * 100, 2
            ),
            'quality_score': round(self.metrics['quality_score'], 2)
        }
```

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U gvrc_user -d gvrc_admin_production

# Reset password if needed
sudo -u postgres psql -c "ALTER USER gvrc_user PASSWORD 'new_password';"
```

#### 2. Memory Issues
```python
# Monitor memory usage
import psutil
process = psutil.Process()
memory_mb = process.memory_info().rss / 1024 / 1024
print(f"Memory usage: {memory_mb}MB")

# Force garbage collection
import gc
gc.collect()
```

#### 3. Data Quality Issues
```python
# Validate data quality
from src.etl_pipeline.utils.validators import DataValidator

validator = DataValidator()
result = validator.validate_facility(facility_data)
print(f"Quality score: {result.quality_score}")
print(f"Errors: {result.errors}")
```

#### 4. Performance Issues
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Analyze table statistics
ANALYZE facilities;
```

## Production Deployment

### 1. Environment Setup
```bash
# Set environment variables
export DJANGO_SETTINGS_MODULE=core.settings.production
export DATABASE_URL=postgresql://gvrc_user:password@localhost:5432/gvrc_admin_production
export LOG_LEVEL=INFO

# Create necessary directories
mkdir -p logs/etl logs/errors logs/processing
mkdir -p data/raw data/processed data/validated
mkdir -p reports/quality reports/statistics
```

### 2. Run Production Pipeline
```bash
# Execute with logging
python src/scripts/production_json_importer.py 2>&1 | tee logs/etl/pipeline_$(date +%Y%m%d_%H%M%S).log

# Run with monitoring
python -m src.etl_pipeline.pipeline --config config/production.yaml --monitor
```

### 3. Verify Deployment
```bash
# Check database records
psql -h localhost -U gvrc_user -d gvrc_admin_production -c "SELECT COUNT(*) FROM facilities;"

# Check logs
tail -f logs/etl/pipeline_*.log

# Check metrics
curl http://localhost:8080/metrics
```

---

*This technical implementation guide provides step-by-step instructions for deploying and operating the GVRC ETL pipeline in production environments.*

