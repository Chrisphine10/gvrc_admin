"""
Data Architecture Signals
Event-driven processing and notifications
"""

import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import (
    RawDataRecord, ValidatedDataRecord, EnrichedDataRecord, 
    DataMart, DataProcessingEvent, DataQualityMetric
)
from .enhanced_etl_pipeline import DataArchitectureManager

logger = logging.getLogger(__name__)


@receiver(post_save, sender=RawDataRecord)
def raw_data_record_created(sender, instance, created, **kwargs):
    """Handle raw data record creation"""
    if created:
        logger.info(f"New raw data record created: {instance.data_id}")
        
        # Update cache
        cache_key = f"raw_data_stats_{instance.source.name}"
        cache.delete(cache_key)
        
        # Log processing event
        DataProcessingEvent.objects.create(
            event_type='data_ingested',
            record_id=instance.data_id,
            source=instance.source,
            success=True,
            event_data={
                'data_size': len(str(instance.raw_data)),
                'file_path': instance.file_path
            }
        )


@receiver(post_save, sender=ValidatedDataRecord)
def validated_data_record_created(sender, instance, created, **kwargs):
    """Handle validated data record creation"""
    if created:
        logger.info(f"New validated data record created: {instance.raw_record.data_id}")
        
        # Update raw record status
        instance.raw_record.processing_status = 'completed'
        instance.raw_record.save()
        
        # Create quality metrics
        _create_quality_metrics(instance)
        
        # Log processing event
        DataProcessingEvent.objects.create(
            event_type='data_validated',
            record_id=instance.raw_record.data_id,
            source=instance.raw_record.source,
            success=instance.is_valid,
            event_data={
                'quality_score': instance.quality_score,
                'validation_errors': len(instance.validation_errors),
                'validation_warnings': len(instance.validation_warnings)
            }
        )


@receiver(post_save, sender=EnrichedDataRecord)
def enriched_data_record_created(sender, instance, created, **kwargs):
    """Handle enriched data record creation"""
    if created:
        logger.info(f"New enriched data record created: {instance.validated_record.raw_record.data_id}")
        
        # Log processing event
        DataProcessingEvent.objects.create(
            event_type='data_enriched',
            record_id=instance.validated_record.raw_record.data_id,
            source=instance.validated_record.raw_record.source,
            success=True,
            event_data={
                'enhancements_applied': instance.enrichment_applied,
                'final_quality_score': instance.final_quality_score
            }
        )


@receiver(post_save, sender=DataMart)
def data_mart_created(sender, instance, created, **kwargs):
    """Handle data mart creation"""
    if created:
        logger.info(f"New data mart created: {instance.mart_type}")
        
        # Log processing event
        DataProcessingEvent.objects.create(
            event_type='data_served',
            record_id=instance.enriched_record.validated_record.raw_record.data_id,
            source=instance.enriched_record.validated_record.raw_record.source,
            success=True,
            event_data={
                'mart_type': instance.mart_type,
                'is_served': instance.is_served
            }
        )


@receiver(pre_save, sender=RawDataRecord)
def raw_data_record_pre_save(sender, instance, **kwargs):
    """Handle raw data record before save"""
    # Generate checksum if not exists
    if not instance.checksum and instance.raw_data:
        import hashlib
        import json
        data_string = json.dumps(instance.raw_data, sort_keys=True)
        instance.checksum = hashlib.sha256(data_string.encode()).hexdigest()


def _create_quality_metrics(validated_record):
    """Create quality metrics for validated record"""
    try:
        # Create completeness metric
        DataQualityMetric.objects.create(
            record_type='validated',
            record_id=validated_record.raw_record.data_id,
            metric_type='completeness',
            metric_value=validated_record.quality_score,
            threshold=0.8,
            passed=validated_record.quality_score >= 0.8,
            details={
                'validation_errors': validated_record.validation_errors,
                'validation_warnings': validated_record.validation_warnings
            }
        )
        
        # Create accuracy metric (simplified)
        accuracy_score = 1.0 if validated_record.is_valid else 0.5
        DataQualityMetric.objects.create(
            record_type='validated',
            record_id=validated_record.raw_record.data_id,
            metric_type='accuracy',
            metric_value=accuracy_score,
            threshold=0.9,
            passed=accuracy_score >= 0.9
        )
        
        # Create consistency metric (simplified)
        consistency_score = 1.0 if not validated_record.validation_warnings else 0.8
        DataQualityMetric.objects.create(
            record_type='validated',
            record_id=validated_record.raw_record.data_id,
            metric_type='consistency',
            metric_value=consistency_score,
            threshold=0.95,
            passed=consistency_score >= 0.95
        )
        
    except Exception as e:
        logger.error(f"Failed to create quality metrics: {e}")


# Custom signal handlers for specific events
@receiver(post_save, sender=DataProcessingEvent)
def processing_event_created(sender, instance, created, **kwargs):
    """Handle processing event creation"""
    if created and not instance.success:
        logger.warning(f"Processing event failed: {instance.event_type} - {instance.record_id}")
        
        # Update cache for error tracking
        cache_key = f"processing_errors_{instance.source.name}"
        error_count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, error_count, 3600)  # Cache for 1 hour


# Signal for data quality alerts
def trigger_quality_alert(record_id, metric_type, score, threshold):
    """Trigger quality alert"""
    logger.warning(f"Quality alert: {metric_type} score {score} below threshold {threshold} for record {record_id}")
    
    # This could trigger notifications, emails, etc.
    # For now, just log the alert
    pass


# Signal for duplicate detection
def trigger_duplicate_alert(record_id, duplicate_count, similarity_score):
    """Trigger duplicate detection alert"""
    logger.warning(f"Duplicate alert: {duplicate_count} duplicates found for record {record_id} with similarity {similarity_score}")
    
    # This could trigger notifications, manual review, etc.
    pass

