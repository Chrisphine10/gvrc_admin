"""
Raw Data Lake Implementation
Immutable storage for all incoming data
"""

import json
import hashlib
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.core.files.storage import default_storage
from .models import RawDataRecord, DataSource, DataProcessingEvent
import logging

logger = logging.getLogger(__name__)


class RawDataLake:
    """Immutable raw data storage and management"""
    
    def __init__(self):
        self.storage_path = getattr(settings, 'RAW_DATA_STORAGE_PATH', 'data/raw/')
        self.metadata_db = 'raw_data_metadata'
    
    def store_raw_data(self, source_name: str, data: Dict[str, Any], 
                      metadata: Dict[str, Any] = None) -> RawDataRecord:
        """Store raw data with metadata and generate unique ID"""
        try:
            # Get or create data source
            source, created = DataSource.objects.get_or_create(
                name=source_name,
                defaults={
                    'source_type': metadata.get('source_type', 'manual'),
                    'description': metadata.get('description', ''),
                    'configuration': metadata.get('configuration', {})
                }
            )
            
            # Generate unique data ID
            data_id = self._generate_data_id(source_name, data)
            
            # Check if data already exists (immutable storage)
            if RawDataRecord.objects.filter(data_id=data_id).exists():
                logger.warning(f"Data with ID {data_id} already exists in raw data lake")
                return RawDataRecord.objects.get(data_id=data_id)
            
            # Store data in file system
            file_path = self._store_data_file(data_id, data)
            
            # Create raw data record
            raw_record = RawDataRecord.objects.create(
                source=source,
                data_id=data_id,
                raw_data=data,
                metadata=metadata or {},
                file_path=file_path,
                processing_status='pending'
            )
            
            # Log processing event
            self._log_event('data_ingested', data_id, source, {
                'file_path': file_path,
                'data_size': len(json.dumps(data))
            })
            
            logger.info(f"Stored raw data {data_id} from source {source_name}")
            return raw_record
            
        except Exception as e:
            logger.error(f"Failed to store raw data: {str(e)}")
            raise
    
    def get_raw_data(self, data_id: str) -> Optional[RawDataRecord]:
        """Retrieve raw data by ID"""
        try:
            return RawDataRecord.objects.get(data_id=data_id)
        except RawDataRecord.DoesNotExist:
            return None
    
    def get_raw_data_by_source(self, source_name: str, 
                              date_range: tuple = None) -> List[RawDataRecord]:
        """Retrieve raw data by source with optional date range"""
        try:
            source = DataSource.objects.get(name=source_name)
            queryset = RawDataRecord.objects.filter(source=source)
            
            if date_range:
                start_date, end_date = date_range
                queryset = queryset.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date
                )
            
            return list(queryset.order_by('-created_at'))
        except DataSource.DoesNotExist:
            logger.error(f"Data source {source_name} not found")
            return []
    
    def update_processing_status(self, data_id: str, status: str, 
                               error_message: str = None) -> bool:
        """Update processing status of raw data record"""
        try:
            record = RawDataRecord.objects.get(data_id=data_id)
            record.processing_status = status
            if error_message:
                record.error_message = error_message
            record.save()
            
            # Log status change event
            self._log_event('processing_status_changed', data_id, record.source, {
                'old_status': record.processing_status,
                'new_status': status,
                'error_message': error_message
            })
            
            return True
        except RawDataRecord.DoesNotExist:
            logger.error(f"Raw data record {data_id} not found")
            return False
    
    def archive_old_data(self, days_old: int = 30) -> int:
        """Archive old raw data records"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            old_records = RawDataRecord.objects.filter(
                created_at__lt=cutoff_date,
                processing_status='completed'
            )
            
            archived_count = 0
            for record in old_records:
                record.processing_status = 'archived'
                record.save()
                archived_count += 1
            
            logger.info(f"Archived {archived_count} old raw data records")
            return archived_count
            
        except Exception as e:
            logger.error(f"Failed to archive old data: {str(e)}")
            return 0
    
    def _generate_data_id(self, source_name: str, data: Dict[str, Any]) -> str:
        """Generate unique data ID based on source and content"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        data_string = json.dumps(data, sort_keys=True)
        content_hash = hashlib.md5(data_string.encode()).hexdigest()[:8]
        return f"{source_name}_{timestamp}_{content_hash}"
    
    def _store_data_file(self, data_id: str, data: Dict[str, Any]) -> str:
        """Store data in file system for backup"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.storage_path, exist_ok=True)
            
            # Generate file path
            filename = f"{data_id}.json"
            file_path = os.path.join(self.storage_path, filename)
            
            # Write data to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'data_id': data_id,
                    'data': data,
                    'stored_at': datetime.now().isoformat(),
                    'checksum': hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
                }, f, indent=2, ensure_ascii=False)
            
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to store data file: {str(e)}")
            raise
    
    def _log_event(self, event_type: str, record_id: str, source: DataSource, 
                   event_data: Dict[str, Any] = None):
        """Log data processing event"""
        try:
            DataProcessingEvent.objects.create(
                event_type=event_type,
                record_id=record_id,
                source=source,
                event_data=event_data or {},
                success=True
            )
        except Exception as e:
            logger.error(f"Failed to log event: {str(e)}")
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get raw data lake storage statistics"""
        try:
            total_records = RawDataRecord.objects.count()
            pending_records = RawDataRecord.objects.filter(processing_status='pending').count()
            completed_records = RawDataRecord.objects.filter(processing_status='completed').count()
            failed_records = RawDataRecord.objects.filter(processing_status='failed').count()
            
            # Calculate storage size
            storage_size = 0
            for record in RawDataRecord.objects.all():
                if record.file_path and os.path.exists(record.file_path):
                    storage_size += os.path.getsize(record.file_path)
            
            return {
                'total_records': total_records,
                'pending_records': pending_records,
                'completed_records': completed_records,
                'failed_records': failed_records,
                'storage_size_bytes': storage_size,
                'storage_size_mb': round(storage_size / (1024 * 1024), 2)
            }
        except Exception as e:
            logger.error(f"Failed to get storage stats: {str(e)}")
            return {}


