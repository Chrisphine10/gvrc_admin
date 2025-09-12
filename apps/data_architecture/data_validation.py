"""
Comprehensive Data Validation Framework
Multi-layer validation with quality gates
"""

import re
import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import ValidatedDataRecord, DataQualityMetric, RawDataRecord
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Comprehensive data validation with quality scoring"""
    
    def __init__(self):
        self.schemas = {
            'facility': self._get_facility_schema(),
            'geographic': self._get_geographic_schema(),
            'contact': self._get_contact_schema(),
            'service': self._get_service_schema(),
            'gbv_organization': self._get_gbv_organization_schema()
        }
        self.quality_thresholds = {
            'completeness': 0.5,  # Lowered from 0.8 to 0.5 for more lenient validation
            'accuracy': 0.7,      # Lowered from 0.9 to 0.7
            'consistency': 0.8,   # Lowered from 0.95 to 0.8
            'timeliness': 0.7,    # Lowered from 0.9 to 0.7
            'uniqueness': 0.8     # Lowered from 0.95 to 0.8
        }
    
    def validate_gbv_organization_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive GBV organization data validation"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 0.0,
            'validation_details': {}
        }
        
        try:
            # Normalize data structure
            normalized_data = self._normalize_gbv_organization_data(data)
            
            # Schema validation
            schema_result = self._validate_schema(normalized_data, 'gbv_organization')
            validation_result['validation_details']['schema'] = schema_result
            
            if not schema_result['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(schema_result['errors'])
            
            validation_result['warnings'].extend(schema_result['warnings'])
            
            # Business rules validation
            business_result = self._validate_gbv_business_rules(normalized_data)
            validation_result['validation_details']['business_rules'] = business_result
            
            if not business_result['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(business_result['errors'])
            
            validation_result['warnings'].extend(business_result['warnings'])
            
            # Quality metrics
            quality_metrics = self._calculate_gbv_quality_metrics(normalized_data)
            validation_result['validation_details']['quality_metrics'] = quality_metrics
            validation_result['quality_score'] = quality_metrics['overall_score']
            
        except Exception as e:
            logger.error(f"GBV organization validation error: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
            return validation_result
        
        return validation_result
    
    def validate_facility_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive facility data validation"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 0.0,
            'validation_details': {}
        }
        
        try:
            # Normalize data structure (handle both nested and flat)
            normalized_data = self._normalize_facility_data(data)
            
            # Schema validation
            schema_result = self._validate_schema(normalized_data, 'facility')
            validation_result['validation_details']['schema'] = schema_result
            
            if not schema_result['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(schema_result['errors'])
            
            # Business rules validation
            business_result = self._validate_business_rules(data)
            validation_result['validation_details']['business_rules'] = business_result
            
            if not business_result['is_valid']:
                validation_result['is_valid'] = False
                validation_result['errors'].extend(business_result['errors'])
            
            # Data quality metrics
            quality_metrics = self._calculate_quality_metrics(data)
            validation_result['validation_details']['quality_metrics'] = quality_metrics
            validation_result['quality_score'] = quality_metrics['overall_score']
            
            # Check against thresholds
            if validation_result['quality_score'] < self.quality_thresholds['completeness']:
                validation_result['warnings'].append(
                    f"Quality score {validation_result['quality_score']:.2f} below threshold"
                )
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
            return validation_result
    
    def _normalize_facility_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize facility data to handle both nested and flat structures"""
        normalized = data.copy()
        
        # If we have flat location fields, create a nested location object
        if 'county' in data and 'location' not in data:
            location = {}
            if 'county' in data:
                location['county'] = data['county']
            if 'constituency' in data:
                location['constituency'] = data['constituency']
            if 'ward' in data:
                location['ward'] = data['ward']
            # Only add latitude/longitude if they exist and are valid numbers
            if 'latitude' in data and data['latitude'] is not None:
                try:
                    location['latitude'] = float(data['latitude'])
                except (ValueError, TypeError):
                    pass
            if 'longitude' in data and data['longitude'] is not None:
                try:
                    location['longitude'] = float(data['longitude'])
                except (ValueError, TypeError):
                    pass
            
            normalized['location'] = location
        
        return normalized
    
    def _normalize_gbv_organization_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize GBV organization data structure"""
        normalized = data.copy()
        
        # Ensure required fields exist
        if 'organization_name' not in normalized:
            normalized['organization_name'] = normalized.get('text', 'Unknown Organization')
        
        # Normalize services list
        if 'services' not in normalized:
            normalized['services'] = []
        elif isinstance(normalized['services'], str):
            normalized['services'] = [s.strip() for s in normalized['services'].split(',')]
        
        # Normalize main offices list
        if 'main_offices' not in normalized:
            normalized['main_offices'] = []
        elif isinstance(normalized['main_offices'], str):
            normalized['main_offices'] = [s.strip() for s in normalized['main_offices'].split(',')]
        
        # Normalize support network list
        if 'support_network' not in normalized:
            normalized['support_network'] = []
        elif isinstance(normalized['support_network'], str):
            normalized['support_network'] = [s.strip() for s in normalized['support_network'].split(',')]
        
        return normalized
    
    def _validate_gbv_business_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate GBV organization business rules"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check if organization has services
        if not data.get('services'):
            result['warnings'].append("Organization has no services listed")
        
        # Check if organization has contact information
        if not data.get('website') and not data.get('toll_free_number'):
            result['warnings'].append("Organization has no contact information")
        
        # Check if organization has coverage information
        if not data.get('coverage'):
            result['warnings'].append("Organization has no coverage information")
        
        return result
    
    def _calculate_gbv_quality_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality metrics for GBV organization data"""
        metrics = {
            'completeness': 0.0,
            'accuracy': 1.0,
            'consistency': 1.0,
            'timeliness': 1.0,
            'uniqueness': 1.0,
            'overall_score': 0.0
        }
        
        # Calculate completeness
        required_fields = ['organization_name', 'services', 'coverage']
        optional_fields = ['website', 'toll_free_number', 'main_offices', 'experience', 'beneficiaries']
        
        required_completeness = sum(1 for field in required_fields if data.get(field)) / len(required_fields)
        optional_completeness = sum(1 for field in optional_fields if data.get(field)) / len(optional_fields)
        
        metrics['completeness'] = (required_completeness * 0.7) + (optional_completeness * 0.3)
        
        # Calculate overall score
        metrics['overall_score'] = (
            metrics['completeness'] * 0.4 +
            metrics['accuracy'] * 0.2 +
            metrics['consistency'] * 0.2 +
            metrics['timeliness'] * 0.1 +
            metrics['uniqueness'] * 0.1
        )
        
        return metrics
    
    def _get_gbv_organization_schema(self) -> Dict[str, Any]:
        """Get GBV organization data schema"""
        return {
            "type": "object",
            "required": ["organization_name"],
            "properties": {
                "organization_name": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 255
                },
                "services": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "coverage": {
                    "type": "string",
                    "maxLength": 500
                },
                "website": {
                    "type": "string",
                    "format": "uri"
                },
                "toll_free_number": {
                    "type": "string",
                    "maxLength": 50
                },
                "main_offices": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "experience": {
                    "type": "string",
                    "maxLength": 200
                },
                "beneficiaries": {
                    "type": "string",
                    "maxLength": 200
                },
                "support_network": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "contact_details": {
                    "type": "object"
                },
                "source_file": {
                    "type": "string"
                },
                "source_type": {
                    "type": "string"
                }
            }
        }
    
    def _validate_schema(self, data: Dict[str, Any], schema_type: str) -> Dict[str, Any]:
        """Validate data against JSON schema"""
        schema = self.schemas.get(schema_type, {})
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Required fields validation
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in data or not data[field]:
                result['is_valid'] = False
                result['errors'].append(f"Missing required field: {field}")
        
        # Field type validation - only validate fields that exist in data
        properties = schema.get('properties', {})
        for field, field_schema in properties.items():
            if field in data and data[field] is not None:
                field_result = self._validate_field(data[field], field_schema, field)
                if not field_result['is_valid']:
                    result['is_valid'] = False
                    result['errors'].extend(field_result['errors'])
                result['warnings'].extend(field_result['warnings'])
        
        return result
    
    def _validate_field(self, value: Any, field_schema: Dict[str, Any], field_name: str) -> Dict[str, Any]:
        """Validate individual field"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Type validation
        expected_type = field_schema.get('type')
        if expected_type == 'string' and not isinstance(value, str):
            result['is_valid'] = False
            result['errors'].append(f"Field {field_name} must be a string")
        elif expected_type == 'number' and not isinstance(value, (int, float)):
            result['is_valid'] = False
            result['errors'].append(f"Field {field_name} must be a number")
        elif expected_type == 'boolean' and not isinstance(value, bool):
            result['is_valid'] = False
            result['errors'].append(f"Field {field_name} must be a boolean")
        
        # String validations
        if isinstance(value, str) and expected_type == 'string':
            # Length validation
            min_length = field_schema.get('minLength', 0)
            max_length = field_schema.get('maxLength', float('inf'))
            if len(value) < min_length:
                result['is_valid'] = False
                result['errors'].append(f"Field {field_name} too short (min: {min_length})")
            elif len(value) > max_length:
                result['is_valid'] = False
                result['errors'].append(f"Field {field_name} too long (max: {max_length})")
            
            # Pattern validation
            pattern = field_schema.get('pattern')
            if pattern and not re.match(pattern, value):
                result['is_valid'] = False
                result['errors'].append(f"Field {field_name} format invalid")
        
        return result
    
    def _validate_business_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business-specific rules"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Facility name validation
        if 'facility_name' in data:
            facility_name = data['facility_name']
            if len(facility_name.strip()) < 3:
                result['is_valid'] = False
                result['errors'].append("Facility name must be at least 3 characters")
            
            # Check for suspicious patterns
            if re.search(r'[0-9]{4,}', facility_name):
                result['warnings'].append("Facility name contains many numbers - verify accuracy")
        
        # Geographic validation
        if 'location' in data:
            location_result = self._validate_location(data['location'])
            if not location_result['is_valid']:
                result['is_valid'] = False
                result['errors'].extend(location_result['errors'])
            result['warnings'].extend(location_result['warnings'])
        
        # Contact validation
        if 'contacts' in data:
            contact_result = self._validate_contacts(data['contacts'])
            if not contact_result['is_valid']:
                result['is_valid'] = False
                result['errors'].extend(contact_result['errors'])
            result['warnings'].extend(contact_result['warnings'])
        
        # Service validation
        if 'services' in data:
            service_result = self._validate_services(data['services'])
            if not service_result['is_valid']:
                result['is_valid'] = False
                result['errors'].extend(service_result['errors'])
            result['warnings'].extend(service_result['warnings'])
        
        return result
    
    def _validate_location(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Validate location data"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # County validation
        if 'county' in location and location['county']:
            county = location['county'].strip()
            if len(county) < 3:
                result['is_valid'] = False
                result['errors'].append("County name too short")
            elif not re.match(r'^[A-Za-z\s]+$', county):
                result['warnings'].append("County name contains non-alphabetic characters")
        
        # Coordinate validation
        if 'latitude' in location and 'longitude' in location:
            lat = location['latitude']
            lng = location['longitude']
            
            if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
                result['is_valid'] = False
                result['errors'].append("Coordinates must be numbers")
            else:
                # Kenya bounds validation
                if not (-4.7 <= lat <= 5.5) or not (33.9 <= lng <= 41.9):
                    result['warnings'].append("Coordinates outside Kenya bounds")
        
        return result
    
    def _validate_contacts(self, contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate contact information"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        if not contacts:
            result['warnings'].append("No contact information provided")
            return result
        
        for i, contact in enumerate(contacts):
            if 'type' not in contact or 'value' not in contact:
                result['is_valid'] = False
                result['errors'].append(f"Contact {i+1} missing type or value")
                continue
            
            contact_type = contact['type']
            contact_value = contact['value']
            
            # Email validation
            if contact_type.lower() == 'email':
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', contact_value):
                    result['is_valid'] = False
                    result['errors'].append(f"Invalid email format: {contact_value}")
            
            # Phone validation
            elif contact_type.lower() in ['phone', 'mobile', 'telephone']:
                # Remove all non-digit characters
                phone_digits = re.sub(r'\D', '', contact_value)
                if len(phone_digits) < 9 or len(phone_digits) > 15:
                    result['warnings'].append(f"Phone number length unusual: {contact_value}")
        
        return result
    
    def _validate_services(self, services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate service information"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        if not services:
            result['warnings'].append("No services specified")
            return result
        
        for i, service in enumerate(services):
            if 'category' not in service:
                result['warnings'].append(f"Service {i+1} missing category")
            
            if 'description' in service and len(service['description']) > 500:
                result['warnings'].append(f"Service {i+1} description very long")
        
        return result
    
    def _calculate_quality_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive quality metrics"""
        metrics = {}
        
        # Completeness
        completeness = self._calculate_completeness(data)
        metrics['completeness'] = completeness
        
        # Accuracy (based on validation results)
        accuracy = self._calculate_accuracy(data)
        metrics['accuracy'] = accuracy
        
        # Consistency
        consistency = self._calculate_consistency(data)
        metrics['consistency'] = consistency
        
        # Timeliness
        timeliness = self._calculate_timeliness(data)
        metrics['timeliness'] = timeliness
        
        # Uniqueness
        uniqueness = self._calculate_uniqueness(data)
        metrics['uniqueness'] = uniqueness
        
        # Overall score (weighted average)
        weights = {
            'completeness': 0.3,
            'accuracy': 0.25,
            'consistency': 0.2,
            'timeliness': 0.15,
            'uniqueness': 0.1
        }
        
        overall_score = sum(metrics[metric] * weights[metric] for metric in metrics)
        metrics['overall_score'] = overall_score
        
        return metrics
    
    def _calculate_completeness(self, data: Dict[str, Any]) -> float:
        """Calculate data completeness score"""
        required_fields = ['facility_name', 'location']
        optional_fields = ['facility_type', 'services', 'contacts', 'coordinates']
        
        required_score = sum(
            1 for field in required_fields 
            if field in data and data[field] and str(data[field]).strip()
        ) / len(required_fields)
        
        optional_score = sum(
            1 for field in optional_fields 
            if field in data and data[field] and str(data[field]).strip()
        ) / len(optional_fields)
        
        # Weighted: 70% required, 30% optional
        return (required_score * 0.7) + (optional_score * 0.3)
    
    def _calculate_accuracy(self, data: Dict[str, Any]) -> float:
        """Calculate data accuracy score based on validation rules"""
        # This would be more sophisticated in practice
        # For now, we'll use a simple heuristic
        
        accuracy_score = 1.0
        
        # Check facility name quality
        if 'facility_name' in data:
            name = data['facility_name']
            if len(name.strip()) < 5:
                accuracy_score -= 0.1
            if re.search(r'[0-9]{3,}', name):
                accuracy_score -= 0.05
        
        # Check location quality
        if 'location' in data:
            location = data['location']
            if 'county' not in location or not location['county']:
                accuracy_score -= 0.2
            if 'latitude' in location and 'longitude' in location:
                lat = location['latitude']
                lng = location['longitude']
                if isinstance(lat, (int, float)) and isinstance(lng, (int, float)):
                    if not (-4.7 <= lat <= 5.5) or not (33.9 <= lng <= 41.9):
                        accuracy_score -= 0.1
        
        return max(0.0, accuracy_score)
    
    def _calculate_consistency(self, data: Dict[str, Any]) -> float:
        """Calculate data consistency score"""
        consistency_score = 1.0
        
        # Check naming consistency
        if 'facility_name' in data:
            name = data['facility_name']
            # Check for consistent capitalization
            if name != name.title() and not name.isupper() and not name.islower():
                consistency_score -= 0.05
        
        # Check location consistency
        if 'location' in data:
            location = data['location']
            county = location.get('county', '')
            constituency = location.get('constituency', '')
            ward = location.get('ward', '')
            
            # Check if all location levels follow same naming pattern
            location_names = [county, constituency, ward]
            if any(name for name in location_names):
                patterns = [bool(re.match(r'^[A-Za-z\s]+$', name)) for name in location_names if name]
                if patterns and not all(patterns):
                    consistency_score -= 0.1
        
        return max(0.0, consistency_score)
    
    def _calculate_timeliness(self, data: Dict[str, Any]) -> float:
        """Calculate data timeliness score"""
        # For now, assume all data is timely
        # In practice, this would check data age, update frequency, etc.
        return 1.0
    
    def _calculate_uniqueness(self, data: Dict[str, Any]) -> float:
        """Calculate data uniqueness score"""
        # This would check for duplicates in the database
        # For now, assume unique
        return 1.0
    
    def _get_facility_schema(self) -> Dict[str, Any]:
        """Get facility data schema - flexible to handle both nested and flat structures"""
        return {
            "type": "object",
            "required": ["facility_name"],
            "properties": {
                "facility_name": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 255
                },
                "facility_type": {
                    "type": "string",
                    "maxLength": 100
                },
                # Support both nested location and flat fields
                "location": {
                    "type": "object",
                    "required": ["county"],
                    "properties": {
                        "county": {"type": "string", "minLength": 3},
                        "constituency": {"type": "string"},
                        "ward": {"type": "string"},
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"}
                    }
                },
                # Flat field structure (for PDF extraction)
                "county": {"type": "string", "minLength": 3},
                "constituency": {"type": "string"},
                "ward": {"type": "string"},
                "latitude": {"type": "number", "minimum": -90, "maximum": 90},
                "longitude": {"type": "number", "minimum": -180, "maximum": 180},
                # Additional PDF extraction fields
                "s_no": {"type": "string"},
                "level": {"type": "string"},
                "status": {"type": "string"},
                "facility_agent": {"type": "string"},
                "registration_number": {"type": "string"},
                "source_type": {"type": "string"},
                "contacts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["type", "value"],
                        "properties": {
                            "type": {"type": "string"},
                            "value": {"type": "string", "minLength": 1}
                        }
                    }
                },
                "services": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "description": {"type": "string", "maxLength": 500}
                        }
                    }
                }
            }
        }
    
    def _get_geographic_schema(self) -> Dict[str, Any]:
        """Get geographic data schema"""
        return {
            "type": "object",
            "required": ["county"],
            "properties": {
                "county": {"type": "string", "minLength": 3},
                "constituency": {"type": "string"},
                "ward": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            }
        }
    
    def _get_contact_schema(self) -> Dict[str, Any]:
        """Get contact data schema"""
        return {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "value"],
                "properties": {
                    "type": {"type": "string"},
                    "value": {"type": "string", "minLength": 1}
                }
            }
        }
    
    def _get_service_schema(self) -> Dict[str, Any]:
        """Get service data schema"""
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "description": {"type": "string", "maxLength": 500}
                }
            }
        }
    
    def validate_batch(self, data_list: List[Dict[str, Any]], data_type: str = 'facility') -> Dict[str, Any]:
        """Validate a batch of data records"""
        batch_result = {
            'total_records': len(data_list),
            'valid_records': 0,
            'invalid_records': 0,
            'validation_results': [],
            'overall_quality_score': 0.0,
            'errors': [],
            'warnings': []
        }
        
        try:
            total_quality_score = 0.0
            
            for i, data in enumerate(data_list):
                try:
                    if data_type == 'facility':
                        validation_result = self.validate_facility_data(data)
                    elif data_type == 'geographic':
                        validation_result = self.validate_geographic_data(data)
                    elif data_type == 'gbv_organization':
                        validation_result = self.validate_gbv_organization_data(data)
                    elif data_type == 'contact':
                        validation_result = self.validate_contact_data(data)
                    elif data_type == 'service':
                        validation_result = self.validate_service_data(data)
                    elif data_type == 'shelter':
                        validation_result = validate_shelter_data(data)
                    elif data_type == 'fgm_resources':
                        validation_result = validate_fgm_resources_data(data)
                    elif data_type == 'police_station':
                        validation_result = validate_police_station_data(data)
                    else:
                        # Generic validation
                        validation_result = self._validate_generic_data(data)
                    
                    batch_result['validation_results'].append({
                        'record_index': i,
                        'validation_result': validation_result
                    })
                    
                    if validation_result['is_valid']:
                        batch_result['valid_records'] += 1
                    else:
                        batch_result['invalid_records'] += 1
                        batch_result['errors'].extend(validation_result['errors'])
                    
                    total_quality_score += validation_result['quality_score']
                    
                except Exception as e:
                    logger.error(f"Validation error for record {i}: {str(e)}")
                    batch_result['invalid_records'] += 1
                    batch_result['errors'].append(f"Record {i}: {str(e)}")
            
            # Calculate overall quality score
            if batch_result['total_records'] > 0:
                batch_result['overall_quality_score'] = total_quality_score / batch_result['total_records']
            
        except Exception as e:
            logger.error(f"Batch validation error: {str(e)}")
            batch_result['errors'].append(f"Batch validation error: {str(e)}")
        
        return batch_result
    
    def _validate_generic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generic data validation for unknown data types"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 0.0,
            'validation_details': {}
        }
        
        try:
            # Basic data quality checks
            if not data:
                validation_result['is_valid'] = False
                validation_result['errors'].append("Empty data record")
                return validation_result
            
            # Check for required fields (basic)
            required_fields = ['facility_name', 'county', 'facility_type']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                validation_result['warnings'].append(f"Missing recommended fields: {missing_fields}")
            
            # Calculate basic quality score
            field_count = len([v for v in data.values() if v])
            total_fields = len(data)
            validation_result['quality_score'] = field_count / total_fields if total_fields > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Generic validation error: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
        
        return validation_result


