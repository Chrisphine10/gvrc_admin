"""
Enhanced Data Architecture Models
Implements multi-layer data architecture beyond medallion pattern
"""

from django.db import models
from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedModel, UserTrackedModel
# Use Django's built-in JSONField (available in Django 3.1+)
import json
import hashlib
from datetime import datetime

User = get_user_model()


class DataSource(TimeStampedModel):
    """Data source registry for extensible integration"""
    name = models.CharField(max_length=100, unique=True)
    source_type = models.CharField(max_length=50, choices=[
        ('manual', 'Manual Entry'),
        ('csv', 'CSV Import'),
        ('api', 'API Integration'),
        ('mobile', 'Mobile App'),
        ('external', 'External System'),
        ('web_scraping', 'Web Scraping'),
        ('iot', 'IoT Device'),
    ])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_frequency = models.CharField(max_length=20, choices=[
        ('realtime', 'Real-time'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('manual', 'Manual'),
    ], default='manual')
    
    class Meta:
        db_table = 'data_sources'
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
    
    def __str__(self):
        return f"{self.name} ({self.source_type})"


class RawDataRecord(TimeStampedModel):
    """Immutable raw data storage - Layer 1"""
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    data_id = models.CharField(max_length=100, unique=True)
    raw_data = models.JSONField()
    metadata = models.JSONField(default=dict)
    checksum = models.CharField(max_length=64, unique=True)
    file_path = models.CharField(max_length=500, blank=True)
    processing_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
    ], default='pending')
    error_message = models.TextField(blank=True)
    
    class Meta:
        db_table = 'raw_data_records'
        verbose_name = 'Raw Data Record'
        verbose_name_plural = 'Raw Data Records'
        indexes = [
            models.Index(fields=['source', 'processing_status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['checksum']),
        ]
    
    def __str__(self):
        return f"Raw Data {self.data_id} from {self.source.name}"
    
    def save(self, *args, **kwargs):
        # Generate checksum for data integrity
        if not self.checksum:
            data_string = json.dumps(self.raw_data, sort_keys=True)
            self.checksum = hashlib.sha256(data_string.encode()).hexdigest()
        super().save(*args, **kwargs)


class ValidatedDataRecord(TimeStampedModel):
    """Quality-gated data storage - Layer 2"""
    raw_record = models.OneToOneField(RawDataRecord, on_delete=models.CASCADE)
    validated_data = models.JSONField()
    quality_score = models.FloatField(default=0.0)
    validation_errors = models.JSONField(default=list, blank=True)
    validation_warnings = models.JSONField(default=list, blank=True)
    validation_rules_applied = models.JSONField(default=list, blank=True)
    is_valid = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'validated_data_records'
        verbose_name = 'Validated Data Record'
        verbose_name_plural = 'Validated Data Records'
        indexes = [
            models.Index(fields=['is_valid', 'quality_score']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Validated Data {self.raw_record.data_id}"


class EnrichedDataRecord(TimeStampedModel):
    """AI-enhanced data storage - Layer 3"""
    validated_record = models.OneToOneField(ValidatedDataRecord, on_delete=models.CASCADE)
    enriched_data = models.JSONField()
    enrichment_applied = models.JSONField(default=list, blank=True)
    ai_enhancements = models.JSONField(default=dict, blank=True)
    geographic_data = models.JSONField(default=dict, blank=True)
    duplicate_flags = models.JSONField(default=list, blank=True)
    final_quality_score = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'enriched_data_records'
        verbose_name = 'Enriched Data Record'
        verbose_name_plural = 'Enriched Data Records'
        indexes = [
            models.Index(fields=['final_quality_score']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Enriched Data {self.validated_record.raw_record.data_id}"


class DataMart(TimeStampedModel):
    """Business-ready data storage - Layer 4"""
    enriched_record = models.OneToOneField(EnrichedDataRecord, on_delete=models.CASCADE)
    mart_data = models.JSONField()
    mart_type = models.CharField(max_length=50, choices=[
        ('facilities', 'Facilities'),
        ('geographic', 'Geographic'),
        ('analytics', 'Analytics'),
        ('mobile', 'Mobile'),
        ('reporting', 'Reporting'),
    ])
    is_served = models.BooleanField(default=False)
    serving_metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'data_marts'
        verbose_name = 'Data Mart'
        verbose_name_plural = 'Data Marts'
        indexes = [
            models.Index(fields=['mart_type', 'is_served']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Data Mart {self.mart_type} - {self.enriched_record.validated_record.raw_record.data_id}"


class DataQualityMetric(TimeStampedModel):
    """Data quality metrics tracking"""
    record_type = models.CharField(max_length=50, choices=[
        ('raw', 'Raw Data'),
        ('validated', 'Validated Data'),
        ('enriched', 'Enriched Data'),
        ('mart', 'Data Mart'),
    ])
    record_id = models.CharField(max_length=100)
    metric_type = models.CharField(max_length=50, choices=[
        ('completeness', 'Completeness'),
        ('accuracy', 'Accuracy'),
        ('consistency', 'Consistency'),
        ('timeliness', 'Timeliness'),
        ('uniqueness', 'Uniqueness'),
    ])
    metric_value = models.FloatField()
    threshold = models.FloatField()
    passed = models.BooleanField()
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'data_quality_metrics'
        verbose_name = 'Data Quality Metric'
        verbose_name_plural = 'Data Quality Metrics'
        indexes = [
            models.Index(fields=['record_type', 'metric_type']),
            models.Index(fields=['passed', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.metric_type} for {self.record_type} {self.record_id}"


class DataProcessingEvent(TimeStampedModel):
    """Event tracking for real-time processing"""
    event_type = models.CharField(max_length=50, choices=[
        ('data_ingested', 'Data Ingested'),
        ('data_validated', 'Data Validated'),
        ('data_enriched', 'Data Enriched'),
        ('data_served', 'Data Served'),
        ('quality_alert', 'Quality Alert'),
        ('duplicate_detected', 'Duplicate Detected'),
        ('error_occurred', 'Error Occurred'),
    ])
    record_id = models.CharField(max_length=100)
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    event_data = models.JSONField(default=dict, blank=True)
    processing_time = models.FloatField(null=True, blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        db_table = 'data_processing_events'
        verbose_name = 'Data Processing Event'
        verbose_name_plural = 'Data Processing Events'
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['source', 'success']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.record_id}"


class GeographicEnhancement(TimeStampedModel):
    """AI-powered geographic data enhancement"""
    record_id = models.CharField(max_length=100, unique=True)
    original_address = models.TextField()
    enhanced_address = models.TextField(blank=True)
    county = models.CharField(max_length=100, blank=True)
    constituency = models.CharField(max_length=100, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    accuracy_level = models.CharField(max_length=50, blank=True)
    geocoding_service = models.CharField(max_length=50, blank=True)
    confidence_score = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'geographic_enhancements'
        verbose_name = 'Geographic Enhancement'
        verbose_name_plural = 'Geographic Enhancements'
        indexes = [
            models.Index(fields=['county', 'constituency']),
            models.Index(fields=['confidence_score']),
        ]
    
    def __str__(self):
        return f"Geographic Enhancement for {self.record_id}"


class DataSwarmPrevention(TimeStampedModel):
    """Data swarm prevention tracking"""
    record_id = models.CharField(max_length=100)
    duplicate_group_id = models.CharField(max_length=100, blank=True)
    similarity_score = models.FloatField(default=0.0)
    match_strategy = models.CharField(max_length=50, blank=True)
    action_taken = models.CharField(max_length=50, choices=[
        ('merged', 'Merged'),
        ('kept_original', 'Kept Original'),
        ('flagged', 'Flagged'),
        ('rejected', 'Rejected'),
    ], blank=True)
    prevention_details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'data_swarm_prevention'
        verbose_name = 'Data Swarm Prevention'
        verbose_name_plural = 'Data Swarm Prevention Records'
        indexes = [
            models.Index(fields=['duplicate_group_id']),
            models.Index(fields=['similarity_score']),
        ]
    
    def __str__(self):
        return f"Swarm Prevention for {self.record_id}"
