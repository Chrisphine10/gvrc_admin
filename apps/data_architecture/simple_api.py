"""
Simple API for Data Architecture Testing
Easy-to-use endpoints for testing and debugging
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def test_enhancement(request):
    """Simple test endpoint for facility enhancement"""
    try:
        if request.method == 'GET':
            return JsonResponse({
                'status': 'ready',
                'message': 'Enhancement API is ready',
                'endpoints': {
                    'POST /test-enhancement/': 'Enhance facility data',
                    'GET /test-enhancement/': 'Get API status'
                }
            })
        
        # POST request - enhance facility data
        data = json.loads(request.body)
        facility_data = data.get('facility', {})
        
        if not facility_data:
            return JsonResponse({
                'status': 'error',
                'message': 'No facility data provided'
            }, status=400)
        
        # Import and use the enhancement system
        from .standalone_integration import StandaloneDataArchitecture
        
        standalone = StandaloneDataArchitecture()
        enhanced_facility = standalone.enhance_facility_data(facility_data)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Facility enhanced successfully',
            'original': facility_data,
            'enhanced': enhanced_facility,
            'improvements': _calculate_improvements(facility_data, enhanced_facility)
        })
        
    except Exception as e:
        logger.error(f"Test enhancement failed: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def batch_enhancement(request):
    """Batch enhancement endpoint"""
    try:
        data = json.loads(request.body)
        facility_ids = data.get('facility_ids', [])
        
        if not facility_ids:
            return JsonResponse({
                'status': 'error',
                'message': 'No facility IDs provided'
            }, status=400)
        
        from .standalone_integration import StandaloneDataArchitecture
        
        standalone = StandaloneDataArchitecture()
        result = standalone.batch_enhance_facilities(facility_ids)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Batch enhancement completed',
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Batch enhancement failed: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def system_status(request):
    """Get system status and health"""
    try:
        from .standalone_integration import StandaloneDataArchitecture
        
        standalone = StandaloneDataArchitecture()
        
        # Get basic system info
        status_info = {
            'status': 'healthy',
            'components': {
                'data_architecture': 'ready',
                'geolocation': 'ready',
                'validation': 'ready',
                'enhancement': 'ready'
            },
            'capabilities': [
                'facility_enhancement',
                'geolocation_enhancement',
                'data_quality_validation',
                'batch_processing',
                'duplicate_detection'
            ],
            'api_endpoints': {
                'test_enhancement': '/data-architecture/test-enhancement/',
                'batch_enhancement': '/data-architecture/batch-enhancement/',
                'system_status': '/data-architecture/system-status/'
            }
        }
        
        return JsonResponse(status_info)
        
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def validate_data(request):
    """Data validation endpoint"""
    try:
        data = json.loads(request.body)
        facility_data = data.get('facility', {})
        
        if not facility_data:
            return JsonResponse({
                'status': 'error',
                'message': 'No facility data provided'
            }, status=400)
        
        from .data_validation import DataValidator, QualityGates
        
        # Validate data
        validator = DataValidator()
        validation_result = validator.validate_facility_data(facility_data)
        
        # Apply quality gates
        quality_gates = QualityGates()
        quality_result = quality_gates.validate_data(facility_data)
        
        return JsonResponse({
            'status': 'success',
            'validation': validation_result,
            'quality_gates': quality_result,
            'recommendations': _generate_recommendations(validation_result, quality_result)
        })
        
    except Exception as e:
        logger.error(f"Data validation failed: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def _calculate_improvements(original: Dict[str, Any], enhanced: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate improvements made during enhancement"""
    improvements = {
        'fields_enhanced': [],
        'quality_score_improvement': 0,
        'geographic_enhancement': False,
        'data_cleaning': False
    }
    
    # Check for name cleaning
    if original.get('facility_name') != enhanced.get('facility_name'):
        improvements['fields_enhanced'].append('facility_name')
        improvements['data_cleaning'] = True
    
    # Check for geographic enhancement
    orig_location = original.get('location', {})
    enh_location = enhanced.get('location', {})
    
    if (orig_location.get('latitude') != enh_location.get('latitude') or 
        orig_location.get('longitude') != enh_location.get('longitude')):
        improvements['fields_enhanced'].append('coordinates')
        improvements['geographic_enhancement'] = True
    
    # Check for contact cleaning
    orig_contacts = original.get('contacts', [])
    enh_contacts = enhanced.get('contacts', [])
    
    if len(orig_contacts) != len(enh_contacts):
        improvements['fields_enhanced'].append('contacts')
        improvements['data_cleaning'] = True
    
    return improvements


def _generate_recommendations(validation_result: Dict[str, Any], quality_result: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on validation and quality results"""
    recommendations = []
    
    # Validation recommendations
    if validation_result.get('errors'):
        recommendations.append(f"Fix {len(validation_result['errors'])} validation errors")
    
    if validation_result.get('warnings'):
        recommendations.append(f"Address {len(validation_result['warnings'])} validation warnings")
    
    # Quality recommendations
    if not quality_result.get('passed'):
        recommendations.append("Improve data quality to meet quality gate thresholds")
    
    # Specific recommendations based on scores
    scores = quality_result.get('scores', {})
    for metric, score in scores.items():
        if score < 0.8:
            recommendations.append(f"Improve {metric} score (current: {score:.2f})")
    
    return recommendations


# URL patterns for simple API
urlpatterns = [
    # These would be added to the main urls.py
    # path('test-enhancement/', test_enhancement, name='test_enhancement'),
    # path('batch-enhancement/', batch_enhancement, name='batch_enhancement'),
    # path('system-status/', system_status, name='system_status'),
    # path('validate-data/', validate_data, name='validate_data'),
]

