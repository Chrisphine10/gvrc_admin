"""
Data Architecture API Views
RESTful API for data architecture management
"""

import logging
import time
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .enhanced_etl_pipeline import DataArchitectureManager
from .raw_data_lake import RawDataLake
from .data_quality_monitor import quality_monitor
from .data_source_integration import integration_manager
from .data_population import data_populator
from .intelligent_data_scraper import intelligent_scraper
from .models import DataSource, DataProcessingEvent, DataQualityMetric
import json

logger = logging.getLogger(__name__)


class DataArchitectureAPIView(View):
    """Base API view for data architecture"""
    
    def __init__(self):
        self.architecture_manager = DataArchitectureManager()
        self.raw_data_lake = RawDataLake()
    
    def get(self, request):
        """Handle GET requests"""
        return JsonResponse({'message': 'Data Architecture API'})
    
    def post(self, request):
        """Handle POST requests"""
        return JsonResponse({'message': 'POST not implemented'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def ingest_facility_data(request):
    """API endpoint for facility data ingestion"""
    try:
        data = request.data
        source_name = data.get('source_name', 'manual')
        source_type = data.get('source_type', 'manual')
        facility_data = data.get('data', [])
        
        if not facility_data:
            return Response({
                'error': 'No data provided',
                'details': 'Please provide facility data in the "data" field'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process data through enhanced ETL pipeline
        architecture_manager = DataArchitectureManager()
        result = architecture_manager.ingest_data(source_name, facility_data, source_type)
        
        if result['success']:
            return Response({
                'message': 'Data ingested successfully',
                'quality_score': result.get('quality_score', 0),
                'processing_time': result.get('processing_time', 0),
                'records_processed': result.get('records_processed', 0),
                'records_successful': result.get('records_successful', 0),
                'records_failed': result.get('records_failed', 0),
                'duplicates_prevented': result.get('duplicates_prevented', 0)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': 'Data ingestion failed',
                'details': result.get('errors', []),
                'warnings': result.get('warnings', [])
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Facility data ingestion failed: {e}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_data_quality_report(request):
    """Get comprehensive data quality report"""
    try:
        architecture_manager = DataArchitectureManager()
        report = architecture_manager.get_data_quality_report()
        
        return Response(report, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get quality report: {e}")
        return Response({
            'error': 'Failed to generate quality report',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_system_health(request):
    """Get system health status"""
    try:
        architecture_manager = DataArchitectureManager()
        health = architecture_manager.get_system_health()
        
        return Response(health, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get system health: {e}")
        return Response({
            'error': 'Failed to get system health',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_processing_stats(request):
    """Get data processing statistics"""
    try:
        architecture_manager = DataArchitectureManager()
        stats = architecture_manager.etl_pipeline.get_processing_stats()
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get processing stats: {e}")
        return Response({
            'error': 'Failed to get processing statistics',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_raw_data_stats(request):
    """Get raw data lake statistics"""
    try:
        raw_data_lake = RawDataLake()
        stats = raw_data_lake.get_storage_stats()
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get raw data stats: {e}")
        return Response({
            'error': 'Failed to get raw data statistics',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_data_sources(request):
    """Get list of data sources"""
    try:
        sources = DataSource.objects.filter(is_active=True).values(
            'id', 'name', 'source_type', 'description', 'last_sync', 'sync_frequency'
        )
        
        return Response(list(sources), status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get data sources: {e}")
        return Response({
            'error': 'Failed to get data sources',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_data_source(request):
    """Register new data source"""
    try:
        data = request.data
        name = data.get('name')
        source_type = data.get('source_type', 'manual')
        description = data.get('description', '')
        configuration = data.get('configuration', {})
        
        if not name:
            return Response({
                'error': 'Source name is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update data source
        source, created = DataSource.objects.get_or_create(
            name=name,
            defaults={
                'source_type': source_type,
                'description': description,
                'configuration': configuration
            }
        )
        
        if not created:
            # Update existing source
            source.source_type = source_type
            source.description = description
            source.configuration = configuration
            source.save()
        
        return Response({
            'message': 'Data source registered successfully',
            'source_id': source.id,
            'created': created
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to register data source: {e}")
        return Response({
            'error': 'Failed to register data source',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_processing_events(request):
    """Get recent processing events"""
    try:
        limit = int(request.GET.get('limit', 50))
        event_type = request.GET.get('event_type')
        source_id = request.GET.get('source_id')
        
        events = DataProcessingEvent.objects.all().order_by('-created_at')
        
        if event_type:
            events = events.filter(event_type=event_type)
        
        if source_id:
            events = events.filter(source_id=source_id)
        
        events = events[:limit]
        
        event_data = []
        for event in events:
            event_data.append({
                'id': event.id,
                'event_type': event.event_type,
                'record_id': event.record_id,
                'source_name': event.source.name,
                'success': event.success,
                'processing_time': event.processing_time,
                'created_at': event.created_at,
                'error_message': event.error_message
            })
        
        return Response(event_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get processing events: {e}")
        return Response({
            'error': 'Failed to get processing events',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quality_metrics(request):
    """Get data quality metrics"""
    try:
        record_type = request.GET.get('record_type')
        metric_type = request.GET.get('metric_type')
        limit = int(request.GET.get('limit', 100))
        
        metrics = DataQualityMetric.objects.all().order_by('-created_at')
        
        if record_type:
            metrics = metrics.filter(record_type=record_type)
        
        if metric_type:
            metrics = metrics.filter(metric_type=metric_type)
        
        metrics = metrics[:limit]
        
        metric_data = []
        for metric in metrics:
            metric_data.append({
                'id': metric.id,
                'record_type': metric.record_type,
                'record_id': metric.record_id,
                'metric_type': metric.metric_type,
                'metric_value': metric.metric_value,
                'threshold': metric.threshold,
                'passed': metric.passed,
                'created_at': metric.created_at,
                'details': metric.details
            })
        
        return Response(metric_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to get quality metrics: {e}")
        return Response({
            'error': 'Failed to get quality metrics',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_processing_stats(request):
    """Reset processing statistics"""
    try:
        architecture_manager = DataArchitectureManager()
        architecture_manager.etl_pipeline.reset_stats()
        
        return Response({
            'message': 'Processing statistics reset successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to reset processing stats: {e}")
        return Response({
            'error': 'Failed to reset processing statistics',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def archive_old_data(request):
    """Archive old raw data records"""
    try:
        days_old = int(request.data.get('days_old', 30))
        
        raw_data_lake = RawDataLake()
        archived_count = raw_data_lake.archive_old_data(days_old)
        
        return Response({
            'message': f'Archived {archived_count} old data records',
            'archived_count': archived_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Failed to archive old data: {e}")
        return Response({
            'error': 'Failed to archive old data',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Mobile API endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mobile_data_collection(request):
    """Mobile app data collection endpoint"""
    try:
        data = request.data
        source_name = 'mobile_app'
        source_type = 'mobile'
        
        # Extract facility data from mobile request
        facility_data = [data] if isinstance(data, dict) else data
        
        # Process through ETL pipeline
        architecture_manager = DataArchitectureManager()
        result = architecture_manager.ingest_data(source_name, facility_data, source_type)
        
        if result['success']:
            return Response({
                'status': 'success',
                'message': 'Data collected successfully',
                'quality_score': result.get('quality_score', 0),
                'record_id': result.get('record_id', 'unknown')
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'message': 'Data collection failed',
                'errors': result.get('errors', [])
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Mobile data collection failed: {e}")
        return Response({
            'status': 'error',
            'message': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Health check endpoint
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        return JsonResponse({
            'status': 'healthy',
            'message': 'Data Architecture API is running',
            'timestamp': time.time(),
            'database': 'PostgreSQL'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


# Data Quality Monitoring Endpoints
def run_quality_checks(request):
    """Run comprehensive data quality checks"""
    try:
        results = quality_monitor.run_quality_checks()
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def get_quality_dashboard(request):
    """Get data quality dashboard data"""
    try:
        dashboard_data = quality_monitor.get_quality_dashboard_data()
        return JsonResponse(dashboard_data)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def setup_quality_gates(request):
    """Set up automated quality gates"""
    try:
        results = quality_monitor.setup_quality_gates()
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


# Data Population Endpoints
def populate_sample_data(request):
    """Populate database with sample data"""
    try:
        results = data_populator.populate_all_data()
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def populate_geography_data(request):
    """Populate geography data (counties, constituencies, wards)"""
    try:
        results = data_populator.populate_geography_data()
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def populate_facilities_data(request):
    """Populate facilities data"""
    try:
        count = int(request.GET.get('count', 50))
        results = data_populator.populate_facilities_data(count)
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


# Data Source Integration Endpoints
def get_data_sources(request):
    """Get list of available data sources"""
    try:
        sources = integration_manager.get_available_sources()
        return JsonResponse({
            'status': 'success',
            'sources': sources,
            'count': len(sources)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def create_data_source(request):
    """Create a new data source"""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        source_type = data.get('type')
        config = data.get('config', {})
        
        if not name or not source_type:
            return JsonResponse({
                'status': 'error',
                'message': 'Name and type are required'
            }, status=400)
        
        data_source = integration_manager.create_data_source(name, source_type, config)
        return JsonResponse({
            'status': 'success',
            'message': 'Data source created successfully',
            'source_id': data_source.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def test_data_source(request, source_id):
    """Test connection to a data source"""
    try:
        data_source = DataSource.objects.get(id=source_id)
        results = integration_manager.test_source_connection(data_source)
        return JsonResponse(results)
    except DataSource.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Data source not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def ingest_from_source(request, source_id):
    """Ingest data from a specific source"""
    try:
        data_source = DataSource.objects.get(id=source_id)
        limit = int(request.GET.get('limit', 0)) or None
        results = integration_manager.ingest_from_source(data_source, limit)
        return JsonResponse(results)
    except DataSource.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Data source not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


# Intelligent Data Scraping Endpoints
def discover_data_files(request):
    """Discover all data files in the project"""
    try:
        files = intelligent_scraper.discover_data_files()
        return JsonResponse({
            'status': 'success',
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def process_all_files(request):
    """Process all discovered data files"""
    try:
        results = intelligent_scraper.process_all_files()
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def clear_sample_data(request):
    """Clear all sample data from the system"""
    try:
        results = intelligent_scraper.clear_sample_data()
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)


def extract_facilities_pdfs(request):
    """Extract data from all PDFs in facilities raw data directory"""
    try:
        import os
        
        pdf_directory = "facilities_import/data/raw/"
        pdf_files = [
            "All_Facilities_Facilities_licensed_by_KMPDC_for_year_2024_as_at_7th_June_2024_at_5.00pm.pdf",
            "LIST_OF_LICENSED_HEALTH_CARE_FACILITIES_BY_KMPDC-1.pdf", 
            "LIST_OF_LICENSED_HEALTH_CARE_FACILITIES_BY_KMPDC.pdf",
            "National_Shelters_Network_a5a50b19.pdf"
        ]
        
        data_manager = DataArchitectureManager()
        all_extracted_data = []
        
        for pdf_file in pdf_files:
            file_path = os.path.join(pdf_directory, pdf_file)
            
            if not os.path.exists(file_path):
                continue
                
            source_name = f"pdf_{pdf_file.replace('.pdf', '').replace(' ', '_').lower()}"
            config = {'file_path': file_path, 'encoding': 'utf-8'}
            
            try:
                data_source = integration_manager.create_data_source(
                    name=source_name,
                    source_type='pdf',
                    config=config
                )
                
                result = integration_manager.ingest_from_source(data_source)
                
                all_extracted_data.append({
                    'source': pdf_file,
                    'result': result
                })
                
            except Exception as e:
                all_extracted_data.append({
                    'source': pdf_file,
                    'error': str(e)
                })
        
        # Save extraction summary
        summary_path = "facilities_import/data/exports/pdf_extraction_summary.json"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        
        with open(summary_path, 'w') as f:
            json.dump(all_extracted_data, f, indent=2, default=str)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Processed {len(all_extracted_data)} PDFs',
            'results': all_extracted_data,
            'summary_path': summary_path
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=500)

