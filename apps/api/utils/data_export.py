# -*- encoding: utf-8 -*-
"""
Analytics Data Export Utilities for Object Storage
Exports large datasets to S3, Azure Blob Storage, or Google Cloud Storage
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# Try to import storage clients (optional dependencies)
try:
    import boto3
    from botocore.exceptions import ClientError
    S3_AVAILABLE = True
except ImportError:
    S3_AVAILABLE = False

try:
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

try:
    from google.cloud import storage as gcs_storage
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False


class AnalyticsExporter:
    """
    Export analytics data to object storage.
    Supports S3, Azure Blob Storage, and Google Cloud Storage.
    """
    
    def __init__(self, storage_type: Optional[str] = None):
        """
        Initialize analytics exporter.
        
        Args:
            storage_type: 's3', 'azure', 'gcs', or None (auto-detect from settings)
        """
        try:
            self.storage_type = storage_type or getattr(settings, 'OBJECT_STORAGE_TYPE', None)
        except Exception:
            # Settings not configured yet
            self.storage_type = storage_type or os.getenv('OBJECT_STORAGE_TYPE', None)
        self.client = None
        self.bucket_name = None
        self.enabled = False
        
        if self.storage_type == 's3' and S3_AVAILABLE:
            self._init_s3()
        elif self.storage_type == 'azure' and AZURE_AVAILABLE:
            self._init_azure()
        elif self.storage_type == 'gcs' and GCS_AVAILABLE:
            self._init_gcs()
        else:
            logger.warning("Object storage not configured. Exports will be saved locally.")
    
    def _init_s3(self):
        """Initialize S3 client"""
        try:
            aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', os.getenv('AWS_ACCESS_KEY_ID'))
            aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', os.getenv('AWS_SECRET_ACCESS_KEY'))
            aws_region = getattr(settings, 'AWS_REGION', os.getenv('AWS_REGION', 'us-east-1'))
            self.bucket_name = getattr(settings, 'AWS_EXPORT_BUCKET', os.getenv('AWS_EXPORT_BUCKET'))
            
            if aws_access_key and aws_secret_key and self.bucket_name:
                self.client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=aws_region
                )
                self.enabled = True
                logger.info(f"S3 exporter initialized with bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize S3 exporter: {e}")
    
    def _init_azure(self):
        """Initialize Azure Blob Storage client"""
        try:
            connection_string = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', 
                                      os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
            container_name = getattr(settings, 'AZURE_EXPORT_CONTAINER', 
                                   os.getenv('AZURE_EXPORT_CONTAINER'))
            
            if connection_string and container_name:
                self.client = BlobServiceClient.from_connection_string(connection_string)
                self.bucket_name = container_name
                self.enabled = True
                logger.info(f"Azure exporter initialized with container: {container_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure exporter: {e}")
    
    def _init_gcs(self):
        """Initialize Google Cloud Storage client"""
        try:
            credentials_path = getattr(settings, 'GCS_CREDENTIALS_PATH', 
                                     os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
            bucket_name = getattr(settings, 'GCS_EXPORT_BUCKET', os.getenv('GCS_EXPORT_BUCKET'))
            
            if bucket_name:
                if credentials_path:
                    self.client = gcs_storage.Client.from_service_account_json(credentials_path)
                else:
                    self.client = gcs_storage.Client()
                self.bucket_name = bucket_name
                self.enabled = True
                logger.info(f"GCS exporter initialized with bucket: {bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GCS exporter: {e}")
    
    def export_queryset_json(self, queryset: QuerySet, export_name: str, 
                            additional_data: Optional[Dict] = None) -> Optional[str]:
        """
        Export queryset to JSON in object storage.
        
        Args:
            queryset: Django QuerySet to export
            export_name: Name for the export (used in file path)
            additional_data: Additional metadata to include
        
        Returns:
            Export key/path in object storage, or None if failed
        """
        try:
            # Convert queryset to list of dicts
            data = list(queryset.values())
            
            # Add metadata
            export_data = {
                'exported_at': timezone.now().isoformat(),
                'record_count': len(data),
                'data': data
            }
            
            if additional_data:
                export_data['metadata'] = additional_data
            
            # Generate export key
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_key = f'exports/{export_name}_{timestamp}.json'
            
            # Export to object storage
            json_data = json.dumps(export_data, default=str, indent=2)
            
            if self.enabled:
                if self.storage_type == 's3':
                    self._upload_s3(export_key, json_data)
                elif self.storage_type == 'azure':
                    self._upload_azure(export_key, json_data)
                elif self.storage_type == 'gcs':
                    self._upload_gcs(export_key, json_data)
            else:
                # Fallback: save locally
                local_path = os.path.join(settings.MEDIA_ROOT, 'exports', f'{export_name}_{timestamp}.json')
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'w') as f:
                    f.write(json_data)
                logger.info(f"Export saved locally: {local_path}")
                return local_path
            
            logger.info(f"Export successful: {export_key}")
            return export_key
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return None
    
    def export_queryset_csv(self, queryset: QuerySet, export_name: str) -> Optional[str]:
        """
        Export queryset to CSV in object storage.
        
        Args:
            queryset: Django QuerySet to export
            export_name: Name for the export
        
        Returns:
            Export key/path in object storage, or None if failed
        """
        try:
            # Convert queryset to list of dicts
            data = list(queryset.values())
            
            if not data:
                logger.warning("No data to export")
                return None
            
            # Generate CSV
            fieldnames = data[0].keys()
            csv_data = []
            csv_data.append(','.join(fieldnames))
            
            for row in data:
                csv_data.append(','.join(str(value) for value in row.values()))
            
            csv_content = '\n'.join(csv_data)
            
            # Generate export key
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_key = f'exports/{export_name}_{timestamp}.csv'
            
            # Export to object storage
            if self.enabled:
                if self.storage_type == 's3':
                    self._upload_s3(export_key, csv_content, content_type='text/csv')
                elif self.storage_type == 'azure':
                    self._upload_azure(export_key, csv_content, content_type='text/csv')
                elif self.storage_type == 'gcs':
                    self._upload_gcs(export_key, csv_content, content_type='text/csv')
            else:
                # Fallback: save locally
                local_path = os.path.join(settings.MEDIA_ROOT, 'exports', f'{export_name}_{timestamp}.csv')
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'w') as f:
                    f.write(csv_content)
                logger.info(f"Export saved locally: {local_path}")
                return local_path
            
            logger.info(f"Export successful: {export_key}")
            return export_key
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return None
    
    def _upload_s3(self, key: str, content: str, content_type: str = 'application/json'):
        """Upload to S3"""
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=content.encode('utf-8'),
            ContentType=content_type
        )
    
    def _upload_azure(self, key: str, content: str, content_type: str = 'application/json'):
        """Upload to Azure Blob Storage"""
        blob_client = self.client.get_blob_client(
            container=self.bucket_name,
            blob=key
        )
        blob_client.upload_blob(
            content.encode('utf-8'),
            overwrite=True,
            content_settings={'content_type': content_type}
        )
    
    def _upload_gcs(self, key: str, content: str, content_type: str = 'application/json'):
        """Upload to Google Cloud Storage"""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(key)
        blob.upload_from_string(
            content,
            content_type=content_type
        )
    
    def export_contact_interactions(self, start_date: datetime, end_date: datetime) -> Optional[str]:
        """
        Export contact interactions to object storage.
        
        Args:
            start_date: Start date for export
            end_date: End date for export
        
        Returns:
            Export key/path, or None if failed
        """
        from apps.analytics.models import ContactInteraction
        
        queryset = ContactInteraction.objects.filter(
            created_at__range=[start_date, end_date]
        ).order_by('-created_at')
        
        return self.export_queryset_json(
            queryset,
            'contact_interactions',
            additional_data={
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'export_type': 'contact_interactions'
            }
        )
    
    def export_referral_outcomes(self, start_date: datetime, end_date: datetime) -> Optional[str]:
        """
        Export referral outcomes to object storage.
        
        Args:
            start_date: Start date for export
            end_date: End date for export
        
        Returns:
            Export key/path, or None if failed
        """
        from apps.analytics.models import ReferralOutcome
        
        queryset = ReferralOutcome.objects.filter(
            created_at__range=[start_date, end_date]
        ).order_by('-created_at')
        
        return self.export_queryset_json(
            queryset,
            'referral_outcomes',
            additional_data={
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'export_type': 'referral_outcomes'
            }
        )


# Global instance (lazy initialization)
_exporter_instance = None

def get_analytics_exporter() -> AnalyticsExporter:
    """Get or create global analytics exporter instance"""
    global _exporter_instance
    if _exporter_instance is None:
        _exporter_instance = AnalyticsExporter()
    return _exporter_instance

