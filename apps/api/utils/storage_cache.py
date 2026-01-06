# -*- encoding: utf-8 -*-
"""
Object Storage Cache Utilities for API Query Results
Supports S3, Azure Blob Storage, and Google Cloud Storage
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Try to import storage clients (optional dependencies)
try:
    import boto3
    from botocore.exceptions import ClientError
    S3_AVAILABLE = True
except ImportError:
    S3_AVAILABLE = False
    logger.warning("boto3 not installed. S3 caching will be disabled.")

try:
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    logger.warning("azure-storage-blob not installed. Azure caching will be disabled.")

try:
    from google.cloud import storage as gcs_storage
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False
    logger.warning("google-cloud-storage not installed. GCS caching will be disabled.")


class ObjectStorageCache:
    """
    Cache query results to object storage for better performance.
    Supports S3, Azure Blob Storage, and Google Cloud Storage.
    Falls back to Django cache if object storage is not configured.
    """
    
    def __init__(self, storage_type: Optional[str] = None):
        """
        Initialize object storage cache.
        
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
            logger.info("Object storage not configured. Using Django cache fallback.")
    
    def _init_s3(self):
        """Initialize S3 client"""
        try:
            aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', os.getenv('AWS_ACCESS_KEY_ID'))
            aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', os.getenv('AWS_SECRET_ACCESS_KEY'))
            aws_region = getattr(settings, 'AWS_REGION', os.getenv('AWS_REGION', 'us-east-1'))
            self.bucket_name = getattr(settings, 'AWS_CACHE_BUCKET', os.getenv('AWS_CACHE_BUCKET'))
            
            if aws_access_key and aws_secret_key and self.bucket_name:
                self.client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=aws_region
                )
                self.enabled = True
                logger.info(f"S3 cache initialized with bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize S3 cache: {e}")
    
    def _init_azure(self):
        """Initialize Azure Blob Storage client"""
        try:
            connection_string = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', 
                                      os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
            container_name = getattr(settings, 'AZURE_CACHE_CONTAINER', 
                                   os.getenv('AZURE_CACHE_CONTAINER'))
            
            if connection_string and container_name:
                self.client = BlobServiceClient.from_connection_string(connection_string)
                self.bucket_name = container_name
                self.enabled = True
                logger.info(f"Azure cache initialized with container: {container_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure cache: {e}")
    
    def _init_gcs(self):
        """Initialize Google Cloud Storage client"""
        try:
            credentials_path = getattr(settings, 'GCS_CREDENTIALS_PATH', 
                                     os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
            bucket_name = getattr(settings, 'GCS_CACHE_BUCKET', os.getenv('GCS_CACHE_BUCKET'))
            
            if bucket_name:
                if credentials_path:
                    self.client = gcs_storage.Client.from_service_account_json(credentials_path)
                else:
                    self.client = gcs_storage.Client()  # Use default credentials
                self.bucket_name = bucket_name
                self.enabled = True
                logger.info(f"GCS cache initialized with bucket: {bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GCS cache: {e}")
    
    def get_cache_key(self, query_params: Dict[str, Any], prefix: str = 'query') -> str:
        """
        Generate cache key from query parameters.
        
        Args:
            query_params: Dictionary of query parameters
            prefix: Prefix for cache key (e.g., 'query', 'facility', 'analytics')
        
        Returns:
            MD5 hash of sorted query parameters
        """
        # Sort parameters for consistent hashing
        key_string = json.dumps(query_params, sort_keys=True, default=str)
        hash_value = hashlib.md5(key_string.encode()).hexdigest()
        return f"{prefix}/{hash_value}.json"
    
    def get(self, cache_key: str, default: Any = None) -> Optional[Any]:
        """
        Retrieve cached data from object storage.
        
        Args:
            cache_key: Cache key (path in object storage)
            default: Default value if not found
        
        Returns:
            Cached data or default value
        """
        if not self.enabled:
            # Fallback to Django cache
            return cache.get(cache_key, default)
        
        try:
            if self.storage_type == 's3':
                return self._get_s3(cache_key)
            elif self.storage_type == 'azure':
                return self._get_azure(cache_key)
            elif self.storage_type == 'gcs':
                return self._get_gcs(cache_key)
        except Exception as e:
            logger.warning(f"Failed to retrieve from object storage: {e}. Using Django cache fallback.")
            return cache.get(cache_key, default)
        
        return default
    
    def _get_s3(self, cache_key: str) -> Optional[Any]:
        """Retrieve from S3"""
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=cache_key
            )
            data = json.loads(response['Body'].read().decode('utf-8'))
            
            # Check TTL if metadata exists
            if 'Metadata' in response and 'ttl' in response['Metadata']:
                ttl = int(response['Metadata']['ttl'])
                # TTL checking would require storing timestamp, simplified here
                pass
            
            return data
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise
    
    def _get_azure(self, cache_key: str) -> Optional[Any]:
        """Retrieve from Azure Blob Storage"""
        try:
            blob_client = self.client.get_blob_client(
                container=self.bucket_name,
                blob=cache_key
            )
            data = blob_client.download_blob().readall().decode('utf-8')
            return json.loads(data)
        except Exception as e:
            if 'BlobNotFound' in str(e):
                return None
            raise
    
    def _get_gcs(self, cache_key: str) -> Optional[Any]:
        """Retrieve from Google Cloud Storage"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(cache_key)
            
            if not blob.exists():
                return None
            
            data = blob.download_as_text()
            return json.loads(data)
        except Exception as e:
            if '404' in str(e):
                return None
            raise
    
    def set(self, cache_key: str, data: Any, ttl: int = 3600) -> bool:
        """
        Store data in object storage cache.
        
        Args:
            cache_key: Cache key (path in object storage)
            data: Data to cache (must be JSON serializable)
            ttl: Time to live in seconds (for metadata, actual expiration handled separately)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            # Fallback to Django cache
            cache.set(cache_key, data, ttl)
            return True
        
        try:
            json_data = json.dumps(data, default=str)
            
            if self.storage_type == 's3':
                return self._set_s3(cache_key, json_data, ttl)
            elif self.storage_type == 'azure':
                return self._set_azure(cache_key, json_data, ttl)
            elif self.storage_type == 'gcs':
                return self._set_gcs(cache_key, json_data, ttl)
        except Exception as e:
            logger.warning(f"Failed to store in object storage: {e}. Using Django cache fallback.")
            cache.set(cache_key, data, ttl)
            return False
        
        return True
    
    def _set_s3(self, cache_key: str, json_data: str, ttl: int) -> bool:
        """Store in S3"""
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=cache_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json',
                Metadata={'ttl': str(ttl), 'cached_at': str(datetime.now().isoformat())}
            )
            return True
        except Exception as e:
            logger.error(f"S3 put_object failed: {e}")
            return False
    
    def _set_azure(self, cache_key: str, json_data: str, ttl: int) -> bool:
        """Store in Azure Blob Storage"""
        try:
            blob_client = self.client.get_blob_client(
                container=self.bucket_name,
                blob=cache_key
            )
            blob_client.upload_blob(
                json_data.encode('utf-8'),
                overwrite=True,
                metadata={'ttl': str(ttl), 'cached_at': datetime.now().isoformat()}
            )
            return True
        except Exception as e:
            logger.error(f"Azure upload_blob failed: {e}")
            return False
    
    def _set_gcs(self, cache_key: str, json_data: str, ttl: int) -> bool:
        """Store in Google Cloud Storage"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(cache_key)
            blob.upload_from_string(
                json_data,
                content_type='application/json'
            )
            # Set metadata
            blob.metadata = {'ttl': str(ttl), 'cached_at': datetime.now().isoformat()}
            blob.patch()
            return True
        except Exception as e:
            logger.error(f"GCS upload_from_string failed: {e}")
            return False
    
    def delete(self, cache_key: str) -> bool:
        """
        Delete cached data from object storage.
        
        Args:
            cache_key: Cache key to delete
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            cache.delete(cache_key)
            return True
        
        try:
            if self.storage_type == 's3':
                self.client.delete_object(Bucket=self.bucket_name, Key=cache_key)
            elif self.storage_type == 'azure':
                blob_client = self.client.get_blob_client(
                    container=self.bucket_name,
                    blob=cache_key
                )
                blob_client.delete_blob()
            elif self.storage_type == 'gcs':
                bucket = self.client.bucket(self.bucket_name)
                blob = bucket.blob(cache_key)
                blob.delete()
            return True
        except Exception as e:
            logger.warning(f"Failed to delete from object storage: {e}")
            return False


# Global instance (lazy initialization)
_storage_cache_instance = None

def get_storage_cache() -> ObjectStorageCache:
    """Get or create global storage cache instance"""
    global _storage_cache_instance
    if _storage_cache_instance is None:
        _storage_cache_instance = ObjectStorageCache()
    return _storage_cache_instance