class DataSourceManager:
    """Manage data sources for extensible integration"""
    
    def __init__(self):
        self.sources = {}
        self._load_registered_sources()
    
    def register_source(self, name: str, source_class, configuration: Dict[str, Any] = None):
        """Register new data source"""
        try:
            source, created = DataSource.objects.get_or_create(
                name=name,
                defaults={
                    'source_type': getattr(source_class, 'source_type', 'external'),
                    'description': getattr(source_class, 'description', ''),
                    'configuration': configuration or {}
                }
            )
            
            if not created:
                # Update existing source
                source.configuration = configuration or {}
                source.save()
            
            self.sources[name] = source_class
            logger.info(f"Registered data source: {name}")
            
        except Exception as e:
            logger.error(f"Failed to register source {name}: {str(e)}")
    
    def get_source(self, name: str):
        """Get registered data source"""
        return self.sources.get(name)
    
    def list_sources(self) -> List[Dict[str, Any]]:
        """List all registered data sources"""
        sources = []
        for name, source_class in self.sources.items():
            sources.append({
                'name': name,
                'class': source_class,
                'source_type': getattr(source_class, 'source_type', 'unknown'),
                'description': getattr(source_class, 'description', '')
            })
        return sources
    
    def _load_registered_sources(self):
        """Load registered sources from database"""
        try:
            for source in DataSource.objects.filter(is_active=True):
                # This would load the actual source class based on configuration
                # For now, we'll use a placeholder
                self.sources[source.name] = None
        except Exception as e:
            logger.error(f"Failed to load registered sources: {str(e)}")