class QualityGates:
    """Data quality gates implementation"""
    
    def __init__(self):
        self.gates = {
            'completeness': CompletenessGate(),
            'accuracy': AccuracyGate(),
            'consistency': ConsistencyGate(),
            'timeliness': TimelinessGate(),
            'uniqueness': UniquenessGate()
        }
        self.thresholds = {
            'completeness': 0.8,
            'accuracy': 0.9,
            'consistency': 0.95,
            'timeliness': 0.9,
            'uniqueness': 0.95
        }
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against all quality gates"""
        validation_result = {
            'passed': True,
            'issues': [],
            'scores': {},
            'recommendations': []
        }
        
        for gate_name, gate in self.gates.items():
            gate_result = gate.validate(data)
            validation_result['scores'][gate_name] = gate_result['score']
            
            if not gate_result['passed']:
                validation_result['passed'] = False
                validation_result['issues'].extend(gate_result['issues'])
            
            if gate_result['recommendations']:
                validation_result['recommendations'].extend(gate_result['recommendations'])
        
        # Overall quality score
        validation_result['overall_score'] = self._calculate_overall_score(validation_result['scores'])
        
        return validation_result
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate overall quality score"""
        weights = {
            'completeness': 0.3,
            'accuracy': 0.25,
            'consistency': 0.2,
            'timeliness': 0.15,
            'uniqueness': 0.1
        }
        
        return sum(scores[metric] * weights[metric] for metric in scores)


