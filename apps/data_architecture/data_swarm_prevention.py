"""
Data Swarm Prevention System
Intelligent deduplication and data quality management
"""

import hashlib
import json
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from difflib import SequenceMatcher
from django.db import transaction
from .models import DataSwarmPrevention, RawDataRecord, ValidatedDataRecord
from .data_validation import DataValidator

logger = logging.getLogger(__name__)


class DataSwarmPreventionSystem:
    """Comprehensive data swarm prevention system"""
    
    def __init__(self):
        self.deduplicator = IntelligentDeduplicator()
        self.quality_gates = DataValidator()
        self.similarity_threshold = 0.85
        self.duplicate_groups = {}
    
    def prevent_data_swarm(self, incoming_data: List[Dict[str, Any]], 
                          source_name: str) -> Dict[str, Any]:
        """Main data swarm prevention pipeline"""
        prevention_result = {
            'total_records': len(incoming_data),
            'duplicates_found': 0,
            'duplicates_merged': 0,
            'quality_issues': 0,
            'data_cleaned': False,
            'processed_records': [],
            'prevention_details': {}
        }
        
        try:
            # Step 1: Detect duplicates
            duplicate_groups = self.deduplicator.find_duplicates(incoming_data)
            prevention_result['duplicates_found'] = len(duplicate_groups)
            prevention_result['prevention_details']['duplicate_groups'] = duplicate_groups
            
            # Step 2: Process duplicates
            if duplicate_groups:
                merged_data = self._process_duplicates(duplicate_groups, source_name)
                prevention_result['duplicates_merged'] = len(merged_data)
                prevention_result['processed_records'].extend(merged_data)
            
            # Step 3: Quality validation for non-duplicates
            non_duplicates = self._get_non_duplicates(incoming_data, duplicate_groups)
            quality_results = []
            
            for record in non_duplicates:
                quality_result = self.quality_gates.validate_facility_data(record)
                quality_results.append(quality_result)
                
                if not quality_result['is_valid']:
                    prevention_result['quality_issues'] += 1
                
                # Clean data if needed
                if quality_result['quality_score'] < 0.5:  # Lowered threshold
                    cleaned_record = self._clean_data(record, quality_result)
                    prevention_result['data_cleaned'] = True
                    prevention_result['processed_records'].append(cleaned_record)
                else:
                    prevention_result['processed_records'].append(record)
            
            prevention_result['prevention_details']['quality_results'] = quality_results
            
            # Step 4: Final validation
            final_validation = self._final_validation(prevention_result['processed_records'])
            prevention_result['prevention_details']['final_validation'] = final_validation
            
            logger.info(f"Data swarm prevention completed: {prevention_result}")
            return prevention_result
            
        except Exception as e:
            logger.error(f"Data swarm prevention failed: {e}")
            prevention_result['error'] = str(e)
            return prevention_result
    
    def _process_duplicates(self, duplicate_groups: List[List[Dict[str, Any]]], 
                          source_name: str) -> List[Dict[str, Any]]:
        """Process duplicate groups and merge them"""
        merged_records = []
        
        for group in duplicate_groups:
            try:
                # Find the best record to keep
                best_record = self.deduplicator.select_best_record(group)
                
                # Merge data from all records
                merged_record = self.deduplicator.merge_duplicate_records(group, best_record)
                
                # Save duplicate prevention record
                self._save_duplicate_prevention_record(group, merged_record, source_name)
                
                merged_records.append(merged_record)
                
            except Exception as e:
                logger.error(f"Failed to process duplicate group: {e}")
                # Keep the first record if merging fails
                merged_records.append(group[0])
        
        return merged_records
    
    def _get_non_duplicates(self, incoming_data: List[Dict[str, Any]], 
                          duplicate_groups: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Get records that are not part of any duplicate group"""
        duplicate_records = set()
        for group in duplicate_groups:
            for record in group:
                duplicate_records.add(id(record))
        
        return [record for record in incoming_data if id(record) not in duplicate_records]
    
    def _clean_data(self, record: Dict[str, Any], 
                   quality_result: Dict[str, Any]) -> Dict[str, Any]:
        """Clean data based on quality issues"""
        cleaned_record = record.copy()
        
        # Clean facility name
        if 'facility_name' in cleaned_record:
            cleaned_record['facility_name'] = self._clean_facility_name(
                cleaned_record['facility_name']
            )
        
        # Clean location data
        if 'location' in cleaned_record:
            cleaned_record['location'] = self._clean_location_data(
                cleaned_record['location']
            )
        
        # Clean contact information
        if 'contacts' in cleaned_record:
            cleaned_record['contacts'] = self._clean_contacts(
                cleaned_record['contacts']
            )
        
        return cleaned_record
    
    def _clean_facility_name(self, name: str) -> str:
        """Clean facility name"""
        if not name:
            return name
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Remove common prefixes/suffixes that might cause duplicates
        prefixes_to_remove = ['The ', 'A ', 'An ']
        for prefix in prefixes_to_remove:
            if name.startswith(prefix):
                name = name[len(prefix):]
        
        return name
    
    def _clean_location_data(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Clean location data"""
        cleaned_location = location.copy()
        
        # Clean county name
        if 'county' in cleaned_location:
            cleaned_location['county'] = self._clean_geographic_name(
                cleaned_location['county']
            )
        
        # Clean constituency name
        if 'constituency' in cleaned_location:
            cleaned_location['constituency'] = self._clean_geographic_name(
                cleaned_location['constituency']
            )
        
        # Clean ward name
        if 'ward' in cleaned_location:
            cleaned_location['ward'] = self._clean_geographic_name(
                cleaned_location['ward']
            )
        
        return cleaned_location
    
    def _clean_geographic_name(self, name: str) -> str:
        """Clean geographic name"""
        if not name:
            return name
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Remove common suffixes
        suffixes_to_remove = [' County', ' Constituency', ' Ward']
        for suffix in suffixes_to_remove:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        
        return name
    
    def _clean_contacts(self, contacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean contact information"""
        cleaned_contacts = []
        seen_contacts = set()
        
        for contact in contacts:
            if 'type' not in contact or 'value' not in contact:
                continue
            
            # Clean contact value
            contact_value = contact['value'].strip()
            if not contact_value:
                continue
            
            # Normalize phone numbers
            if contact['type'].lower() in ['phone', 'mobile', 'telephone']:
                contact_value = self._normalize_phone_number(contact_value)
            
            # Normalize email addresses
            elif contact['type'].lower() == 'email':
                contact_value = contact_value.lower().strip()
            
            # Check for duplicates
            contact_key = f"{contact['type']}:{contact_value}"
            if contact_key in seen_contacts:
                continue
            
            seen_contacts.add(contact_key)
            cleaned_contacts.append({
                'type': contact['type'],
                'value': contact_value
            })
        
        return cleaned_contacts
    
    def _normalize_phone_number(self, phone: str) -> str:
        """Normalize phone number format"""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        
        # Handle Kenya phone numbers
        if digits.startswith('254'):
            return f"+{digits}"
        elif digits.startswith('0') and len(digits) == 10:
            return f"+254{digits[1:]}"
        elif len(digits) == 9:
            return f"+254{digits}"
        else:
            return phone  # Return original if can't normalize
    
    def _final_validation(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Final validation of processed records"""
        validation_result = {
            'total_records': len(records),
            'valid_records': 0,
            'invalid_records': 0,
            'average_quality_score': 0.0,
            'issues': []
        }
        
        total_quality_score = 0.0
        
        for record in records:
            quality_result = self.quality_gates.validate_facility_data(record)
            
            if quality_result['is_valid']:
                validation_result['valid_records'] += 1
            else:
                validation_result['invalid_records'] += 1
                validation_result['issues'].extend(quality_result['errors'])
            
            total_quality_score += quality_result['quality_score']
        
        if records:
            validation_result['average_quality_score'] = total_quality_score / len(records)
        
        return validation_result
    
    def _save_duplicate_prevention_record(self, duplicate_group: List[Dict[str, Any]], 
                                        merged_record: Dict[str, Any], 
                                        source_name: str):
        """Save duplicate prevention tracking record"""
        try:
            group_id = hashlib.md5(
                json.dumps(merged_record, sort_keys=True).encode()
            ).hexdigest()[:16]
            
            for i, record in enumerate(duplicate_group):
                DataSwarmPrevention.objects.create(
                    record_id=f"{source_name}_{int(time.time())}_{i}",
                    duplicate_group_id=group_id,
                    similarity_score=0.9,  # Would calculate actual similarity
                    match_strategy='fuzzy_matching',
                    action_taken='merged' if i == 0 else 'merged',
                    prevention_details={
                        'group_size': len(duplicate_group),
                        'merged_into': merged_record.get('facility_name', ''),
                        'source': source_name
                    }
                )
        except Exception as e:
            logger.error(f"Failed to save duplicate prevention record: {e}")


class IntelligentDeduplicator:
    """Intelligent duplicate detection and merging"""
    
    def __init__(self):
        self.similarity_threshold = 0.85
        self.fuzzy_matcher = FuzzyMatcher()
        self.ml_detector = MLDuplicateDetector()
    
    def find_duplicates(self, data: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Find duplicates using multiple strategies"""
        duplicate_groups = []
        processed_indices = set()
        
        for i, record1 in enumerate(data):
            if i in processed_indices:
                continue
            
            duplicate_group = [record1]
            processed_indices.add(i)
            
            for j, record2 in enumerate(data[i+1:], i+1):
                if j in processed_indices:
                    continue
                
                # Check for duplicates using multiple strategies
                if self._is_duplicate(record1, record2):
                    duplicate_group.append(record2)
                    processed_indices.add(j)
            
            # Only add groups with more than one record
            if len(duplicate_group) > 1:
                duplicate_groups.append(duplicate_group)
        
        return duplicate_groups
    
    def _is_duplicate(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Check if two records are duplicates"""
        # Strategy 1: Exact matching on key fields
        if self._exact_match(record1, record2):
            return True
        
        # Strategy 2: Fuzzy matching on facility name
        if self._fuzzy_name_match(record1, record2):
            return True
        
        # Strategy 3: Location-based matching
        if self._location_match(record1, record2):
            return True
        
        # Strategy 4: ML-based detection
        if self._ml_duplicate_detection(record1, record2):
            return True
        
        return False
    
    def _exact_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Exact matching on key fields"""
        key_fields = ['facility_name', 'location.county', 'location.constituency']
        
        for field in key_fields:
            value1 = self._get_nested_value(record1, field)
            value2 = self._get_nested_value(record2, field)
            
            if value1 and value2 and value1.lower().strip() == value2.lower().strip():
                continue
            else:
                return False
        
        return True
    
    def _fuzzy_name_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Fuzzy matching on facility names"""
        name1 = record1.get('facility_name', '').lower().strip()
        name2 = record2.get('facility_name', '').lower().strip()
        
        if not name1 or not name2:
            return False
        
        similarity = self.fuzzy_matcher.calculate_similarity(name1, name2)
        return similarity >= self.similarity_threshold
    
    def _location_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Location-based duplicate detection"""
        loc1 = record1.get('location', {})
        loc2 = record2.get('location', {})
        
        # Check if coordinates are very close
        if (loc1.get('latitude') and loc1.get('longitude') and 
            loc2.get('latitude') and loc2.get('longitude')):
            
            distance = self._calculate_distance(
                loc1['latitude'], loc1['longitude'],
                loc2['latitude'], loc2['longitude']
            )
            
            # Consider duplicates if within 100 meters
            if distance < 0.1:  # 100 meters in degrees (approximate)
                return True
        
        # Check county and constituency match
        county1 = loc1.get('county', '').lower().strip()
        county2 = loc2.get('county', '').lower().strip()
        constituency1 = loc1.get('constituency', '').lower().strip()
        constituency2 = loc2.get('constituency', '').lower().strip()
        
        if county1 and county2 and constituency1 and constituency2:
            if county1 == county2 and constituency1 == constituency2:
                # Check if facility names are similar
                name1 = record1.get('facility_name', '').lower().strip()
                name2 = record2.get('facility_name', '').lower().strip()
                
                if name1 and name2:
                    similarity = self.fuzzy_matcher.calculate_similarity(name1, name2)
                    return similarity >= 0.7  # Lower threshold for location-based matching
        
        return False
    
    def _ml_duplicate_detection(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """ML-based duplicate detection"""
        # This would use machine learning models
        # For now, return False
        return False
    
    def select_best_record(self, duplicate_group: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best record from a duplicate group"""
        if len(duplicate_group) == 1:
            return duplicate_group[0]
        
        # Score each record based on completeness and quality
        best_record = None
        best_score = -1
        
        for record in duplicate_group:
            score = self._calculate_record_score(record)
            if score > best_score:
                best_score = score
                best_record = record
        
        return best_record
    
    def _calculate_record_score(self, record: Dict[str, Any]) -> float:
        """Calculate quality score for a record"""
        score = 0.0
        
        # Completeness score
        required_fields = ['facility_name', 'location', 'contacts']
        completeness = sum(
            1 for field in required_fields 
            if field in record and record[field]
        ) / len(required_fields)
        score += completeness * 0.4
        
        # Location completeness
        location = record.get('location', {})
        location_fields = ['county', 'constituency', 'ward', 'latitude', 'longitude']
        location_completeness = sum(
            1 for field in location_fields 
            if field in location and location[field]
        ) / len(location_fields)
        score += location_completeness * 0.3
        
        # Contact completeness
        contacts = record.get('contacts', [])
        if contacts:
            score += 0.2
        
        # Data quality indicators
        facility_name = record.get('facility_name', '')
        if len(facility_name) > 5:  # Longer names are usually more descriptive
            score += 0.1
        
        return score
    
    def merge_duplicate_records(self, duplicate_group: List[Dict[str, Any]], 
                              best_record: Dict[str, Any]) -> Dict[str, Any]:
        """Merge duplicate records into the best record"""
        merged_record = best_record.copy()
        
        # Merge contact information
        all_contacts = []
        for record in duplicate_group:
            contacts = record.get('contacts', [])
            all_contacts.extend(contacts)
        
        # Remove duplicate contacts
        unique_contacts = []
        seen_contacts = set()
        for contact in all_contacts:
            contact_key = f"{contact.get('type', '')}:{contact.get('value', '')}"
            if contact_key not in seen_contacts:
                unique_contacts.append(contact)
                seen_contacts.add(contact_key)
        
        merged_record['contacts'] = unique_contacts
        
        # Merge services
        all_services = []
        for record in duplicate_group:
            services = record.get('services', [])
            all_services.extend(services)
        
        # Remove duplicate services
        unique_services = []
        seen_services = set()
        for service in all_services:
            service_key = f"{service.get('category', '')}:{service.get('description', '')}"
            if service_key not in seen_services:
                unique_services.append(service)
                seen_services.add(service_key)
        
        merged_record['services'] = unique_services
        
        # Add merge metadata
        merged_record['_merge_metadata'] = {
            'merged_from': len(duplicate_group),
            'merge_timestamp': time.time(),
            'original_records': [r.get('facility_name', '') for r in duplicate_group]
        }
        
        return merged_record
    
    def _get_nested_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Get nested value from dictionary using dot notation"""
        keys = field_path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def _calculate_distance(self, lat1: float, lng1: float, 
                          lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in degrees"""
        # Simple Euclidean distance (not accurate for large distances)
        return ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5


class FuzzyMatcher:
    """Fuzzy string matching for duplicate detection"""
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        if not str1 or not str2:
            return 0.0
        
        # Normalize strings
        str1 = self._normalize_string(str1)
        str2 = self._normalize_string(str2)
        
        # Use SequenceMatcher for similarity
        matcher = SequenceMatcher(None, str1, str2)
        return matcher.ratio()
    
    def _normalize_string(self, text: str) -> str:
        """Normalize string for comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common words that don't add meaning
        stop_words = {'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for'}
        words = text.split()
        words = [word for word in words if word not in stop_words]
        
        return ' '.join(words)


class MLDuplicateDetector:
    """Machine learning-based duplicate detection"""
    
    def __init__(self):
        # This would initialize ML models
        pass
    
    def find_duplicates(self, data: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Find duplicates using ML models"""
        # This would use trained ML models
        # For now, return empty list
        return []
    
    def train_model(self, training_data: List[Dict[str, Any]]):
        """Train ML model on training data"""
        # This would train the model
        pass
"""
Data Swarm Prevention System
Intelligent deduplication and data quality management
"""

import hashlib
import json
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from difflib import SequenceMatcher
from django.db import transaction
from .models import DataSwarmPrevention, RawDataRecord, ValidatedDataRecord
from .data_validation import DataValidator

logger = logging.getLogger(__name__)


class DataSwarmPreventionSystem:
    """Comprehensive data swarm prevention system"""
    
    def __init__(self):
        self.deduplicator = IntelligentDeduplicator()
        self.quality_gates = DataValidator()
        self.similarity_threshold = 0.85
        self.duplicate_groups = {}
    
    def prevent_data_swarm(self, incoming_data: List[Dict[str, Any]], 
                          source_name: str) -> Dict[str, Any]:
        """Main data swarm prevention pipeline"""
        prevention_result = {
            'total_records': len(incoming_data),
            'duplicates_found': 0,
            'duplicates_merged': 0,
            'quality_issues': 0,
            'data_cleaned': False,
            'processed_records': [],
            'prevention_details': {}
        }
        
        try:
            # Step 1: Detect duplicates
            duplicate_groups = self.deduplicator.find_duplicates(incoming_data)
            prevention_result['duplicates_found'] = len(duplicate_groups)
            prevention_result['prevention_details']['duplicate_groups'] = duplicate_groups
            
            # Step 2: Process duplicates
            if duplicate_groups:
                merged_data = self._process_duplicates(duplicate_groups, source_name)
                prevention_result['duplicates_merged'] = len(merged_data)
                prevention_result['processed_records'].extend(merged_data)
            
            # Step 3: Quality validation for non-duplicates
            non_duplicates = self._get_non_duplicates(incoming_data, duplicate_groups)
            quality_results = []
            
            for record in non_duplicates:
                quality_result = self.quality_gates.validate_facility_data(record)
                quality_results.append(quality_result)
                
                if not quality_result['is_valid']:
                    prevention_result['quality_issues'] += 1
                
                # Clean data if needed
                if quality_result['quality_score'] < 0.8:
                    cleaned_record = self._clean_data(record, quality_result)
                    prevention_result['data_cleaned'] = True
                    prevention_result['processed_records'].append(cleaned_record)
                else:
                    prevention_result['processed_records'].append(record)
            
            prevention_result['prevention_details']['quality_results'] = quality_results
            
            # Step 4: Final validation
            final_validation = self._final_validation(prevention_result['processed_records'])
            prevention_result['prevention_details']['final_validation'] = final_validation
            
            logger.info(f"Data swarm prevention completed: {prevention_result}")
            return prevention_result
            
        except Exception as e:
            logger.error(f"Data swarm prevention failed: {e}")
            prevention_result['error'] = str(e)
            return prevention_result
    
    def _process_duplicates(self, duplicate_groups: List[List[Dict[str, Any]]], 
                          source_name: str) -> List[Dict[str, Any]]:
        """Process duplicate groups and merge them"""
        merged_records = []
        
        for group in duplicate_groups:
            try:
                # Find the best record to keep
                best_record = self.deduplicator.select_best_record(group)
                
                # Merge data from all records
                merged_record = self.deduplicator.merge_duplicate_records(group, best_record)
                
                # Save duplicate prevention record
                self._save_duplicate_prevention_record(group, merged_record, source_name)
                
                merged_records.append(merged_record)
                
            except Exception as e:
                logger.error(f"Failed to process duplicate group: {e}")
                # Keep the first record if merging fails
                merged_records.append(group[0])
        
        return merged_records
    
    def _get_non_duplicates(self, incoming_data: List[Dict[str, Any]], 
                          duplicate_groups: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Get records that are not part of any duplicate group"""
        duplicate_records = set()
        for group in duplicate_groups:
            for record in group:
                duplicate_records.add(id(record))
        
        return [record for record in incoming_data if id(record) not in duplicate_records]
    
    def _clean_data(self, record: Dict[str, Any], 
                   quality_result: Dict[str, Any]) -> Dict[str, Any]:
        """Clean data based on quality issues"""
        cleaned_record = record.copy()
        
        # Clean facility name
        if 'facility_name' in cleaned_record:
            cleaned_record['facility_name'] = self._clean_facility_name(
                cleaned_record['facility_name']
            )
        
        # Clean location data
        if 'location' in cleaned_record:
            cleaned_record['location'] = self._clean_location_data(
                cleaned_record['location']
            )
        
        # Clean contact information
        if 'contacts' in cleaned_record:
            cleaned_record['contacts'] = self._clean_contacts(
                cleaned_record['contacts']
            )
        
        return cleaned_record
    
    def _clean_facility_name(self, name: str) -> str:
        """Clean facility name"""
        if not name:
            return name
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Remove common prefixes/suffixes that might cause duplicates
        prefixes_to_remove = ['The ', 'A ', 'An ']
        for prefix in prefixes_to_remove:
            if name.startswith(prefix):
                name = name[len(prefix):]
        
        return name
    
    def _clean_location_data(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Clean location data"""
        cleaned_location = location.copy()
        
        # Clean county name
        if 'county' in cleaned_location:
            cleaned_location['county'] = self._clean_geographic_name(
                cleaned_location['county']
            )
        
        # Clean constituency name
        if 'constituency' in cleaned_location:
            cleaned_location['constituency'] = self._clean_geographic_name(
                cleaned_location['constituency']
            )
        
        # Clean ward name
        if 'ward' in cleaned_location:
            cleaned_location['ward'] = self._clean_geographic_name(
                cleaned_location['ward']
            )
        
        return cleaned_location
    
    def _clean_geographic_name(self, name: str) -> str:
        """Clean geographic name"""
        if not name:
            return name
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Remove common suffixes
        suffixes_to_remove = [' County', ' Constituency', ' Ward']
        for suffix in suffixes_to_remove:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        
        return name
    
    def _clean_contacts(self, contacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean contact information"""
        cleaned_contacts = []
        seen_contacts = set()
        
        for contact in contacts:
            if 'type' not in contact or 'value' not in contact:
                continue
            
            # Clean contact value
            contact_value = contact['value'].strip()
            if not contact_value:
                continue
            
            # Normalize phone numbers
            if contact['type'].lower() in ['phone', 'mobile', 'telephone']:
                contact_value = self._normalize_phone_number(contact_value)
            
            # Normalize email addresses
            elif contact['type'].lower() == 'email':
                contact_value = contact_value.lower().strip()
            
            # Check for duplicates
            contact_key = f"{contact['type']}:{contact_value}"
            if contact_key in seen_contacts:
                continue
            
            seen_contacts.add(contact_key)
            cleaned_contacts.append({
                'type': contact['type'],
                'value': contact_value
            })
        
        return cleaned_contacts
    
    def _normalize_phone_number(self, phone: str) -> str:
        """Normalize phone number format"""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        
        # Handle Kenya phone numbers
        if digits.startswith('254'):
            return f"+{digits}"
        elif digits.startswith('0') and len(digits) == 10:
            return f"+254{digits[1:]}"
        elif len(digits) == 9:
            return f"+254{digits}"
        else:
            return phone  # Return original if can't normalize
    
    def _final_validation(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Final validation of processed records"""
        validation_result = {
            'total_records': len(records),
            'valid_records': 0,
            'invalid_records': 0,
            'average_quality_score': 0.0,
            'issues': []
        }
        
        total_quality_score = 0.0
        
        for record in records:
            quality_result = self.quality_gates.validate_facility_data(record)
            
            if quality_result['is_valid']:
                validation_result['valid_records'] += 1
            else:
                validation_result['invalid_records'] += 1
                validation_result['issues'].extend(quality_result['errors'])
            
            total_quality_score += quality_result['quality_score']
        
        if records:
            validation_result['average_quality_score'] = total_quality_score / len(records)
        
        return validation_result
    
    def _save_duplicate_prevention_record(self, duplicate_group: List[Dict[str, Any]], 
                                        merged_record: Dict[str, Any], 
                                        source_name: str):
        """Save duplicate prevention tracking record"""
        try:
            group_id = hashlib.md5(
                json.dumps(merged_record, sort_keys=True).encode()
            ).hexdigest()[:16]
            
            for i, record in enumerate(duplicate_group):
                DataSwarmPrevention.objects.create(
                    record_id=f"{source_name}_{int(time.time())}_{i}",
                    duplicate_group_id=group_id,
                    similarity_score=0.9,  # Would calculate actual similarity
                    match_strategy='fuzzy_matching',
                    action_taken='merged' if i == 0 else 'merged',
                    prevention_details={
                        'group_size': len(duplicate_group),
                        'merged_into': merged_record.get('facility_name', ''),
                        'source': source_name
                    }
                )
        except Exception as e:
            logger.error(f"Failed to save duplicate prevention record: {e}")


class IntelligentDeduplicator:
    """Intelligent duplicate detection and merging"""
    
    def __init__(self):
        self.similarity_threshold = 0.85
        self.fuzzy_matcher = FuzzyMatcher()
        self.ml_detector = MLDuplicateDetector()
    
    def find_duplicates(self, data: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Find duplicates using multiple strategies"""
        duplicate_groups = []
        processed_indices = set()
        
        for i, record1 in enumerate(data):
            if i in processed_indices:
                continue
            
            duplicate_group = [record1]
            processed_indices.add(i)
            
            for j, record2 in enumerate(data[i+1:], i+1):
                if j in processed_indices:
                    continue
                
                # Check for duplicates using multiple strategies
                if self._is_duplicate(record1, record2):
                    duplicate_group.append(record2)
                    processed_indices.add(j)
            
            # Only add groups with more than one record
            if len(duplicate_group) > 1:
                duplicate_groups.append(duplicate_group)
        
        return duplicate_groups
    
    def _is_duplicate(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Check if two records are duplicates"""
        # Strategy 1: Exact matching on key fields
        if self._exact_match(record1, record2):
            return True
        
        # Strategy 2: Fuzzy matching on facility name
        if self._fuzzy_name_match(record1, record2):
            return True
        
        # Strategy 3: Location-based matching
        if self._location_match(record1, record2):
            return True
        
        # Strategy 4: ML-based detection
        if self._ml_duplicate_detection(record1, record2):
            return True
        
        return False
    
    def _exact_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Exact matching on key fields"""
        key_fields = ['facility_name', 'location.county', 'location.constituency']
        
        for field in key_fields:
            value1 = self._get_nested_value(record1, field)
            value2 = self._get_nested_value(record2, field)
            
            if value1 and value2 and value1.lower().strip() == value2.lower().strip():
                continue
            else:
                return False
        
        return True
    
    def _fuzzy_name_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Fuzzy matching on facility names"""
        name1 = record1.get('facility_name', '').lower().strip()
        name2 = record2.get('facility_name', '').lower().strip()
        
        if not name1 or not name2:
            return False
        
        similarity = self.fuzzy_matcher.calculate_similarity(name1, name2)
        return similarity >= self.similarity_threshold
    
    def _location_match(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """Location-based duplicate detection"""
        loc1 = record1.get('location', {})
        loc2 = record2.get('location', {})
        
        # Check if coordinates are very close
        if (loc1.get('latitude') and loc1.get('longitude') and 
            loc2.get('latitude') and loc2.get('longitude')):
            
            distance = self._calculate_distance(
                loc1['latitude'], loc1['longitude'],
                loc2['latitude'], loc2['longitude']
            )
            
            # Consider duplicates if within 100 meters
            if distance < 0.1:  # 100 meters in degrees (approximate)
                return True
        
        # Check county and constituency match
        county1 = loc1.get('county', '').lower().strip()
        county2 = loc2.get('county', '').lower().strip()
        constituency1 = loc1.get('constituency', '').lower().strip()
        constituency2 = loc2.get('constituency', '').lower().strip()
        
        if county1 and county2 and constituency1 and constituency2:
            if county1 == county2 and constituency1 == constituency2:
                # Check if facility names are similar
                name1 = record1.get('facility_name', '').lower().strip()
                name2 = record2.get('facility_name', '').lower().strip()
                
                if name1 and name2:
                    similarity = self.fuzzy_matcher.calculate_similarity(name1, name2)
                    return similarity >= 0.7  # Lower threshold for location-based matching
        
        return False
    
    def _ml_duplicate_detection(self, record1: Dict[str, Any], record2: Dict[str, Any]) -> bool:
        """ML-based duplicate detection"""
        # This would use machine learning models
        # For now, return False
        return False
    
    def select_best_record(self, duplicate_group: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best record from a duplicate group"""
        if len(duplicate_group) == 1:
            return duplicate_group[0]
        
        # Score each record based on completeness and quality
        best_record = None
        best_score = -1
        
        for record in duplicate_group:
            score = self._calculate_record_score(record)
            if score > best_score:
                best_score = score
                best_record = record
        
        return best_record
    
    def _calculate_record_score(self, record: Dict[str, Any]) -> float:
        """Calculate quality score for a record"""
        score = 0.0
        
        # Completeness score
        required_fields = ['facility_name', 'location', 'contacts']
        completeness = sum(
            1 for field in required_fields 
            if field in record and record[field]
        ) / len(required_fields)
        score += completeness * 0.4
        
        # Location completeness
        location = record.get('location', {})
        location_fields = ['county', 'constituency', 'ward', 'latitude', 'longitude']
        location_completeness = sum(
            1 for field in location_fields 
            if field in location and location[field]
        ) / len(location_fields)
        score += location_completeness * 0.3
        
        # Contact completeness
        contacts = record.get('contacts', [])
        if contacts:
            score += 0.2
        
        # Data quality indicators
        facility_name = record.get('facility_name', '')
        if len(facility_name) > 5:  # Longer names are usually more descriptive
            score += 0.1
        
        return score
    
    def merge_duplicate_records(self, duplicate_group: List[Dict[str, Any]], 
                              best_record: Dict[str, Any]) -> Dict[str, Any]:
        """Merge duplicate records into the best record"""
        merged_record = best_record.copy()
        
        # Merge contact information
        all_contacts = []
        for record in duplicate_group:
            contacts = record.get('contacts', [])
            all_contacts.extend(contacts)
        
        # Remove duplicate contacts
        unique_contacts = []
        seen_contacts = set()
        for contact in all_contacts:
            contact_key = f"{contact.get('type', '')}:{contact.get('value', '')}"
            if contact_key not in seen_contacts:
                unique_contacts.append(contact)
                seen_contacts.add(contact_key)
        
        merged_record['contacts'] = unique_contacts
        
        # Merge services
        all_services = []
        for record in duplicate_group:
            services = record.get('services', [])
            all_services.extend(services)
        
        # Remove duplicate services
        unique_services = []
        seen_services = set()
        for service in all_services:
            service_key = f"{service.get('category', '')}:{service.get('description', '')}"
            if service_key not in seen_services:
                unique_services.append(service)
                seen_services.add(service_key)
        
        merged_record['services'] = unique_services
        
        # Add merge metadata
        merged_record['_merge_metadata'] = {
            'merged_from': len(duplicate_group),
            'merge_timestamp': time.time(),
            'original_records': [r.get('facility_name', '') for r in duplicate_group]
        }
        
        return merged_record
    
    def _get_nested_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Get nested value from dictionary using dot notation"""
        keys = field_path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def _calculate_distance(self, lat1: float, lng1: float, 
                          lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in degrees"""
        # Simple Euclidean distance (not accurate for large distances)
        return ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5


class FuzzyMatcher:
    """Fuzzy string matching for duplicate detection"""
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        if not str1 or not str2:
            return 0.0
        
        # Normalize strings
        str1 = self._normalize_string(str1)
        str2 = self._normalize_string(str2)
        
        # Use SequenceMatcher for similarity
        matcher = SequenceMatcher(None, str1, str2)
        return matcher.ratio()
    
    def _normalize_string(self, text: str) -> str:
        """Normalize string for comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common words that don't add meaning
        stop_words = {'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for'}
        words = text.split()
        words = [word for word in words if word not in stop_words]
        
        return ' '.join(words)


class MLDuplicateDetector:
    """Machine learning-based duplicate detection"""
    
    def __init__(self):
        # This would initialize ML models
        pass
    
    def find_duplicates(self, data: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Find duplicates using ML models"""
        # This would use trained ML models
        # For now, return empty list
        return []
    
    def train_model(self, training_data: List[Dict[str, Any]]):
        """Train ML model on training data"""
        # This would train the model
        pass

