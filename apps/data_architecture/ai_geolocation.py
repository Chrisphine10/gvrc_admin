"""
AI-Powered Geolocation Enhancement
Free geocoding services for accurate coordinates
"""

import requests
import time
import logging
from typing import Dict, Any, Optional, List, Tuple
from decimal import Decimal
from django.conf import settings
from .models import GeographicEnhancement
import json

logger = logging.getLogger(__name__)


class AIGeolocationEnhancer:
    """AI-powered geolocation enhancement using free services"""
    
    def __init__(self):
        self.free_services = [
            'nominatim',  # OpenStreetMap
            'google',     # Google Maps (free tier)
            'mapbox'      # Mapbox (free tier)
        ]
        self.cache = {}  # Cache results to avoid API limits
        self.kenya_bounds = {
            'min_lat': -4.7, 'max_lat': 5.5,
            'min_lng': 33.9, 'max_lng': 41.9
        }
        self.rate_limits = {
            'nominatim': {'requests_per_second': 1, 'last_request': 0},
            'google': {'requests_per_second': 10, 'last_request': 0},
            'mapbox': {'requests_per_second': 5, 'last_request': 0}
        }
    
    def enhance_coordinates(self, address: str, county: str = None, 
                          constituency: str = None, ward: str = None) -> Optional[Dict[str, Any]]:
        """Enhance coordinates using multiple free services"""
        cache_key = f"{address}_{county}_{constituency}_{ward}"
        if cache_key in self.cache:
            logger.info(f"Using cached geolocation for {address}")
            return self.cache[cache_key]
        
        coordinates = None
        service_used = None
        
        # Try each service until we get a result
        for service in self.free_services:
            try:
                if self._check_rate_limit(service):
                    coordinates = self._get_coordinates_from_service(
                        service, address, county, constituency, ward
                    )
                    if coordinates and self._validate_kenya_coordinates(coordinates):
                        service_used = service
                        break
                    else:
                        logger.warning(f"Service {service} returned invalid coordinates")
                else:
                    logger.warning(f"Rate limit exceeded for service {service}")
                    time.sleep(1)  # Wait before trying next service
                    
            except Exception as e:
                logger.warning(f"Service {service} failed: {e}")
                continue
        
        # Cache the result
        if coordinates:
            coordinates['source'] = service_used
            self.cache[cache_key] = coordinates
            logger.info(f"Enhanced coordinates for {address} using {service_used}")
        
        return coordinates
    
    def enhance_geographic_hierarchy(self, address: str, county: str = None, 
                                   constituency: str = None, ward: str = None) -> Dict[str, Any]:
        """Enhance complete geographic hierarchy"""
        enhancement_result = {
            'original_address': address,
            'enhanced_address': address,
            'county': county,
            'constituency': constituency,
            'ward': ward,
            'latitude': None,
            'longitude': None,
            'accuracy_level': 'unknown',
            'geocoding_service': None,
            'confidence_score': 0.0,
            'enhancements_applied': []
        }
        
        try:
            # Get coordinates
            coordinates = self.enhance_coordinates(address, county, constituency, ward)
            
            if coordinates:
                enhancement_result.update({
                    'latitude': coordinates.get('lat'),
                    'longitude': coordinates.get('lng'),
                    'accuracy_level': coordinates.get('accuracy', 'unknown'),
                    'geocoding_service': coordinates.get('source'),
                    'confidence_score': coordinates.get('confidence', 0.0)
                })
                enhancement_result['enhancements_applied'].append('coordinates')
            
            # Enhance geographic hierarchy
            hierarchy_result = self._enhance_geographic_hierarchy(
                address, county, constituency, ward, coordinates
            )
            
            if hierarchy_result:
                enhancement_result.update(hierarchy_result)
                enhancement_result['enhancements_applied'].extend(
                    hierarchy_result.get('hierarchy_enhancements', [])
                )
            
            # Calculate overall confidence score
            enhancement_result['confidence_score'] = self._calculate_confidence_score(
                enhancement_result
            )
            
            # Save enhancement record
            self._save_enhancement_record(enhancement_result)
            
            return enhancement_result
            
        except Exception as e:
            logger.error(f"Failed to enhance geographic hierarchy: {e}")
            return enhancement_result
    
    def _get_coordinates_from_service(self, service: str, address: str, 
                                    county: str = None, constituency: str = None, 
                                    ward: str = None) -> Optional[Dict[str, Any]]:
        """Get coordinates from specific service"""
        if service == 'nominatim':
            return self._get_nominatim_coordinates(address, county, constituency, ward)
        elif service == 'google':
            return self._get_google_coordinates(address, county, constituency, ward)
        elif service == 'mapbox':
            return self._get_mapbox_coordinates(address, county, constituency, ward)
        return None
    
    def _get_nominatim_coordinates(self, address: str, county: str = None, 
                                 constituency: str = None, ward: str = None) -> Optional[Dict[str, Any]]:
        """Get coordinates from Nominatim (free)"""
        try:
            # Build search query
            query_parts = [address]
            if ward:
                query_parts.append(ward)
            if constituency:
                query_parts.append(constituency)
            if county:
                query_parts.append(county)
            query_parts.append('Kenya')
            
            search_query = ', '.join(query_parts)
            
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': search_query,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'ke',
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'GVRC-Admin/1.0 (geolocation-enhancement)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                if results:
                    result = results[0]
                    return {
                        'latitude': float(result['lat']),
                        'longitude': float(result['lon']),
                        'accuracy': result.get('type', 'unknown'),
                        'confidence': self._calculate_nominatim_confidence(result),
                        'display_name': result.get('display_name', '')
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Nominatim geocoding failed: {e}")
            return None
    
    def _get_google_coordinates(self, address: str, county: str = None, 
                              constituency: str = None, ward: str = None) -> Optional[Dict[str, Any]]:
        """Get coordinates from Google Maps (free tier)"""
        try:
            # This would require Google Maps API key
            # For now, return None to use other services
            api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
            if not api_key:
                return None
            
            # Build search query
            query_parts = [address]
            if ward:
                query_parts.append(ward)
            if constituency:
                query_parts.append(constituency)
            if county:
                query_parts.append(county)
            query_parts.append('Kenya')
            
            search_query = ' '.join(query_parts)
            
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': search_query,
                'key': api_key,
                'region': 'ke'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK' and data['results']:
                    result = data['results'][0]
                    location = result['geometry']['location']
                    return {
                        'latitude': location['lat'],
                        'longitude': location['lng'],
                        'accuracy': result['geometry'].get('location_type', 'unknown'),
                        'confidence': self._calculate_google_confidence(result),
                        'display_name': result.get('formatted_address', '')
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Google geocoding failed: {e}")
            return None
    
    def _get_mapbox_coordinates(self, address: str, county: str = None, 
                              constituency: str = None, ward: str = None) -> Optional[Dict[str, Any]]:
        """Get coordinates from Mapbox (free tier)"""
        try:
            # This would require Mapbox API key
            # For now, return None to use other services
            api_key = getattr(settings, 'MAPBOX_API_KEY', None)
            if not api_key:
                return None
            
            # Build search query
            query_parts = [address]
            if ward:
                query_parts.append(ward)
            if constituency:
                query_parts.append(constituency)
            if county:
                query_parts.append(county)
            query_parts.append('Kenya')
            
            search_query = ' '.join(query_parts)
            
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{search_query}.json"
            params = {
                'access_token': api_key,
                'country': 'ke',
                'limit': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    feature = data['features'][0]
                    coordinates = feature['geometry']['coordinates']
                    return {
                        'lat': coordinates[1],
                        'lng': coordinates[0],
                        'accuracy': feature.get('place_type', ['unknown'])[0],
                        'confidence': self._calculate_mapbox_confidence(feature),
                        'display_name': feature.get('place_name', '')
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Mapbox geocoding failed: {e}")
            return None
    
    def _enhance_geographic_hierarchy(self, address: str, county: str = None, 
                                    constituency: str = None, ward: str = None, 
                                    coordinates: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enhance geographic hierarchy using coordinates and address parsing"""
        result = {
            'hierarchy_enhancements': []
        }
        
        try:
            # If we have coordinates, try to get more precise location info
            if coordinates:
                # This would use reverse geocoding to get more accurate hierarchy
                # For now, we'll use the existing county/constituency/ward if available
                pass
            
            # Parse address for additional geographic information
            address_parts = address.lower().split()
            
            # Look for county names in address
            if not county:
                county_candidates = self._find_county_in_address(address_parts)
                if county_candidates:
                    county = county_candidates[0]
                    result['county'] = county
                    result['hierarchy_enhancements'].append('county_parsed')
            
            # Look for constituency names in address
            if not constituency and county:
                constituency_candidates = self._find_constituency_in_address(
                    address_parts, county
                )
                if constituency_candidates:
                    constituency = constituency_candidates[0]
                    result['constituency'] = constituency
                    result['hierarchy_enhancements'].append('constituency_parsed')
            
            # Look for ward names in address
            if not ward and constituency:
                ward_candidates = self._find_ward_in_address(
                    address_parts, constituency
                )
                if ward_candidates:
                    ward = ward_candidates[0]
                    result['ward'] = ward
                    result['hierarchy_enhancements'].append('ward_parsed')
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to enhance geographic hierarchy: {e}")
            return result
    
    def _find_county_in_address(self, address_parts: List[str]) -> List[str]:
        """Find county names in address parts"""
        # This would use a comprehensive list of Kenya counties
        # For now, return empty list
        return []
    
    def _find_constituency_in_address(self, address_parts: List[str], 
                                    county: str) -> List[str]:
        """Find constituency names in address parts"""
        # This would use a comprehensive list of Kenya constituencies
        # For now, return empty list
        return []
    
    def _find_ward_in_address(self, address_parts: List[str], 
                            constituency: str) -> List[str]:
        """Find ward names in address parts"""
        # This would use a comprehensive list of Kenya wards
        # For now, return empty list
        return []
    
    def _validate_kenya_coordinates(self, coordinates: Dict[str, Any]) -> bool:
        """Validate that coordinates are within Kenya bounds"""
        try:
            lat = coordinates.get('latitude')
            lng = coordinates.get('longitude')
            
            if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
                return False
            
            return (self.kenya_bounds['min_lat'] <= lat <= self.kenya_bounds['max_lat'] and
                    self.kenya_bounds['min_lng'] <= lng <= self.kenya_bounds['max_lng'])
        except Exception:
            return False
    
    def _check_rate_limit(self, service: str) -> bool:
        """Check if service is within rate limits"""
        try:
            current_time = time.time()
            rate_limit = self.rate_limits.get(service, {})
            
            if current_time - rate_limit.get('last_request', 0) >= 1.0 / rate_limit.get('requests_per_second', 1):
                self.rate_limits[service]['last_request'] = current_time
                return True
            return False
        except Exception:
            return True  # Allow if rate limit check fails
    
    def _calculate_nominatim_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for Nominatim result"""
        confidence = 0.5  # Base confidence
        
        # Higher confidence for more specific results
        if result.get('type') in ['house', 'building', 'amenity']:
            confidence += 0.3
        elif result.get('type') in ['street', 'road']:
            confidence += 0.2
        elif result.get('type') in ['suburb', 'neighbourhood']:
            confidence += 0.1
        
        # Check importance score
        importance = result.get('importance', 0)
        if importance > 0.5:
            confidence += 0.2
        elif importance > 0.3:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _calculate_google_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for Google result"""
        confidence = 0.7  # Base confidence for Google
        
        # Check geometry accuracy
        geometry = result.get('geometry', {})
        location_type = geometry.get('location_type', '')
        
        if location_type == 'ROOFTOP':
            confidence += 0.2
        elif location_type == 'RANGE_INTERPOLATED':
            confidence += 0.1
        elif location_type == 'GEOMETRIC_CENTER':
            confidence += 0.05
        
        return min(1.0, confidence)
    
    def _calculate_mapbox_confidence(self, feature: Dict[str, Any]) -> float:
        """Calculate confidence score for Mapbox result"""
        confidence = 0.6  # Base confidence for Mapbox
        
        # Check relevance score
        relevance = feature.get('relevance', 0)
        if relevance > 0.8:
            confidence += 0.3
        elif relevance > 0.6:
            confidence += 0.2
        elif relevance > 0.4:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _calculate_confidence_score(self, enhancement_result: Dict[str, Any]) -> float:
        """Calculate overall confidence score for enhancement"""
        confidence = 0.0
        
        # Base confidence from geocoding service
        if enhancement_result.get('geocoding_service'):
            confidence += 0.4
        
        # Confidence from coordinates accuracy
        if enhancement_result.get('latitude') and enhancement_result.get('longitude'):
            confidence += 0.3
        
        # Confidence from hierarchy completeness
        hierarchy_score = 0
        if enhancement_result.get('county'):
            hierarchy_score += 0.2
        if enhancement_result.get('constituency'):
            hierarchy_score += 0.2
        if enhancement_result.get('ward'):
            hierarchy_score += 0.1
        confidence += hierarchy_score
        
        return min(1.0, confidence)
    
    def _save_enhancement_record(self, enhancement_result: Dict[str, Any]):
        """Save geographic enhancement record"""
        try:
            record_id = f"geo_{int(time.time())}"
            
            GeographicEnhancement.objects.create(
                record_id=record_id,
                original_address=enhancement_result['original_address'],
                enhanced_address=enhancement_result['enhanced_address'],
                county=enhancement_result.get('county', ''),
                constituency=enhancement_result.get('constituency', ''),
                ward=enhancement_result.get('ward', ''),
                latitude=enhancement_result.get('latitude'),
                longitude=enhancement_result.get('longitude'),
                accuracy_level=enhancement_result.get('accuracy_level', ''),
                geocoding_service=enhancement_result.get('geocoding_service', ''),
                confidence_score=enhancement_result.get('confidence_score', 0.0)
            )
            
        except Exception as e:
            logger.error(f"Failed to save enhancement record: {e}")


class KenyaGeographicEnhancement:
    """Complete Kenya geographic data enhancement"""
    
    def __init__(self):
        self.counties = self._load_counties()
        self.constituencies = self._load_constituencies()
        self.wards = self._load_wards()
        self.geolocator = AIGeolocationEnhancer()
    
    def enhance_facility_location(self, facility_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance facility with complete geographic data"""
        try:
            location = facility_data.get('location', {})
            address = facility_data.get('address', '')
            
            # Extract existing location data
            county = location.get('county', '')
            constituency = location.get('constituency', '')
            ward = location.get('ward', '')
            
            # Enhance coordinates if missing
            if not location.get('latitude') or not location.get('longitude'):
                coordinates = self.geolocator.enhance_coordinates(
                    address, county, constituency, ward
                )
                if coordinates:
                    location['latitude'] = coordinates['lat']
                    location['longitude'] = coordinates['lng']
                    location['accuracy_level'] = coordinates.get('accuracy', 'unknown')
            
            # Enhance geographic hierarchy
            hierarchy_result = self.geolocator.enhance_geographic_hierarchy(
                address, county, constituency, ward
            )
            
            if hierarchy_result:
                location.update({
                    'county': hierarchy_result.get('county', county),
                    'constituency': hierarchy_result.get('constituency', constituency),
                    'ward': hierarchy_result.get('ward', ward)
                })
            
            # Find best matching county
            if location.get('county'):
                county_match = self._find_best_county_match(location['county'])
                if county_match:
                    location['county_id'] = county_match['id']
                    location['county_code'] = county_match['code']
            
            # Find best matching constituency
            if location.get('constituency') and location.get('county_id'):
                constituency_match = self._find_best_constituency_match(
                    location['constituency'], location['county_id']
                )
                if constituency_match:
                    location['constituency_id'] = constituency_match['id']
                    location['constituency_code'] = constituency_match['code']
            
            # Find best matching ward
            if location.get('ward') and location.get('constituency_id'):
                ward_match = self._find_best_ward_match(
                    location['ward'], location['constituency_id']
                )
                if ward_match:
                    location['ward_id'] = ward_match['id']
                    location['ward_code'] = ward_match['code']
            
            facility_data['location'] = location
            return facility_data
            
        except Exception as e:
            logger.error(f"Failed to enhance facility location: {e}")
            return facility_data
    
    def _find_best_county_match(self, county_name: str) -> Optional[Dict[str, Any]]:
        """Find best matching county using fuzzy matching"""
        if not county_name:
            return None
        
        # Simple exact match first
        for county in self.counties:
            if county['name'].lower() == county_name.lower():
                return county
        
        # Fuzzy matching would go here
        # For now, return None if no exact match
        return None
    
    def _find_best_constituency_match(self, constituency_name: str, 
                                    county_id: int) -> Optional[Dict[str, Any]]:
        """Find best matching constituency"""
        if not constituency_name or not county_id:
            return None
        
        # Filter constituencies by county
        county_constituencies = [
            c for c in self.constituencies 
            if c.get('county_id') == county_id
        ]
        
        # Simple exact match
        for constituency in county_constituencies:
            if constituency['name'].lower() == constituency_name.lower():
                return constituency
        
        return None
    
    def _find_best_ward_match(self, ward_name: str, 
                            constituency_id: int) -> Optional[Dict[str, Any]]:
        """Find best matching ward"""
        if not ward_name or not constituency_id:
            return None
        
        # Filter wards by constituency
        constituency_wards = [
            w for w in self.wards 
            if w.get('constituency_id') == constituency_id
        ]
        
        # Simple exact match
        for ward in constituency_wards:
            if ward['name'].lower() == ward_name.lower():
                return ward
        
        return None
    
    def _load_counties(self) -> List[Dict[str, Any]]:
        """Load all 47 counties of Kenya"""
        # This would load from database or file
        # For now, return sample data
        return [
            {'id': 1, 'name': 'Mombasa', 'code': 'MOM'},
            {'id': 2, 'name': 'Kwale', 'code': 'KWA'},
            {'id': 3, 'name': 'Kilifi', 'code': 'KIL'},
            # ... all 47 counties
        ]
    
    def _load_constituencies(self) -> List[Dict[str, Any]]:
        """Load all 290 constituencies"""
        # This would load from database
        return []
    
    def _load_wards(self) -> List[Dict[str, Any]]:
        """Load all 1,450 wards"""
        # This would load from database
        return []
    
    def enhance_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance a batch of data records with geolocation information"""
        enhanced_data = []
        
        for record in data_list:
            try:
                # Extract location information
                address = record.get('facility_name', '') or record.get('organization_name', '') or record.get('shelter_name', '')
                county = record.get('county', '')
                constituency = record.get('constituency', '')
                ward = record.get('ward', '')
                
                # Enhance coordinates if we have location data
                if address or county:
                    enhanced_location = self.enhance_coordinates(
                        address=address,
                        county=county,
                        constituency=constituency,
                        ward=ward
                    )
                    
                    if enhanced_location:
                        # Add enhanced location data to the record
                        record.update({
                            'latitude': enhanced_location.get('latitude'),
                            'longitude': enhanced_location.get('longitude'),
                            'geocoding_confidence': enhanced_location.get('confidence', 0.0),
                            'geocoding_service': enhanced_location.get('service_used'),
                            'geocoding_accuracy': enhanced_location.get('accuracy', 'unknown')
                        })
                
                enhanced_data.append(record)
                
            except Exception as e:
                logger.warning(f"Failed to enhance geolocation for record: {str(e)}")
                enhanced_data.append(record)  # Add original record even if enhancement fails
        
        return enhanced_data