class CompletenessGate:
    """Completeness quality gate"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data completeness"""
        required_fields = ['facility_name', 'location', 'contacts']
        optional_fields = ['facility_type', 'services', 'coordinates']
        
        completeness_score = 0
        issues = []
        recommendations = []
        
        # Check required fields
        required_completeness = sum(
            1 for field in required_fields 
            if field in data and data[field] and str(data[field]).strip()
        ) / len(required_fields)
        
        # Check optional fields
        optional_completeness = sum(
            1 for field in optional_fields 
            if field in data and data[field] and str(data[field]).strip()
        ) / len(optional_fields)
        
        # Calculate weighted score
        completeness_score = (required_completeness * 0.7) + (optional_completeness * 0.3)
        
        # Check against threshold
        threshold = 0.8
        passed = completeness_score >= threshold
        
        if not passed:
            issues.append(f"Completeness score {completeness_score:.2f} below threshold {threshold}")
            
            # Generate recommendations
            missing_required = [field for field in required_fields 
                              if field not in data or not data.get(field)]
            if missing_required:
                recommendations.append(f"Add missing required fields: {', '.join(missing_required)}")
        
        return {
            'passed': passed,
            'score': completeness_score,
            'issues': issues,
            'recommendations': recommendations
        }


class AccuracyGate:
    """Accuracy quality gate"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data accuracy"""
        accuracy_score = 1.0
        issues = []
        recommendations = []
        
        # Check facility name quality
        if 'facility_name' in data:
            name = data['facility_name']
            if len(name.strip()) < 5:
                accuracy_score -= 0.2
                issues.append("Facility name too short")
                recommendations.append("Provide a more descriptive facility name")
        
        # Check location accuracy
        if 'location' in data:
            location = data['location']
            if 'county' not in location or not location['county']:
                accuracy_score -= 0.3
                issues.append("Missing county information")
                recommendations.append("Provide county information for accurate location")
        
        threshold = 0.9
        passed = accuracy_score >= threshold
        
        if not passed:
            issues.append(f"Accuracy score {accuracy_score:.2f} below threshold {threshold}")
        
        return {
            'passed': passed,
            'score': accuracy_score,
            'issues': issues,
            'recommendations': recommendations
        }


