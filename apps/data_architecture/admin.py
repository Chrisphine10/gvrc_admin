"""
Data Architecture Admin Interface
Enhanced admin for data architecture management
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    DataSource, RawDataRecord, ValidatedDataRecord, EnrichedDataRecord,
    DataMart, DataQualityMetric, DataProcessingEvent, GeographicEnhancement,
    DataSwarmPrevention
)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'is_active', 'last_sync', 'sync_frequency']
    list_filter = ['source_type', 'is_active', 'sync_frequency']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'source_type', 'description', 'is_active')
        }),
        ('Configuration', {
            'fields': ('configuration', 'sync_frequency', 'last_sync')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(RawDataRecord)
class RawDataRecordAdmin(admin.ModelAdmin):
    list_display = ['data_id', 'source', 'processing_status', 'created_at', 'quality_score_display']
    list_filter = ['source', 'processing_status', 'created_at']
    search_fields = ['data_id', 'source__name']
    readonly_fields = ['data_id', 'checksum', 'created_at', 'updated_at', 'raw_data_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('data_id', 'source', 'processing_status', 'checksum')
        }),
        ('Data', {
            'fields': ('raw_data_display', 'metadata'),
            'classes': ('collapse',)
        }),
        ('File Storage', {
            'fields': ('file_path',),
            'classes': ('collapse',)
        }),
        ('Error Handling', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def quality_score_display(self, obj):
        """Display quality score with color coding"""
        if obj.processing_status == 'completed':
            return format_html(
                '<span style="color: green;">✓ Completed</span>'
            )
        elif obj.processing_status == 'failed':
            return format_html(
                '<span style="color: red;">✗ Failed</span>'
            )
        else:
            return format_html(
                '<span style="color: orange;">⏳ {}</span>',
                obj.processing_status.title()
            )
    quality_score_display.short_description = 'Status'
    
    def raw_data_display(self, obj):
        """Display raw data in a formatted way"""
        if obj.raw_data:
            import json
            formatted_data = json.dumps(obj.raw_data, indent=2)
            return format_html('<pre>{}</pre>', formatted_data)
        return '-'
    raw_data_display.short_description = 'Raw Data'


@admin.register(ValidatedDataRecord)
class ValidatedDataRecordAdmin(admin.ModelAdmin):
    list_display = ['raw_record', 'is_valid', 'quality_score', 'created_at']
    list_filter = ['is_valid', 'created_at']
    search_fields = ['raw_record__data_id']
    readonly_fields = ['created_at', 'updated_at', 'validation_details_display']
    
    fieldsets = (
        ('Validation Results', {
            'fields': ('raw_record', 'is_valid', 'quality_score')
        }),
        ('Validation Details', {
            'fields': ('validation_errors', 'validation_warnings', 'validation_rules_applied'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('validated_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def validation_details_display(self, obj):
        """Display validation details"""
        details = []
        if obj.validation_errors:
            details.append(f"Errors: {len(obj.validation_errors)}")
        if obj.validation_warnings:
            details.append(f"Warnings: {len(obj.validation_warnings)}")
        if obj.validation_rules_applied:
            details.append(f"Rules: {len(obj.validation_rules_applied)}")
        
        return ', '.join(details) if details else 'No details'
    validation_details_display.short_description = 'Validation Summary'


@admin.register(EnrichedDataRecord)
class EnrichedDataRecordAdmin(admin.ModelAdmin):
    list_display = ['validated_record', 'final_quality_score', 'enhancements_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['validated_record__raw_record__data_id']
    readonly_fields = ['created_at', 'updated_at', 'enhancements_display']
    
    fieldsets = (
        ('Enrichment Results', {
            'fields': ('validated_record', 'final_quality_score', 'enrichment_applied')
        }),
        ('AI Enhancements', {
            'fields': ('ai_enhancements', 'geographic_data'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('enriched_data',),
            'classes': ('collapse',)
        }),
        ('Duplicate Detection', {
            'fields': ('duplicate_flags',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def enhancements_count(self, obj):
        """Count of enhancements applied"""
        return len(obj.enrichment_applied) if obj.enrichment_applied else 0
    enhancements_count.short_description = 'Enhancements'
    
    def enhancements_display(self, obj):
        """Display enhancements in a readable format"""
        if obj.enrichment_applied:
            return format_html(
                '<ul>{}</ul>',
                ''.join(f'<li>{enhancement}</li>' for enhancement in obj.enrichment_applied)
            )
        return 'No enhancements'
    enhancements_display.short_description = 'Applied Enhancements'


@admin.register(DataMart)
class DataMartAdmin(admin.ModelAdmin):
    list_display = ['enriched_record', 'mart_type', 'is_served', 'created_at']
    list_filter = ['mart_type', 'is_served', 'created_at']
    search_fields = ['enriched_record__validated_record__raw_record__data_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Data Mart Information', {
            'fields': ('enriched_record', 'mart_type', 'is_served')
        }),
        ('Serving Configuration', {
            'fields': ('serving_metadata',),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('mart_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DataQualityMetric)
class DataQualityMetricAdmin(admin.ModelAdmin):
    list_display = ['record_type', 'metric_type', 'metric_value', 'threshold', 'passed', 'created_at']
    list_filter = ['record_type', 'metric_type', 'passed', 'created_at']
    search_fields = ['record_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('record_type', 'record_id', 'metric_type', 'metric_value', 'threshold', 'passed')
        }),
        ('Details', {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DataProcessingEvent)
class DataProcessingEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'record_id', 'source', 'success', 'created_at']
    list_filter = ['event_type', 'success', 'source', 'created_at']
    search_fields = ['record_id', 'source__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('event_type', 'record_id', 'source', 'success')
        }),
        ('Event Data', {
            'fields': ('event_data', 'processing_time', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(GeographicEnhancement)
class GeographicEnhancementAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'county', 'constituency', 'ward', 'confidence_score', 'created_at']
    list_filter = ['county', 'geocoding_service', 'created_at']
    search_fields = ['record_id', 'original_address', 'county', 'constituency', 'ward']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Geographic Information', {
            'fields': ('record_id', 'original_address', 'enhanced_address')
        }),
        ('Location Hierarchy', {
            'fields': ('county', 'constituency', 'ward')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude', 'accuracy_level')
        }),
        ('Enhancement Details', {
            'fields': ('geocoding_service', 'confidence_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DataSwarmPrevention)
class DataSwarmPreventionAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'duplicate_group_id', 'similarity_score', 'action_taken', 'created_at']
    list_filter = ['action_taken', 'match_strategy', 'created_at']
    search_fields = ['record_id', 'duplicate_group_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Prevention Information', {
            'fields': ('record_id', 'duplicate_group_id', 'similarity_score', 'match_strategy', 'action_taken')
        }),
        ('Details', {
            'fields': ('prevention_details',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


# Custom admin site configuration
admin.site.site_header = "GVRC Data Architecture Admin"
admin.site.site_title = "Data Architecture"
admin.site.index_title = "Enhanced Data Architecture Management"

