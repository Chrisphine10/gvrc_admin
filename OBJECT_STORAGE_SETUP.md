# Object Storage Integration Guide

## Overview

This project includes optional object storage integration for:
- **Query Result Caching**: Cache expensive API queries to reduce database load
- **Analytics Data Export**: Export large datasets for analysis
- **Backup Storage**: Store automated backups

## Supported Providers

- **Amazon S3** (via boto3)
- **Azure Blob Storage** (via azure-storage-blob)
- **Google Cloud Storage** (via google-cloud-storage)

## Installation

### For S3 (Amazon Web Services)
```bash
pip install boto3
```

### For Azure Blob Storage
```bash
pip install azure-storage-blob
```

### For Google Cloud Storage
```bash
pip install google-cloud-storage
```

## Configuration

### Environment Variables

Add the following to your `.env` file or environment:

#### For S3:
```bash
OBJECT_STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
AWS_CACHE_BUCKET=gvrc-api-cache
AWS_EXPORT_BUCKET=gvrc-api-exports
```

#### For Azure Blob Storage:
```bash
OBJECT_STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_CACHE_CONTAINER=gvrc-api-cache
AZURE_EXPORT_CONTAINER=gvrc-api-exports
```

#### For Google Cloud Storage:
```bash
OBJECT_STORAGE_TYPE=gcs
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
GCS_CACHE_BUCKET=gvrc-api-cache
GCS_EXPORT_BUCKET=gvrc-api-exports
```

### Django Settings (Optional)

You can also configure in `core/settings/base.py`:

```python
# Object Storage Configuration
OBJECT_STORAGE_TYPE = os.getenv('OBJECT_STORAGE_TYPE', None)  # 's3', 'azure', 'gcs', or None

# S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_CACHE_BUCKET = os.getenv('AWS_CACHE_BUCKET', '')
AWS_EXPORT_BUCKET = os.getenv('AWS_EXPORT_BUCKET', '')

# Azure Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')
AZURE_CACHE_CONTAINER = os.getenv('AZURE_CACHE_CONTAINER', '')
AZURE_EXPORT_CONTAINER = os.getenv('AZURE_EXPORT_CONTAINER', '')

# GCS Configuration
GCS_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
GCS_CACHE_BUCKET = os.getenv('GCS_CACHE_BUCKET', '')
GCS_EXPORT_BUCKET = os.getenv('GCS_EXPORT_BUCKET', '')
```

## Usage

### Query Result Caching

```python
from apps.api.utils.storage_cache import get_storage_cache

# In your view
def get_queryset(self):
    cache = get_storage_cache()
    cache_key = cache.get_cache_key(self.request.query_params, prefix='facilities')
    
    # Try cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # Execute query
    queryset = Facility.objects.select_related(...)
    # ... query logic ...
    
    # Cache result (serialize to list of dicts)
    data = list(queryset.values())
    cache.set(cache_key, data, ttl=3600)  # Cache for 1 hour
    
    return queryset
```

### Analytics Data Export

```python
from apps.api.utils.data_export import get_analytics_exporter
from datetime import datetime, timedelta

# Export contact interactions
exporter = get_analytics_exporter()
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

export_key = exporter.export_contact_interactions(start_date, end_date)
if export_key:
    print(f"Export successful: {export_key}")
```

### Custom Export

```python
from apps.api.utils.data_export import get_analytics_exporter

exporter = get_analytics_exporter()

# Export any queryset as JSON
queryset = Facility.objects.filter(is_active=True)
export_key = exporter.export_queryset_json(queryset, 'active_facilities')

# Export as CSV
export_key = exporter.export_queryset_csv(queryset, 'active_facilities')
```

## Fallback Behavior

If object storage is not configured:
- **Caching**: Falls back to Django's cache framework (Redis, Memcached, etc.)
- **Exports**: Saves files locally to `MEDIA_ROOT/exports/`

This ensures the application works even without object storage configured.

## Security Best Practices

1. **Never commit credentials**: Use environment variables or secret management services
2. **Use IAM roles**: For production, prefer IAM roles over access keys
3. **Bucket policies**: Configure bucket policies to restrict access
4. **Encryption**: Enable server-side encryption for sensitive data
5. **Access logging**: Enable access logging for audit trails

## Bucket/Container Setup

### S3 Buckets
1. Create buckets: `gvrc-api-cache` and `gvrc-api-exports`
2. Configure CORS if needed
3. Set up lifecycle policies for automatic cleanup
4. Enable versioning for important data

### Azure Containers
1. Create containers: `gvrc-api-cache` and `gvrc-api-exports`
2. Set access level (private recommended)
3. Configure retention policies

### GCS Buckets
1. Create buckets: `gvrc-api-cache` and `gvrc-api-exports`
2. Set storage class (Standard, Nearline, Coldline, Archive)
3. Configure lifecycle rules

## Monitoring

Monitor object storage usage:
- **S3**: CloudWatch metrics
- **Azure**: Azure Monitor
- **GCS**: Cloud Monitoring

Set up alerts for:
- High storage costs
- Unusual access patterns
- Failed operations

## Troubleshooting

### Common Issues

1. **ImportError**: Install the required package (boto3, azure-storage-blob, or google-cloud-storage)
2. **Access Denied**: Check credentials and bucket permissions
3. **Bucket Not Found**: Ensure buckets/containers exist and names are correct
4. **Connection Timeout**: Check network connectivity and firewall rules

### Debug Mode

Enable debug logging:
```python
import logging
logging.getLogger('apps.api.utils.storage_cache').setLevel(logging.DEBUG)
logging.getLogger('apps.api.utils.data_export').setLevel(logging.DEBUG)
```

## Cost Optimization

1. **Use appropriate storage classes**: Standard for frequent access, Nearline/Coldline for archives
2. **Set TTL on cache**: Don't cache indefinitely
3. **Compress large exports**: Use gzip compression for JSON exports
4. **Lifecycle policies**: Automatically delete old cache files
5. **Monitor usage**: Set up billing alerts

## Example: Integration in API Views

```python
# apps/api/views.py
from apps.api.utils.storage_cache import get_storage_cache

class FacilityListView(generics.ListAPIView):
    def get_queryset(self):
        cache = get_storage_cache()
        cache_key = cache.get_cache_key(self.request.query_params, prefix='facilities')
        
        # Try cache
        cached = cache.get(cache_key)
        if cached:
            # Reconstruct queryset from cached data
            facility_ids = [item['facility_id'] for item in cached]
            return Facility.objects.filter(facility_id__in=facility_ids)
        
        # Execute query
        queryset = Facility.objects.select_related(...)
        # ... filtering logic ...
        
        # Cache result
        data = list(queryset.values())
        cache.set(cache_key, data, ttl=3600)
        
        return queryset
```

## Support

For issues or questions:
1. Check logs: `logs/django.log`
2. Review this documentation
3. Check provider-specific documentation (AWS, Azure, GCS)