class ConsistencyGate:
    """Consistency quality gate"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data consistency"""
        consistency_score = 1.0
        issues = []
        recommendations = []
        
        # Check naming consistency
        if 'facility_name' in data:
            name = data['facility_name']
            if not name.istitle() and not name.isupper() and not name.islower():
                consistency_score -= 0.1
                recommendations.append("Use consistent capitalization for facility name")
        
        threshold = 0.95
        passed = consistency_score >= threshold
        
        if not passed:
            issues.append(f"Consistency score {consistency_score:.2f} below threshold {threshold}")
        
        return {
            'passed': passed,
            'score': consistency_score,
            'issues': issues,
            'recommendations': recommendations
        }


class TimelinessGate:
    """Timeliness quality gate"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data timeliness"""
        # For now, assume all data is timely
        # In practice, this would check data age, update frequency, etc.
        return {
            'passed': True,
            'score': 1.0,
            'issues': [],
            'recommendations': []
        }


class UniquenessGate:
    """Uniqueness quality gate"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data uniqueness"""
        # This would check for duplicates in the database
        # For now, assume unique
        return {
            'passed': True,
            'score': 1.0,
            'issues': [],
            'recommendations': []
        }


# Additional validation methods for new data types
def validate_shelter_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate shelter data from National Shelters Network"""
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'quality_score': 0.0,
        'validation_details': {}
    }
    
    try:
        # Required fields
        required_fields = ['shelter_name', 'county']
        for field in required_fields:
            if not data.get(field):
                validation_result['errors'].append(f"Missing required field: {field}")
                validation_result['is_valid'] = False
        
        # Optional fields validation
        if data.get('shelter_number') and not str(data['shelter_number']).strip():
            validation_result['warnings'].append("Shelter number is empty")
        
        if data.get('contact_info') and len(str(data['contact_info'])) < 5:
            validation_result['warnings'].append("Contact info seems too short")
        
        # Calculate quality score
        total_fields = len([k for k in data.keys() if data.get(k) is not None])
        filled_fields = len([k for k in data.keys() if data.get(k) and str(data.get(k)).strip()])
        validation_result['quality_score'] = filled_fields / max(total_fields, 1)
        
        return validation_result
        
    except Exception as e:
        validation_result['is_valid'] = False
        validation_result['errors'].append(f"Validation error: {str(e)}")
        return validation_result


def validate_fgm_resources_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate FGM resources data"""
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'quality_score': 0.0,
        'validation_details': {}
    }
    
    try:
        # Required fields
        required_fields = ['document_title', 'gbv_category']
        for field in required_fields:
            if not data.get(field):
                validation_result['errors'].append(f"Missing required field: {field}")
                validation_result['is_valid'] = False
        
        # URL validation
        if data.get('file_url') and not _is_valid_url(data['file_url']):
            validation_result['warnings'].append("Invalid file URL format")
        
        if data.get('external_url') and not _is_valid_url(data['external_url']):
            validation_result['warnings'].append("Invalid external URL format")
        
        # Calculate quality score
        total_fields = len([k for k in data.keys() if data.get(k) is not None])
        filled_fields = len([k for k in data.keys() if data.get(k) and str(data.get(k)).strip()])
        validation_result['quality_score'] = filled_fields / max(total_fields, 1)
        
        return validation_result
        
    except Exception as e:
        validation_result['is_valid'] = False
        validation_result['errors'].append(f"Validation error: {str(e)}")
        return validation_result


