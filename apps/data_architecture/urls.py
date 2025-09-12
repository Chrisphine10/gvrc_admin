"""
Data Architecture URL Configuration
API endpoints for enhanced data architecture
"""

from django.urls import path
from . import views

app_name = 'data_architecture'

urlpatterns = [
    # Data Ingestion Endpoints
    path('ingest/facility/', views.ingest_facility_data, name='ingest_facility_data'),
    path('ingest/mobile/', views.mobile_data_collection, name='mobile_data_collection'),
    
    # Data Source Management
    path('sources/', views.get_data_sources, name='get_data_sources'),
    path('sources/register/', views.register_data_source, name='register_data_source'),
    
    # Monitoring and Health
    path('health/', views.get_system_health, name='get_system_health'),
    path('health/check/', views.health_check, name='health_check'),
    path('quality/report/', views.get_data_quality_report, name='get_data_quality_report'),
    path('quality/metrics/', views.get_quality_metrics, name='get_quality_metrics'),
    
    # Statistics and Analytics
    path('stats/processing/', views.get_processing_stats, name='get_processing_stats'),
    path('stats/raw-data/', views.get_raw_data_stats, name='get_raw_data_stats'),
    path('stats/reset/', views.reset_processing_stats, name='reset_processing_stats'),
    
    # Processing Events
    path('events/', views.get_processing_events, name='get_processing_events'),
    
    # Data Management
    path('archive/', views.archive_old_data, name='archive_old_data'),
    
    # Data Quality Monitoring
    path('quality/check/', views.run_quality_checks, name='run_quality_checks'),
    path('quality/dashboard/', views.get_quality_dashboard, name='get_quality_dashboard'),
    path('quality/gates/setup/', views.setup_quality_gates, name='setup_quality_gates'),
    
    # Data Population
    path('populate/all/', views.populate_sample_data, name='populate_sample_data'),
    path('populate/geography/', views.populate_geography_data, name='populate_geography_data'),
    path('populate/facilities/', views.populate_facilities_data, name='populate_facilities_data'),
    
    # Data Source Integration
    path('sources/', views.get_data_sources, name='get_data_sources'),
    path('sources/create/', views.create_data_source, name='create_data_source'),
    path('sources/<int:source_id>/test/', views.test_data_source, name='test_data_source'),
    path('sources/<int:source_id>/ingest/', views.ingest_from_source, name='ingest_from_source'),
    
    # Intelligent Data Scraping
    path('scrape/discover/', views.discover_data_files, name='discover_data_files'),
    path('scrape/process/', views.process_all_files, name='process_all_files'),
    path('scrape/clear-sample/', views.clear_sample_data, name='clear_sample_data'),
    
    # PDF Data Extraction
    path('extract/pdfs/', views.extract_facilities_pdfs, name='extract_facilities_pdfs'),
]

