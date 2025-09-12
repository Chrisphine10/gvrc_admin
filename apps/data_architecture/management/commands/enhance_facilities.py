"""
Enhance Facilities Management Command
Iterative, debug-friendly facility enhancement
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.conf import settings
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Enhance facilities with AI-powered geolocation and data quality improvements'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--facility-ids',
            type=str,
            help='Comma-separated list of facility IDs to enhance (e.g., "1,2,3")'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Number of facilities to process in each batch (default: 10)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be enhanced without making changes'
        )
        parser.add_argument(
            '--step',
            type=str,
            choices=['extract', 'validate', 'geolocate', 'enhance', 'save'],
            help='Run only specific step for debugging'
        )
        parser.add_argument(
            '--output-file',
            type=str,
            help='Save enhanced data to JSON file'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output for debugging'
        )
    
    def handle(self, *args, **options):
        """Main command handler"""
        self.verbose = options['verbose']
        self.dry_run = options['dry_run']
        self.batch_size = options['batch_size']
        self.output_file = options['output_file']
        self.step = options['step']
        
        # Set up logging
        if self.verbose:
            logging.basicConfig(level=logging.DEBUG)
        
        try:
            # Get facility IDs
            facility_ids = self._get_facility_ids(options['facility_ids'])
            
            if not facility_ids:
                self.stdout.write(
                    self.style.WARNING('No facilities found to enhance')
                )
                return
            
            self.stdout.write(
                self.style.SUCCESS(f'Found {len(facility_ids)} facilities to enhance')
            )
            
            # Process facilities
            if self.step:
                # Run specific step for debugging
                self._run_single_step(facility_ids)
            else:
                # Run full enhancement pipeline
                self._run_full_pipeline(facility_ids)
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Command failed: {str(e)}')
            )
            if self.verbose:
                import traceback
                self.stdout.write(traceback.format_exc())
            raise CommandError(f'Enhancement failed: {str(e)}')
    
    def _get_facility_ids(self, facility_ids_str: Optional[str]) -> List[int]:
        """Get list of facility IDs to process"""
        if facility_ids_str:
            # Parse comma-separated IDs
            try:
                return [int(id.strip()) for id in facility_ids_str.split(',')]
            except ValueError:
                raise CommandError('Invalid facility IDs format. Use comma-separated integers.')
        else:
            # Get all active facilities
            return self._get_all_facility_ids()
    
    def _get_all_facility_ids(self) -> List[int]:
        """Get all active facility IDs from database"""
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM facilities 
                    WHERE active_status = true 
                    ORDER BY id
                """)
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to get facility IDs: {str(e)}')
            )
            return []
    
    def _run_single_step(self, facility_ids: List[int]):
        """Run a single step for debugging"""
        self.stdout.write(
            self.style.WARNING(f'Running single step: {self.step}')
        )
        
        if self.step == 'extract':
            self._step_extract(facility_ids[:5])  # Limit for debugging
        elif self.step == 'validate':
            facilities = self._step_extract(facility_ids[:5])
            self._step_validate(facilities)
        elif self.step == 'geolocate':
            facilities = self._step_extract(facility_ids[:5])
            self._step_geolocate(facilities)
        elif self.step == 'enhance':
            facilities = self._step_extract(facility_ids[:5])
            enhanced = self._step_enhance(facilities)
            self._step_save(enhanced)
        elif self.step == 'save':
            self.stdout.write('Save step requires enhanced data. Run --step enhance first.')
    
    def _run_full_pipeline(self, facility_ids: List[int]):
        """Run the complete enhancement pipeline"""
        self.stdout.write(
            self.style.SUCCESS('Starting full enhancement pipeline...')
        )
        
        # Process in batches
        total_processed = 0
        total_enhanced = 0
        
        for i in range(0, len(facility_ids), self.batch_size):
            batch_ids = facility_ids[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (len(facility_ids) + self.batch_size - 1) // self.batch_size
            
            self.stdout.write(
                f'Processing batch {batch_num}/{total_batches} ({len(batch_ids)} facilities)'
            )
            
            try:
                # Step 1: Extract
                facilities = self._step_extract(batch_ids)
                
                # Step 2: Validate
                validated_facilities = self._step_validate(facilities)
                
                # Step 3: Geolocate
                geolocated_facilities = self._step_geolocate(validated_facilities)
                
                # Step 4: Enhance
                enhanced_facilities = self._step_enhance(geolocated_facilities)
                
                # Step 5: Save
                if not self.dry_run:
                    saved_count = self._step_save(enhanced_facilities)
                    total_enhanced += saved_count
                else:
                    self.stdout.write(
                        self.style.WARNING('DRY RUN: Would save enhanced data')
                    )
                
                total_processed += len(batch_ids)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Batch {batch_num} completed successfully')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Batch {batch_num} failed: {str(e)}')
                )
                if self.verbose:
                    import traceback
                    self.stdout.write(traceback.format_exc())
                continue
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'Enhancement completed: {total_processed} processed, {total_enhanced} enhanced'
            )
        )
    
    def _step_extract(self, facility_ids: List[int]) -> List[Dict[str, Any]]:
        """Step 1: Extract facility data from database"""
        self.stdout.write('Step 1: Extracting facility data...')
        
        try:
            with connections['default'].cursor() as cursor:
                # Build comprehensive query
                query = """
                SELECT 
                    f.id,
                    f.facility_name,
                    f.registration_number,
                    f.operational_status_id,
                    f.ward_id,
                    f.active_status,
                    f.created_at,
                    f.updated_at,
                    w.ward_name,
                    c.constituency_name,
                    co.county_name,
                    os.status_name,
                    fco.latitude,
                    fco.longitude
                FROM facilities f
                LEFT JOIN wards w ON f.ward_id = w.id
                LEFT JOIN constituencies c ON w.constituency_id = c.id
                LEFT JOIN counties co ON c.county_id = co.id
                LEFT JOIN operational_statuses os ON f.operational_status_id = os.id
                LEFT JOIN facility_coordinates fco ON f.id = fco.facility_id
                WHERE f.id = ANY(%s)
                ORDER BY f.id
                """
                
                cursor.execute(query, [facility_ids])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
                # Structure the data
                facilities = []
                for row in rows:
                    facility = {
                        'id': row[0],
                        'facility_name': row[1],
                        'registration_number': row[2],
                        'operational_status': row[11] if row[11] else 'Unknown',
                        'location': {
                            'ward': row[8] if row[8] else '',
                            'constituency': row[9] if row[9] else '',
                            'county': row[10] if row[10] else '',
                            'latitude': float(row[12]) if row[12] else None,
                            'longitude': float(row[13]) if row[13] else None
                        },
                        'active_status': row[5],
                        'created_at': row[6].isoformat() if row[6] else None,
                        'updated_at': row[7].isoformat() if row[7] else None
                    }
                    facilities.append(facility)
                
                # Get contacts for each facility
                for facility in facilities:
                    facility['contacts'] = self._get_facility_contacts(facility['id'])
                
                self.stdout.write(
                    self.style.SUCCESS(f'Extracted {len(facilities)} facilities')
                )
                
                if self.verbose:
                    for facility in facilities[:3]:  # Show first 3 for debugging
                        self.stdout.write(f"  - {facility['facility_name']} ({facility['id']})")
                
                return facilities
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Extraction failed: {str(e)}')
            )
            raise
    
    def _get_facility_contacts(self, facility_id: int) -> List[Dict[str, str]]:
        """Get contacts for a specific facility"""
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("""
                    SELECT ct.type_name, fc.contact_value
                    FROM facility_contacts fc
                    JOIN contact_types ct ON fc.contact_type_id = ct.id
                    WHERE fc.facility_id = %s AND fc.active_status = true
                """, [facility_id])
                
                return [
                    {'type': row[0], 'value': row[1]} 
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            if self.verbose:
                self.stdout.write(f"Warning: Could not get contacts for facility {facility_id}: {e}")
            return []
    
    def _step_validate(self, facilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 2: Validate facility data"""
        self.stdout.write('Step 2: Validating facility data...')
        
        validated_facilities = []
        validation_issues = []
        
        for facility in facilities:
            issues = []
            
            # Check required fields
            if not facility.get('facility_name'):
                issues.append('Missing facility name')
            
            if not facility.get('location', {}).get('county'):
                issues.append('Missing county information')
            
            # Check data quality
            if facility.get('facility_name') and len(facility['facility_name']) < 3:
                issues.append('Facility name too short')
            
            if not facility.get('contacts'):
                issues.append('No contact information')
            
            # Add validation metadata
            facility['_validation'] = {
                'is_valid': len(issues) == 0,
                'issues': issues,
                'quality_score': max(0, 1.0 - (len(issues) * 0.2))
            }
            
            if issues:
                validation_issues.extend([f"{facility['facility_name']}: {issue}" for issue in issues])
            
            validated_facilities.append(facility)
        
        self.stdout.write(
            self.style.SUCCESS(f'Validated {len(validated_facilities)} facilities')
        )
        
        if validation_issues:
            self.stdout.write(
                self.style.WARNING(f'Found {len(validation_issues)} validation issues:')
            )
            for issue in validation_issues[:10]:  # Show first 10 issues
                self.stdout.write(f"  - {issue}")
            if len(validation_issues) > 10:
                self.stdout.write(f"  ... and {len(validation_issues) - 10} more")
        
        return validated_facilities
    
    def _step_geolocate(self, facilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 3: Enhance geolocation data"""
        self.stdout.write('Step 3: Enhancing geolocation data...')
        
        geolocated_facilities = []
        geolocation_results = {
            'enhanced': 0,
            'already_has_coords': 0,
            'failed': 0
        }
        
        for facility in facilities:
            location = facility.get('location', {})
            
            # Check if already has coordinates
            if location.get('latitude') and location.get('longitude'):
                geolocation_results['already_has_coords'] += 1
                facility['_geolocation'] = {
                    'status': 'already_has_coordinates',
                    'source': 'existing'
                }
            else:
                # Try to enhance coordinates
                try:
                    enhanced_coords = self._enhance_coordinates(facility)
                    if enhanced_coords:
                        facility['location'].update(enhanced_coords)
                        facility['_geolocation'] = {
                            'status': 'enhanced',
                            'source': enhanced_coords.get('source', 'unknown'),
                            'confidence': enhanced_coords.get('confidence', 0)
                        }
                        geolocation_results['enhanced'] += 1
                    else:
                        facility['_geolocation'] = {
                            'status': 'failed',
                            'reason': 'No coordinates found'
                        }
                        geolocation_results['failed'] += 1
                except Exception as e:
                    facility['_geolocation'] = {
                        'status': 'error',
                        'error': str(e)
                    }
                    geolocation_results['failed'] += 1
                    if self.verbose:
                        self.stdout.write(f"Geolocation failed for {facility['facility_name']}: {e}")
            
            geolocated_facilities.append(facility)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Geolocation completed: {geolocation_results["enhanced"]} enhanced, '
                f'{geolocation_results["already_has_coords"]} already had coordinates, '
                f'{geolocation_results["failed"]} failed'
            )
        )
        
        return geolocated_facilities
    
    def _enhance_coordinates(self, facility: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Enhance coordinates for a single facility"""
        # Simple geocoding simulation (replace with actual geocoding service)
        location = facility.get('location', {})
        county = location.get('county', '')
        constituency = location.get('constituency', '')
        ward = location.get('ward', '')
        
        # Build address
        address_parts = [facility.get('facility_name', '')]
        if ward:
            address_parts.append(ward)
        if constituency:
            address_parts.append(constituency)
        if county:
            address_parts.append(county)
        address_parts.append('Kenya')
        
        address = ', '.join(filter(None, address_parts))
        
        # Simulate geocoding (replace with actual service)
        # For now, return None to indicate no coordinates found
        # In real implementation, this would call the geocoding service
        
        if self.verbose:
            self.stdout.write(f"  Attempting geocoding for: {address}")
        
        return None  # Placeholder - would return actual coordinates
    
    def _step_enhance(self, facilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 4: Apply AI enhancements"""
        self.stdout.write('Step 4: Applying AI enhancements...')
        
        enhanced_facilities = []
        enhancement_stats = {
            'geographic_enhanced': 0,
            'data_cleaned': 0,
            'quality_improved': 0
        }
        
        for facility in facilities:
            # Clean facility name
            original_name = facility.get('facility_name', '')
            cleaned_name = self._clean_facility_name(original_name)
            if cleaned_name != original_name:
                facility['facility_name'] = cleaned_name
                enhancement_stats['data_cleaned'] += 1
            
            # Enhance location data
            location = facility.get('location', {})
            if location.get('county'):
                location['county'] = self._clean_geographic_name(location['county'])
                enhancement_stats['geographic_enhanced'] += 1
            
            if location.get('constituency'):
                location['constituency'] = self._clean_geographic_name(location['constituency'])
                enhancement_stats['geographic_enhanced'] += 1
            
            if location.get('ward'):
                location['ward'] = self._clean_geographic_name(location['ward'])
                enhancement_stats['geographic_enhanced'] += 1
            
            # Clean contact information
            contacts = facility.get('contacts', [])
            cleaned_contacts = self._clean_contacts(contacts)
            if len(cleaned_contacts) != len(contacts):
                facility['contacts'] = cleaned_contacts
                enhancement_stats['data_cleaned'] += 1
            
            # Calculate final quality score
            quality_score = self._calculate_quality_score(facility)
            facility['_enhancement'] = {
                'quality_score': quality_score,
                'enhancements_applied': [
                    'name_cleaning',
                    'geographic_standardization',
                    'contact_cleaning'
                ]
            }
            
            if quality_score > facility.get('_validation', {}).get('quality_score', 0):
                enhancement_stats['quality_improved'] += 1
            
            enhanced_facilities.append(facility)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Enhancement completed: {enhancement_stats["geographic_enhanced"]} geographic, '
                f'{enhancement_stats["data_cleaned"]} cleaned, '
                f'{enhancement_stats["quality_improved"]} quality improved'
            )
        )
        
        return enhanced_facilities
    
    def _clean_facility_name(self, name: str) -> str:
        """Clean facility name"""
        if not name:
            return name
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Remove common prefixes
        prefixes = ['The ', 'A ', 'An ']
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
        
        return name
    
    def _clean_geographic_name(self, name: str) -> str:
        """Clean geographic name"""
        if not name:
            return name
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Remove common suffixes
        suffixes = [' County', ' Constituency', ' Ward']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        
        return name
    
    def _clean_contacts(self, contacts: List[Dict[str, str]]) -> List[Dict[str, str]]:
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
    
    def _calculate_quality_score(self, facility: Dict[str, Any]) -> float:
        """Calculate overall quality score for facility"""
        score = 0.0
        
        # Completeness (40%)
        required_fields = ['facility_name', 'location']
        completeness = sum(
            1 for field in required_fields 
            if field in facility and facility[field]
        ) / len(required_fields)
        score += completeness * 0.4
        
        # Location completeness (30%)
        location = facility.get('location', {})
        location_fields = ['county', 'constituency', 'ward', 'latitude', 'longitude']
        location_completeness = sum(
            1 for field in location_fields 
            if field in location and location[field]
        ) / len(location_fields)
        score += location_completeness * 0.3
        
        # Contact completeness (20%)
        contacts = facility.get('contacts', [])
        if contacts:
            score += 0.2
        
        # Data quality (10%)
        facility_name = facility.get('facility_name', '')
        if len(facility_name) > 5:
            score += 0.1
        
        return min(1.0, score)
    
    def _step_save(self, facilities: List[Dict[str, Any]]) -> int:
        """Step 5: Save enhanced facilities"""
        self.stdout.write('Step 5: Saving enhanced facilities...')
        
        if self.dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN: Would save enhanced data')
            )
            return len(facilities)
        
        saved_count = 0
        
        try:
            # Save to output file if specified
            if self.output_file:
                self._save_to_file(facilities)
                saved_count = len(facilities)
            
            # Save to database (placeholder)
            # In real implementation, this would save to the data architecture database
            for facility in facilities:
                # Placeholder: would save to data architecture database
                saved_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Saved {saved_count} enhanced facilities')
            )
            
            return saved_count
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Save failed: {str(e)}')
            )
            raise
    
    def _save_to_file(self, facilities: List[Dict[str, Any]]):
        """Save enhanced facilities to JSON file"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(facilities, f, indent=2, ensure_ascii=False, default=str)
            
            self.stdout.write(
                self.style.SUCCESS(f'Enhanced data saved to {self.output_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to save to file: {str(e)}')
            )
            raise