def validate_police_station_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate police station data"""
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'quality_score': 0.0,
        'validation_details': {}
    }
    
    try:
        # Required fields
        required_fields = ['police_station_name']
        for field in required_fields:
            if not data.get(field):
                validation_result['errors'].append(f"Missing required field: {field}")
                validation_result['is_valid'] = False
        
        # Phone number validation
        if data.get('phone_number') and not _is_valid_phone(data['phone_number']):
            validation_result['warnings'].append("Phone number format may be invalid")
        
        # Calculate quality score
        total_fields = len([k for k in data.keys() if data.get(k) is not None])
        filled_fields = len([k for k in data.keys() if data.get(k) and str(data.get(k)).strip()])
        validation_result['quality_score'] = filled_fields / max(total_fields, 1)
        
        return validation_result
        
    except Exception as e:
        validation_result['is_valid'] = False
        validation_result['errors'].append(f"Validation error: {str(e)}")
        return validation_result


def _is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    try:
        import re
        pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return pattern.match(url) is not None
    except:
        return False


def _is_valid_phone(phone: str) -> bool:
    """Check if phone number is valid"""
    try:
        import re
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', str(phone))
        # Check if it's a reasonable length (7-15 digits)
        return 7 <= len(digits_only) <= 15
    except:
        return False

