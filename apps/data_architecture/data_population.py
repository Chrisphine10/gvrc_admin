"""
Data Population System
Populates the database with sample data for testing and demonstration
"""

import logging
import json
import random
import pandas as pd
import os
import re
import pdfplumber
import docx
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from django.utils import timezone
import openpyxl
from openpyxl import load_workbook
from django.db import transaction
from .models import DataSource, RawDataRecord, ValidatedDataRecord, EnrichedDataRecord
from .data_source_integration import integration_manager
from apps.facilities.models import Facility, FacilityContact, FacilityCoordinate, FacilityGBVCategory, FacilityInfrastructure, FacilityOwner, FacilityService
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import OperationalStatus, ContactType, GBVCategory, InfrastructureType, OwnerType, ServiceCategory, DocumentType, ConditionStatus
from apps.documents.models import Document
from apps.authentication.models import User

logger = logging.getLogger(__name__)


class DataPopulator:
    """Populates the database with comprehensive sample data"""
    
    def __init__(self):
        self.sample_data = self._load_sample_data()
        self.data_folder = "facilities_import/data/raw"
        self.user = self._get_or_create_user()
        
        # Initialize duplicate prevention caches
        self._facility_name_cache = set()
        self._facility_code_cache = set()
        self._registration_number_cache = set()
        self._load_existing_facilities()
    
    def _load_sample_data(self) -> Dict[str, Any]:
        """Load sample data templates"""
        return {
            'counties': [
                {'name': 'Nairobi', 'code': '001'},
                {'name': 'Mombasa', 'code': '002'},
                {'name': 'Kisumu', 'code': '003'},
                {'name': 'Nakuru', 'code': '004'},
                {'name': 'Eldoret', 'code': '005'},
                {'name': 'Thika', 'code': '006'},
                {'name': 'Malindi', 'code': '007'},
                {'name': 'Kitale', 'code': '008'},
                {'name': 'Garissa', 'code': '009'},
                {'name': 'Kakamega', 'code': '010'},
            ],
            'facility_types': [
                'Hospital', 'Health Center', 'Clinic', 'Dispensary', 'Maternity Home',
                'Mental Health Center', 'Rehabilitation Center', 'Crisis Center',
                'Safe House', 'Legal Aid Center', 'Police Station', 'Court'
            ],
            'gbv_categories': [
                'Physical Violence', 'Sexual Violence', 'Emotional Violence',
                'Economic Violence', 'Psychological Violence', 'Digital Violence',
                'Intimate Partner Violence', 'Child Abuse', 'Elder Abuse',
                'Human Trafficking', 'Female Genital Mutilation', 'Forced Marriage'
            ],
            'services': [
                'Medical Treatment', 'Counseling', 'Legal Aid', 'Shelter',
                'Emergency Response', 'Rehabilitation', 'Prevention Programs',
                'Awareness Training', 'Support Groups', 'Crisis Intervention',
                'Forensic Services', 'Child Protection'
            ],
            'operational_statuses': [
                'Operational', 'Under Maintenance', 'Temporarily Closed',
                'Under Construction', 'Planned', 'Suspended'
            ],
            'contact_types': [
                'Phone', 'Email', 'WhatsApp', 'Facebook', 'Twitter',
                'Instagram', 'Website', 'Physical Address'
            ],
            'infrastructure_types': [
                'Building', 'Equipment', 'Vehicle', 'Technology', 'Furniture',
                'Medical Equipment', 'Security System', 'Communication System'
            ],
            'owner_types': [
                'Government', 'Private', 'NGO', 'Faith-Based', 'Community',
                'International Organization', 'Partnership'
            ]
        }
    
    def populate_geography_data(self) -> Dict[str, Any]:
        """Populate counties, constituencies, and wards"""
        try:
            with transaction.atomic():
                # Create counties
                counties_created = 0
                for county_data in self.sample_data['counties']:
                    county, created = County.objects.get_or_create(
                        county_name=county_data['name'],
                        defaults={'county_code': county_data['code']}
                    )
                    if created:
                        counties_created += 1
                
                # Create constituencies (2-3 per county)
                constituencies_created = 0
                for county in County.objects.all():
                    for i in range(random.randint(2, 3)):
                        constituency_name = f"{county.county_name} Constituency {i+1}"
                        constituency, created = Constituency.objects.get_or_create(
                            constituency_name=constituency_name,
                            county=county,
                            defaults={'constituency_code': f"{county.county_code}{i+1:02d}"}
                        )
                        if created:
                            constituencies_created += 1
                
                # Create wards (3-5 per constituency)
                wards_created = 0
                for constituency in Constituency.objects.all():
                    for i in range(random.randint(3, 5)):
                        ward_name = f"{constituency.constituency_name} Ward {i+1}"
                        ward, created = Ward.objects.get_or_create(
                            ward_name=ward_name,
                            constituency=constituency,
                            defaults={'ward_code': f"{constituency.constituency_code}{i+1:02d}"}
                        )
                        if created:
                            wards_created += 1
                
                logger.info(f"Geography data populated: {counties_created} counties, {constituencies_created} constituencies, {wards_created} wards")
                return {
                    'status': 'success',
                    'counties': counties_created,
                    'constituencies': constituencies_created,
                    'wards': wards_created
                }
                
        except Exception as e:
            logger.error(f"Geography data population failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def populate_lookup_data(self) -> Dict[str, Any]:
        """Populate lookup tables"""
        try:
            with transaction.atomic():
                results = {}
                
                # Operational Statuses
                statuses_created = 0
                for status_name in self.sample_data['operational_statuses']:
                    status, created = OperationalStatus.objects.get_or_create(
                        status_name=status_name,
                        defaults={'description': f"{status_name} status", 'sort_order': statuses_created}
                    )
                    if created:
                        statuses_created += 1
                results['operational_statuses'] = statuses_created
                
                # Contact Types
                contact_types_created = 0
                for type_name in self.sample_data['contact_types']:
                    contact_type, created = ContactType.objects.get_or_create(
                        type_name=type_name,
                        defaults={'description': f"{type_name} contact method"}
                    )
                    if created:
                        contact_types_created += 1
                results['contact_types'] = contact_types_created
                
                # GBV Categories
                gbv_categories_created = 0
                for category_name in self.sample_data['gbv_categories']:
                    category, created = GBVCategory.objects.get_or_create(
                        category_name=category_name,
                        defaults={'description': f"{category_name} services"}
                    )
                    if created:
                        gbv_categories_created += 1
                results['gbv_categories'] = gbv_categories_created
                
                # Service Categories
                service_categories_created = 0
                for service_name in self.sample_data['services']:
                    service, created = ServiceCategory.objects.get_or_create(
                        category_name=service_name,
                        defaults={'description': f"{service_name} service"}
                    )
                    if created:
                        service_categories_created += 1
                results['service_categories'] = service_categories_created
                
                # Infrastructure Types
                infrastructure_types_created = 0
                for type_name in self.sample_data['infrastructure_types']:
                    infra_type, created = InfrastructureType.objects.get_or_create(
                        type_name=type_name,
                        defaults={'description': f"{type_name} infrastructure"}
                    )
                    if created:
                        infrastructure_types_created += 1
                results['infrastructure_types'] = infrastructure_types_created
                
                # Owner Types
                owner_types_created = 0
                for type_name in self.sample_data['owner_types']:
                    owner_type, created = OwnerType.objects.get_or_create(
                        type_name=type_name,
                        defaults={'description': f"{type_name} ownership"}
                    )
                    if created:
                        owner_types_created += 1
                results['owner_types'] = owner_types_created
                
                logger.info(f"Lookup data populated: {results}")
                return {'status': 'success', 'results': results}
                
        except Exception as e:
            logger.error(f"Lookup data population failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def populate_facilities_data(self, count: int = 50) -> Dict[str, Any]:
        """Populate facilities with comprehensive data"""
        try:
            with transaction.atomic():
                facilities_created = 0
                contacts_created = 0
                coordinates_created = 0
                gbv_categories_created = 0
                infrastructure_created = 0
                owners_created = 0
                services_created = 0
                
                # First, update ward names to be more meaningful
                logger.info("🔄 Updating ward names to be more meaningful...")
                ward_updates = self._create_meaningful_ward_names()
                
                # Process real data sources first
                logger.info("🔄 Processing real data sources...")
                
                # Process KMPDC facilities
                kmpdc_count = self.process_kmpdc_facilities()
                facilities_created += kmpdc_count
                
                # Process police stations
                police_count = self.process_police_stations()
                facilities_created += police_count
                
                # Process shelters
                shelter_count = self.process_shelters()
                facilities_created += shelter_count
                
                # Process healthcare facilities from GeoJSON
                healthcare_count = self.process_healthcare_facilities()
                facilities_created += healthcare_count
                
                # Process GBV Station Pilot data
                gbv_pilot_count = self.process_gbv_station_pilot()
                facilities_created += gbv_pilot_count
                
                # Process FGM Resources
                fgm_resources_count = self.process_fgm_resources()
                
                # Enrich existing facilities with cache data
                enriched_count = self.enrich_facilities_from_cache()
                
                # If we have real data, skip sample data creation
                if facilities_created > 0 or enriched_count > 0:
                    logger.info(f"✅ Created {facilities_created} facilities and enriched {enriched_count} from real data sources")
                    logger.info(f"✅ Updated {ward_updates} ward names to be more meaningful")
                    return {
                        'status': 'success',
                        'facilities': facilities_created,
                        'enriched': enriched_count,
                        'ward_updates': ward_updates,
                        'contacts': contacts_created,
                        'coordinates': coordinates_created,
                        'gbv_categories': gbv_categories_created,
                        'infrastructure': infrastructure_created,
                        'owners': owners_created,
                        'services': services_created,
                        'message': f'Created {facilities_created} facilities and enriched {enriched_count} from real data sources'
                    }
                
                # Get random wards for facilities
                wards = list(Ward.objects.all())
                if not wards:
                    return {'status': 'error', 'message': 'No wards available. Populate geography data first.'}
                
                # Get lookup data
                operational_statuses = list(OperationalStatus.objects.all())
                if not operational_statuses:
                    # Create default operational status if none exist
                    default_status = OperationalStatus.objects.create(
                        status_name='Operational',
                        description='Fully operational facility',
                        sort_order=1
                    )
                    operational_statuses = [default_status]
                
                contact_types = list(ContactType.objects.all())
                gbv_categories = list(GBVCategory.objects.all())
                service_categories = list(ServiceCategory.objects.all())
                infrastructure_types = list(InfrastructureType.objects.all())
                owner_types = list(OwnerType.objects.all())
                
                # Get existing facility count to avoid code conflicts
                existing_count = Facility.objects.count()
                
                for i in range(count):
                    # Create facility
                    ward = random.choice(wards)
                    facility_name = f"{random.choice(self.sample_data['facility_types'])} {existing_count + i + 1}"
                    
                    # Get a user for created_by (use first superuser or create one)
                    from apps.authentication.models import User
                    user = User.objects.filter(is_superuser=True).first()
                    if not user:
                        user = User.objects.create_superuser(
                            email='system@admin.com',
                            password='system123',
                            full_name='System User',
                            phone_number='+254700000000'
                        )
                    
                    facility = Facility.objects.create(
                        facility_name=facility_name,
                        facility_code=f"FAC{existing_count + i + 1:04d}",
                        registration_number=f"REG{existing_count + i + 1:06d}",
                        ward=ward,
                        address_line_1=f"Address {i+1}, {ward.ward_name}",
                        address_line_2=f"Building {i+1}",
                        is_active=True,
                        description=f"Sample facility {i+1} providing GBV services",
                        website_url=f"https://facility{i+1}.example.com" if random.choice([True, False]) else "",
                        operational_status=random.choice(operational_statuses) if operational_statuses else None,
                        created_by=user
                    )
                    facilities_created += 1
                    
                    # Create facility contacts
                    for j in range(random.randint(1, 3)):
                        contact_type = random.choice(contact_types) if contact_types else None
                        contact_value = self._generate_contact_value(contact_type.type_name if contact_type else 'Phone')
                        
                        FacilityContact.objects.create(
                            facility=facility,
                            contact_type=contact_type,
                            contact_value=contact_value,
                            is_primary=(j == 0),
                            created_by=user
                        )
                        contacts_created += 1
                    
                    # Create facility coordinates
                    if random.choice([True, False]):
                        FacilityCoordinate.objects.create(
                            facility=facility,
                            latitude=round(random.uniform(-4.0, 4.0), 6),
                            longitude=round(random.uniform(33.0, 42.0), 6),
                            collection_date=datetime.now().date(),
                            data_source='Sample Data',
                            collection_method='GPS'
                        )
                        coordinates_created += 1
                    
                    # Create GBV categories
                    selected_gbv_categories = random.sample(gbv_categories, random.randint(1, 3)) if gbv_categories else []
                    for gbv_category in selected_gbv_categories:
                        FacilityGBVCategory.objects.create(
                            facility=facility,
                            gbv_category=gbv_category,
                            created_by=user
                        )
                        gbv_categories_created += 1
                    
                    # Create infrastructure
                    for j in range(random.randint(1, 2)):
                        infrastructure_type = random.choice(infrastructure_types) if infrastructure_types else None
                        # Get or create a default condition status
                        from apps.lookups.models import ConditionStatus
                        condition_status, _ = ConditionStatus.objects.get_or_create(
                            status_name='Good',
                            defaults={'description': 'Good condition'}
                        )
                        
                        FacilityInfrastructure.objects.create(
                            facility=facility,
                            infrastructure_type=infrastructure_type,
                            condition_status=condition_status,
                            description=f"Sample {infrastructure_type.type_name if infrastructure_type else 'infrastructure'} {j+1}",
                            capacity=random.randint(10, 100),
                            current_utilization=random.randint(5, 50),
                            is_available=random.choice([True, False]),
                            created_by=user
                        )
                        infrastructure_created += 1
                    
                    # Create owner
                    if owner_types:
                        owner_type = random.choice(owner_types)
                        FacilityOwner.objects.create(
                            facility=facility,
                            owner_type=owner_type,
                            owner_name=f"{owner_type.type_name} Owner {i+1}",
                            created_by=user
                        )
                        owners_created += 1
                    
                    # Create services
                    selected_services = random.sample(service_categories, random.randint(1, 4)) if service_categories else []
                    for service_category in selected_services:
                        FacilityService.objects.create(
                            facility=facility,
                            service_category=service_category,
                            service_name=f"{service_category.category_name} Service",
                            service_description=f"Provides {service_category.category_name} services",
                            is_free=random.choice([True, False]),
                            cost_range=f"KSh {random.randint(500, 5000)} - {random.randint(5000, 50000)}" if not random.choice([True, False]) else "",
                            availability_hours="8:00 AM - 5:00 PM",
                            availability_days="Monday-Friday",
                            appointment_required=random.choice([True, False])
                        )
                        services_created += 1
                
                logger.info(f"Facilities data populated: {facilities_created} facilities, {contacts_created} contacts, {coordinates_created} coordinates")
                return {
                    'status': 'success',
                    'facilities': facilities_created,
                    'contacts': contacts_created,
                    'coordinates': coordinates_created,
                    'gbv_categories': gbv_categories_created,
                    'infrastructure': infrastructure_created,
                    'owners': owners_created,
                    'services': services_created
                }
                
        except Exception as e:
            logger.error(f"Facilities data population failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_contact_value(self, contact_type: str) -> str:
        """Generate appropriate contact value based on type"""
        if contact_type.lower() == 'phone':
            return f"+254{random.randint(700000000, 799999999)}"
        elif contact_type.lower() == 'email':
            return f"contact{random.randint(1, 1000)}@example.com"
        elif contact_type.lower() == 'whatsapp':
            return f"+254{random.randint(700000000, 799999999)}"
        elif contact_type.lower() == 'website':
            return f"https://facility{random.randint(1, 1000)}.example.com"
        elif contact_type.lower() == 'physical address':
            return f"Address {random.randint(1, 1000)}, Nairobi, Kenya"
        else:
            return f"contact_{random.randint(1, 1000)}"
    
    def populate_data_architecture_data(self) -> Dict[str, Any]:
        """Populate data architecture tables with sample data"""
        try:
            with transaction.atomic():
                # Create sample data sources
                data_sources_created = 0
                
                # CSV Data Source
                csv_source = DataSource.objects.create(
                    name='Sample CSV Data',
                    source_type='csv',
                    configuration={
                        'file_path': 'sample_data/facilities.csv',
                        'encoding': 'utf-8',
                        'delimiter': ','
                    },
                    is_active=True
                )
                data_sources_created += 1
                
                # JSON Data Source
                json_source = DataSource.objects.create(
                    name='Sample JSON Data',
                    source_type='json',
                    configuration={
                        'file_path': 'sample_data/facilities.json',
                        'array_key': 'facilities'
                    },
                    is_active=True
                )
                data_sources_created += 1
                
                # API Data Source
                api_source = DataSource.objects.create(
                    name='Sample API Data',
                    source_type='api',
                    configuration={
                        'base_url': 'https://api.example.com',
                        'endpoint': 'facilities',
                        'headers': {'Authorization': 'Bearer token123'},
                        'params': {'format': 'json'}
                    },
                    is_active=True
                )
                data_sources_created += 1
                
                # Create sample raw data records
                raw_records_created = 0
                for i in range(20):
                    sample_data = {
                        'facility_name': f'Sample Facility {i+1}',
                        'address': f'Sample Address {i+1}',
                        'phone': f'+254{random.randint(700000000, 799999999)}',
                        'email': f'facility{i+1}@example.com',
                        'services': random.sample(self.sample_data['services'], random.randint(1, 3))
                    }
                    
                    # Only add coordinates for 80% of sample facilities
                    if i % 10 < 8:  # 80% with coordinates
                        sample_data.update({
                            'latitude': round(random.uniform(-4.0, 4.0), 6),
                            'longitude': round(random.uniform(33.0, 42.0), 6)
                        })
                    # 20% will be created without coordinates
                    
                    # Generate unique data_id and checksum
                    import hashlib
                    data_id = f"sample_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    checksum = hashlib.sha256(json.dumps(sample_data, sort_keys=True).encode()).hexdigest()
                    
                    RawDataRecord.objects.create(
                        source=random.choice([csv_source, json_source, api_source]),
                        data_id=data_id,
                        raw_data=sample_data,
                        metadata={'source_type': 'sample', 'created_by': 'data_populator'},
                        checksum=checksum,
                        processing_status='completed'
                    )
                    raw_records_created += 1
                
                logger.info(f"Data architecture data populated: {data_sources_created} sources, {raw_records_created} raw records")
                return {
                    'status': 'success',
                    'data_sources': data_sources_created,
                    'raw_records': raw_records_created
                }
                
        except Exception as e:
            logger.error(f"Data architecture data population failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def populate_all_data(self) -> Dict[str, Any]:
        """Populate all sample data"""
        try:
            results = {}
            
            # Populate in order of dependencies
            geography_result = self.populate_geography_data()
            results['geography'] = geography_result
            
            if geography_result['status'] == 'success':
                lookup_result = self.populate_lookup_data()
                results['lookup'] = lookup_result
                
                if lookup_result['status'] == 'success':
                    facilities_result = self.populate_facilities_data(100)
                    results['facilities'] = facilities_result
                
                data_arch_result = self.populate_data_architecture_data()
                results['data_architecture'] = data_arch_result
            
            # Calculate totals
            total_created = sum(
                result.get('counties', 0) + result.get('constituencies', 0) + result.get('wards', 0) +
                result.get('facilities', 0) + result.get('contacts', 0) + result.get('coordinates', 0) +
                result.get('data_sources', 0) + result.get('raw_records', 0)
                for result in results.values()
                if isinstance(result, dict) and result.get('status') == 'success'
            )
            
            logger.info(f"All data populated successfully. Total records created: {total_created}")
            return {
                'status': 'success',
                'message': f'Successfully populated {total_created} records',
                'results': results,
                'total_created': total_created
            }
            
        except Exception as e:
            logger.error(f"Data population failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_or_create_user(self):
        """Get or create a user for data processing"""
        try:
            user = User.objects.first()
            if not user:
                user = User.objects.create(
                    username='data_processor',
                    email='processor@gvrc.com',
                    full_name='Data Processor',
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )
            return user
        except Exception as e:
            logger.error(f"Error getting/creating user: {e}")
    
    def _load_existing_facilities(self):
        """Load existing facilities into cache for duplicate prevention"""
        try:
            facilities = Facility.objects.filter(is_active=True).values_list(
                'facility_name', 'facility_code', 'registration_number'
            )
            
            for name, code, reg_num in facilities:
                if name:
                    self._facility_name_cache.add(name.lower().strip())
                if code:
                    self._facility_code_cache.add(code.strip())
                if reg_num:
                    self._registration_number_cache.add(reg_num.strip())
                    
            logger.info(f"Loaded {len(self._facility_name_cache)} existing facilities for duplicate prevention")
        except Exception as e:
            logger.error(f"Error loading existing facilities: {e}")
    
    def _is_duplicate_facility(self, facility_name: str, facility_code: str = None, 
                             registration_number: str = None) -> bool:
        """Check if facility already exists to prevent duplicates"""
        try:
            # Check by name (case insensitive)
            if facility_name and facility_name.lower().strip() in self._facility_name_cache:
                return True
            
            # Check by facility code
            if facility_code and facility_code.strip() in self._facility_code_cache:
                return True
            
            # Check by registration number
            if registration_number and registration_number.strip() in self._registration_number_cache:
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking for duplicate facility: {e}")
            return False
    
    def _add_facility_to_cache(self, facility_name: str, facility_code: str = None, 
                             registration_number: str = None):
        """Add facility to cache after creation"""
        try:
            if facility_name:
                self._facility_name_cache.add(facility_name.lower().strip())
            if facility_code:
                self._facility_code_cache.add(facility_code.strip())
            if registration_number:
                self._registration_number_cache.add(registration_number.strip())
        except Exception as e:
            logger.error(f"Error adding facility to cache: {e}")
            return None
    
    def _create_meaningful_ward_names(self):
        """Replace generic ward names with more meaningful ones based on Kenya's administrative structure"""
        try:
            logger.info("🔄 Updating ward names to be more meaningful...")
            
            # Don't update ward names - this was causing the Westlands issue
            # Instead, just return 0 to indicate no changes were made
            logger.info("✅ Skipping ward name updates to prevent data corruption")
            return 0
            
        except Exception as e:
            logger.error(f"Error updating ward names: {e}")
            return 0
    
    def fix_geolocation_issues(self):
        """Fix geolocation data issues including duplicates and accuracy problems"""
        try:
            logger.info("🔧 Fixing geolocation data issues...")
            
            from apps.facilities.models import FacilityCoordinate
            from apps.geography.models import County
            from django.db import transaction
            import random
            
            fixed_issues = {
                'duplicates_removed': 0,
                'coordinates_updated': 0,
                'missing_coordinates_added': 0
            }
            
            with transaction.atomic():
                # 1. Fix duplicate coordinates by adding small random offsets
                logger.info("🔄 Fixing duplicate coordinates...")
                coords = FacilityCoordinate.objects.filter(is_active=True)
                coord_pairs = {}
                
                for coord in coords:
                    if coord.latitude and coord.longitude:
                        key = (float(coord.latitude), float(coord.longitude))
                        if key not in coord_pairs:
                            coord_pairs[key] = []
                        coord_pairs[key].append(coord)
                
                # Fix duplicates by adding small random offsets
                for (lat, lon), coord_list in coord_pairs.items():
                    if len(coord_list) > 1:
                        # Keep the first coordinate as is, offset the others
                        for i, coord in enumerate(coord_list[1:], 1):
                            # Add small random offset (within ~100m)
                            offset_lat = random.uniform(-0.001, 0.001)  # ~100m
                            offset_lon = random.uniform(-0.001, 0.001)  # ~100m
                            
                            coord.latitude = lat + offset_lat
                            coord.longitude = lon + offset_lon
                            coord.save()
                            fixed_issues['duplicates_removed'] += 1
                
                # 2. Fix coordinates that are too far from their county centers
                logger.info("🔄 Fixing coordinate accuracy by county...")
                
                # Define approximate county centers
                county_centers = {
                    'Nairobi': (-1.2921, 36.8219),
                    'Mombasa': (-4.0437, 39.6682),
                    'Kisumu': (-0.0917, 34.7680),
                    'Nakuru': (-0.3070, 36.0800),
                    'Eldoret': (0.5143, 35.2698),
                    'Thika': (-1.0333, 37.0833),
                    'Nyeri': (-0.4201, 36.9476),
                    'Meru': (0.0463, 37.6559),
                    'Machakos': (-1.5167, 37.2667),
                    'Kakamega': (0.2842, 34.7523),
                    'Bungoma': (0.5695, 34.5584),
                    'Kisii': (-0.6773, 34.7796),
                    'Homa Bay': (-0.5363, 34.4576),
                    'Migori': (-1.0634, 34.4731),
                    'Kericho': (-0.3677, 35.2831),
                    'Bomet': (-0.7814, 35.3416),
                    'Narok': (-1.0803, 35.8711),
                    'Kajiado': (-1.8524, 36.7768),
                    'Garissa': (-0.4532, 39.6461),
                    'Wajir': (1.7471, 40.0573),
                    'Mandera': (3.9375, 41.8569),
                    'Marsabit': (2.3284, 37.9899),
                    'Isiolo': (0.3546, 37.5822),
                    'Meru': (0.0463, 37.6559),
                    'Tharaka Nithi': (-0.2965, 37.7236),
                    'Embu': (-0.5396, 37.4574),
                    'Kitui': (-1.3667, 38.0167),
                    'Makueni': (-2.2833, 37.8333),
                    'Nyandarua': (-0.5333, 36.5833),
                    'Nyeri': (-0.4201, 36.9476),
                    'Kirinyaga': (-0.5000, 37.3333),
                    'Murang\'a': (-0.7833, 37.0333),
                    'Kiambu': (-1.1667, 36.8333),
                    'Taita Taveta': (-3.4000, 38.3667),
                    'Lamu': (-2.2717, 40.9020),
                    'Tana River': (-1.5167, 40.0167),
                    'Kilifi': (-3.5107, 39.9093),
                    'Kwale': (-4.1816, 39.4606),
                    'Trans Nzoia': (1.0167, 35.0167),
                    'West Pokot': (1.5167, 35.1167),
                    'Samburu': (1.1167, 36.7167),
                    'Turkana': (3.1167, 35.6167),
                    'Uasin Gishu': (0.5167, 35.2833),
                    'Elgeyo Marakwet': (0.5167, 35.5167),
                    'Nandi': (0.1167, 35.1167),
                    'Baringo': (0.4667, 35.9667),
                    'Laikipia': (0.2167, 36.3667),
                    'Nakuru': (-0.3070, 36.0800),
                    'Narok': (-1.0803, 35.8711),
                    'Kajiado': (-1.8524, 36.7768),
                    'Kericho': (-0.3677, 35.2831),
                    'Bomet': (-0.7814, 35.3416),
                    'Kakamega': (0.2842, 34.7523),
                    'Vihiga': (0.0833, 34.7167),
                    'Bungoma': (0.5695, 34.5584),
                    'Busia': (0.4667, 34.1167),
                    'Siaya': (0.0667, 34.2833),
                    'Kisumu': (-0.0917, 34.7680),
                    'Homa Bay': (-0.5363, 34.4576),
                    'Migori': (-1.0634, 34.4731),
                    'Kisii': (-0.6773, 34.7796),
                    'Nyamira': (-0.5667, 34.9500)
                }
                
                # Fix coordinates that are too far from county centers
                for county in County.objects.all():
                    county_name = county.county_name
                    if county_name in county_centers:
                        center_lat, center_lon = county_centers[county_name]
                        
                        # Get facilities in this county
                        facilities = Facility.objects.filter(ward__constituency__county=county)
                        coords = FacilityCoordinate.objects.filter(facility__in=facilities, is_active=True)
                        
                        for coord in coords:
                            if coord.latitude and coord.longitude:
                                lat, lon = float(coord.latitude), float(coord.longitude)
                                
                                # Check if coordinate is too far from county center (>2 degrees)
                                lat_diff = abs(lat - center_lat)
                                lon_diff = abs(lon - center_lon)
                                
                                if lat_diff > 2.0 or lon_diff > 2.0:
                                    # Move coordinate closer to county center with some randomness
                                    new_lat = center_lat + random.uniform(-0.5, 0.5)
                                    new_lon = center_lon + random.uniform(-0.5, 0.5)
                                    
                                    coord.latitude = new_lat
                                    coord.longitude = new_lon
                                    coord.save()
                                    fixed_issues['coordinates_updated'] += 1
                
                # 3. Add missing coordinates for facilities without them
                logger.info("🔄 Adding missing coordinates...")
                facilities_without_coords = Facility.objects.filter(facilitycoordinate__isnull=True)
                
                for facility in facilities_without_coords[:1000]:  # Limit to first 1000 to avoid timeout
                    county = facility.ward.constituency.county.county_name
                    if county in county_centers:
                        center_lat, center_lon = county_centers[county]
                        
                        # Add random offset around county center
                        lat = center_lat + random.uniform(-0.3, 0.3)
                        lon = center_lon + random.uniform(-0.3, 0.3)
                        
                        FacilityCoordinate.objects.create(
                            facility=facility,
                            latitude=lat,
                            longitude=lon,
                            collection_date='2025-01-01',
                            data_source='estimated',
                            collection_method='estimated',
                            is_active=True,
                            created_by=self.user,
                            updated_by=self.user
                        )
                        fixed_issues['missing_coordinates_added'] += 1
            
            logger.info(f"✅ Geolocation fixes completed: {fixed_issues}")
            return fixed_issues
            
        except Exception as e:
            logger.error(f"Error fixing geolocation issues: {e}")
            return {'error': str(e)}
    
    def process_all_data_sources(self):
        """Process all data sources from the data folder"""
        logger.info("🚀 Starting comprehensive data processing from all sources")
        
        # Initialize counters for unique facility codes
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {
                'police': 0,
                'gbv_pol': 0,
                'gbv_org': 0,
                'shel': 0,
                'kmpdc': 0
            }
        
        results = {
            'police_stations': 0,
            'gbv_station_pilot': 0,
            'gbv_organizations': 0,
            'shelters': 0,
            'fgm_resources': 0,
            'kmpdc_facilities': 0,
            'documents': 0,
            'errors': []
        }
        
        try:
            # Process Police Stations
            results['police_stations'] = self.process_police_stations()
            
            # Process GBV Station Pilot (additional police stations)
            results['gbv_station_pilot'] = self.process_gbv_station_pilot()
            
            # Process GBV Organizations
            results['gbv_organizations'] = self.process_gbv_organizations()
            
            # Process Shelters
            results['shelters'] = self.process_shelters()
            
            # Process FGM Resources
            results['fgm_resources'] = self.process_fgm_resources()
            
            # Process KMPDC Facilities
            results['kmpdc_facilities'] = self.process_kmpdc_facilities()
            
            # Process Documents
            results['documents'] = self.process_documents()
            
            logger.info(f"✅ Data processing completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in comprehensive data processing: {e}")
            results['errors'].append(str(e))
            return results
    
    def process_police_stations(self):
        """Process police stations from Excel file"""
        logger.info("👮 Processing Police Stations...")
        
        try:
            file_path = os.path.join(self.data_folder, "NAIROBI LIST OF POLICE STATIONS.xlsx")
            if not os.path.exists(file_path):
                logger.warning(f"Police stations file not found: {file_path}")
                return 0
            
            df = pd.read_excel(file_path, sheet_name='Police Stations')
            
            # Clean the data - skip header row
            df = df.iloc[1:].copy()
            df.columns = ['station_name', 'phone_number', 'sub_county']
            df = df.dropna(subset=['station_name'])
            
            created_count = 0
            
            with transaction.atomic():
                for _, row in df.iterrows():
                    try:
                        # Get or create ward (use Nairobi as default)
                        ward = Ward.objects.filter(ward_name__icontains='Nairobi').first()
                        if not ward:
                            # Create a default ward if none exists
                            county = County.objects.filter(county_name__icontains='Nairobi').first()
                            if not county:
                                county = County.objects.create(county_name='Nairobi', county_code='001')
                            constituency = Constituency.objects.filter(constituency_name__icontains='Nairobi').first()
                            if not constituency:
                                constituency = Constituency.objects.create(constituency_name='Nairobi Central', county=county)
                            ward = Ward.objects.create(ward_name='Nairobi Central Ward', constituency=constituency)
                        
                        # Get operational status
                        op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                        if not op_status:
                            op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                        
                        # Create police station facility
                        self.facility_code_counters['police'] += 1
                        facility = Facility.objects.create(
                            facility_name=row['station_name'],
                            facility_code=f"POL_{self.facility_code_counters['police']:06d}",
                            registration_number=f"KPS_{self.facility_code_counters['police']:06d}",
                            operational_status=op_status,
                            ward=ward,
                            address_line_1=f"{row['station_name']}, {row['sub_county']}",
                            description=f"Police Station in {row['sub_county']}",
                            is_active=True,
                        )
                        
                        # Add phone contact if available
                        if pd.notna(row['phone_number']):
                            phone_type = ContactType.objects.filter(type_name='Phone').first()
                            if not phone_type:
                                phone_type = ContactType.objects.create(type_name='Phone', validation_regex='')
                            
                            FacilityContact.objects.create(
                                facility=facility,
                                contact_type=phone_type,
                                contact_value=str(row['phone_number']),
                                is_primary=True,
                                is_active=True,
                                created_by=self.user,
                                updated_by=self.user
                            )
                        
                        # Add GBV categories for police stations
                        gbv_categories = ['Physical Violence', 'Sexual Violence', 'Intimate Partner Violence']
                        for gbv_name in gbv_categories:
                            gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                            if gbv_category:
                                           FacilityGBVCategory.objects.create(
                                               facility=facility,
                                               gbv_category=gbv_category
                                           )
                        
                        created_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error creating police station {row['station_name']}: {e}")
                        continue
            
            logger.info(f"✅ Created {created_count} police stations")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error processing police stations: {e}")
            return 0
    
    def process_gbv_station_pilot(self):
        """Process police stations from GBV SDTATION PILOT.xlsx file"""
        logger.info("👮 Processing GBV Station Pilot Police Stations...")
        
        # Initialize counters if not exists
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {'gbv_pol': 0}
        elif 'gbv_pol' not in self.facility_code_counters:
            self.facility_code_counters['gbv_pol'] = 0
        
        try:
            file_path = os.path.join(self.data_folder, "GBV SDTATION PILOT.xlsx")
            if not os.path.exists(file_path):
                logger.warning(f"GBV Station Pilot file not found: {file_path}")
                return 0
            
            df = pd.read_excel(file_path, sheet_name='Sheet1')
            
            # Find the header row (look for 'REGION' column)
            header_row = None
            for idx, row in df.iterrows():
                if 'REGION' in str(row.values):
                    header_row = idx
                    break
            
            if header_row is None:
                logger.warning("Could not find header row in GBV Station Pilot file")
                return 0
            
            # Set the header row and clean data
            df = df.iloc[header_row:].copy()
            df.columns = df.iloc[0]
            df = df.iloc[1:].reset_index(drop=True)
            
            # Clean column names
            df.columns = ['region', 'county', 'sub_county', 'police_station', 'police_post']
            
            # Remove empty rows and clean data
            df = df.dropna(subset=['police_station', 'police_post'], how='all')
            
            # Clean 'nan' values
            df = df.replace('nan', pd.NA)
            df = df.replace('NaN', pd.NA)
            df = df.replace('', pd.NA)
            
            created_count = 0
            current_region = None
            current_county = None
            current_sub_county = None
            
            for _, row in df.iterrows():
                try:
                    with transaction.atomic():
                        # Track current region, county, sub_county from previous rows
                        if pd.notna(row['region']) and str(row['region']).strip() not in ['nan', 'NaN', '']:
                            current_region = str(row['region']).strip()
                        
                        if pd.notna(row['county']) and str(row['county']).strip() not in ['nan', 'NaN', '']:
                            current_county = str(row['county']).strip()
                        
                        if pd.notna(row['sub_county']) and str(row['sub_county']).strip() not in ['nan', 'NaN', '']:
                            current_sub_county = str(row['sub_county']).strip()
                        
                        # Process police stations
                        if pd.notna(row['police_station']) and str(row['police_station']).strip() not in ['nan', 'NaN', '']:
                            station_name = str(row['police_station']).strip()
                            if station_name and station_name not in ['REGION', 'COUNTY', 'SUB-COUNTY', 'POLICE STATION', 'POLICE POST', 'P/STATION', 'P/POST']:
                                # Extract phone number if present (format: "NAME-0712345678")
                                phone_number = None
                                if '-' in station_name and len(station_name.split('-')[-1]) >= 10:
                                    parts = station_name.split('-')
                                    station_name = '-'.join(parts[:-1])
                                    phone_number = parts[-1]
                                
                                # Use current context for location
                                county_name = current_county or 'Unknown'
                                sub_county_name = current_sub_county or 'Unknown'
                                
                                # Get or create ward based on sub-county
                                ward = Ward.objects.filter(ward_name__icontains=sub_county_name).first()
                                if not ward:
                                    # Create county if needed
                                    county = County.objects.filter(county_name__icontains=county_name).first()
                                    if not county:
                                        county = County.objects.create(county_name=county_name, county_code=f"CNT_{created_count + 1:03d}")
                                    
                                    # Create constituency with unique code
                                    constituency = Constituency.objects.filter(constituency_name__icontains=sub_county_name).first()
                                    if not constituency:
                                        constituency_code = f"{county.county_code}_{created_count + 1:03d}"
                                        constituency = Constituency.objects.create(
                                            constituency_name=sub_county_name, 
                                            county=county,
                                            constituency_code=constituency_code
                                        )
                                    
                                    # Create ward with unique code
                                    ward_code = f"{constituency.constituency_code}_W01"
                                    ward = Ward.objects.create(
                                        ward_name=sub_county_name, 
                                        constituency=constituency,
                                        ward_code=ward_code
                                    )
                                
                                # Get operational status
                                op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                                if not op_status:
                                    op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                                
                                # Create police station facility
                                self.facility_code_counters['gbv_pol'] += 1
                                facility = Facility.objects.create(
                                    facility_name=station_name,
                                    facility_code=f"GBV_POL_{self.facility_code_counters['gbv_pol']:06d}",
                                    registration_number=f"GBV_POL_REG_{self.facility_code_counters['gbv_pol']:06d}",
                                    operational_status=op_status,
                                    ward=ward,
                                    address_line_1=f"{station_name}, {sub_county_name}",
                                    description=f"Police Station in {sub_county_name}, {county_name}",
                                    is_active=True,
                                )
                                
                                # Add phone contact if available
                                if phone_number:
                                    phone_type = ContactType.objects.filter(type_name='Phone').first()
                                    if not phone_type:
                                        phone_type = ContactType.objects.create(type_name='Phone', validation_regex='')
                                    
                                    FacilityContact.objects.create(
                                        facility=facility,
                                        contact_type=phone_type,
                                        contact_value=phone_number,
                                        is_primary=True,
                                        is_active=True,
                                        created_by=self.user,
                                        updated_by=self.user
                                    )
                                
                                # Add GBV categories for police stations
                                gbv_categories = ['Physical Violence', 'Sexual Violence', 'Intimate Partner Violence']
                                for gbv_name in gbv_categories:
                                    gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                                    if gbv_category:
                                        FacilityGBVCategory.objects.create(
                                            facility=facility,
                                            gbv_category=gbv_category
                                        )
                                
                                created_count += 1
                        
                        # Process police posts
                        if pd.notna(row['police_post']) and str(row['police_post']).strip() not in ['nan', 'NaN', '']:
                            post_name = str(row['police_post']).strip()
                            if post_name and post_name not in ['REGION', 'COUNTY', 'SUB-COUNTY', 'POLICE STATION', 'POLICE POST', 'P/STATION', 'P/POST']:
                                # Use current context for location
                                county_name = current_county or 'Unknown'
                                sub_county_name = current_sub_county or 'Unknown'
                                
                                # Get or create ward based on sub-county
                                ward = Ward.objects.filter(ward_name__icontains=sub_county_name).first()
                                if not ward:
                                    # Create county if needed
                                    county = County.objects.filter(county_name__icontains=county_name).first()
                                    if not county:
                                        county = County.objects.create(county_name=county_name, county_code=f"CNT_{created_count + 1:03d}")
                                    
                                    # Create constituency
                                    constituency = Constituency.objects.filter(constituency_name__icontains=sub_county_name).first()
                                    if not constituency:
                                        constituency = Constituency.objects.create(constituency_name=sub_county_name, county=county)
                                    
                                    # Create ward
                                    ward = Ward.objects.create(ward_name=sub_county_name, constituency=constituency)
                                
                                # Get operational status
                                op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                                if not op_status:
                                    op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                                
                                # Create police post facility
                                self.facility_code_counters['gbv_pol'] += 1
                                facility = Facility.objects.create(
                                    facility_name=post_name,
                                    facility_code=f"GBV_POST_{self.facility_code_counters['gbv_pol']:06d}",
                                    registration_number=f"GBV_POST_REG_{self.facility_code_counters['gbv_pol']:06d}",
                                    operational_status=op_status,
                                    ward=ward,
                                    address_line_1=f"{post_name}, {sub_county_name}",
                                    description=f"Police Post in {sub_county_name}, {county_name}",
                                    is_active=True,
                                )
                                
                                # Add GBV categories for police posts
                                gbv_categories = ['Physical Violence', 'Sexual Violence', 'Intimate Partner Violence']
                                for gbv_name in gbv_categories:
                                    gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                                    if gbv_category:
                                        FacilityGBVCategory.objects.create(
                                            facility=facility,
                                            gbv_category=gbv_category
                                        )
                                
                                created_count += 1
                        
                except Exception as e:
                    logger.error(f"Error creating GBV station pilot facility: {e}")
                    continue
            
            logger.info(f"✅ Created {created_count} GBV station pilot facilities")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error processing GBV station pilot: {e}")
            return 0
    
    def process_gbv_organizations(self):
        """Process GBV organizations from DOCX file with comprehensive parsing"""
        logger.info("🏛️ Processing GBV Organizations...")
        
        try:
            file_path = os.path.join(self.data_folder, "GBV Support Organizations, Legal, Psychological and Child Protection.docx")
            if not os.path.exists(file_path):
                logger.warning(f"GBV organizations file not found: {file_path}")
                return 0
            
            # Parse DOCX file
            doc = docx.Document(file_path)
            organizations = self._extract_gbv_organizations_from_docx(doc)
            
            created_count = 0
            
            for org in organizations:
                try:
                    with transaction.atomic():
                        # Get or create ward based on county
                        ward = self._get_or_create_ward_for_county(org.get('county', 'Nairobi'))
                        
                        # Get operational status
                        op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                        if not op_status:
                            op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                        
                        # Create facility
                        self.facility_code_counters['gbv_org'] += 1
                        facility = Facility.objects.create(
                            facility_name=org['name'],
                            facility_code=f"GBV_ORG_{self.facility_code_counters['gbv_org']:06d}",
                            registration_number=f"GBV_ORG_REG_{self.facility_code_counters['gbv_org']:06d}",
                            operational_status=op_status,
                            ward=ward,
                            address_line_1=f"{org['name']} Office",
                            description=org.get('description', 'GBV Support Organization'),
                            is_active=True,
                        )
                        
                        # Add contacts from GBV organizations
                        for contact in org.get('contacts', []):
                            contact_type = self._determine_contact_type(contact)
                            if contact_type:
                                contact_type_obj = ContactType.objects.filter(type_name=contact_type).first()
                                if not contact_type_obj:
                                    contact_type_obj = ContactType.objects.create(
                                        type_name=contact_type,
                                        validation_regex=""
                                    )
                                
                                FacilityContact.objects.create(
                                    facility=facility,
                                    contact_type=contact_type_obj,
                                    contact_value=contact,
                                    is_primary=True,
                                    is_active=True,
                                    created_by=self.user,
                                    updated_by=self.user
                                )
                        
                        # Add services based on organization type
                        services = self._get_services_for_organization_type(org.get('type', 'General'))
                        for service_name in services:
                            service_category = ServiceCategory.objects.filter(category_name=service_name).first()
                            if not service_category:
                                service_category = ServiceCategory.objects.create(
                                    category_name=service_name,
                                    description=f"{service_name} services"
                                )
                            
                            FacilityService.objects.create(
                                facility=facility,
                                service_category=service_category,
                                service_name=service_name,
                                service_description=f"Provides {service_name} services",
                                is_free=True,
                                availability_hours="8:00 AM - 5:00 PM",
                                availability_days="Monday-Friday",
                                appointment_required=False
                            )
                        
                        # Add GBV categories based on organization type
                        gbv_categories = self._get_gbv_categories_for_organization_type(org.get('type', 'General'))
                        for gbv_name in gbv_categories:
                            gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                            if gbv_category:
                                FacilityGBVCategory.objects.create(
                                    facility=facility,
                                    gbv_category=gbv_category
                                )
                        
                        created_count += 1
                        
                except Exception as e:
                    logger.error(f"Error creating GBV organization {org.get('name', 'Unknown')}: {e}")
                    continue
            
            logger.info(f"✅ Created {created_count} GBV organizations")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error processing GBV organizations: {e}")
            return 0
    
    def process_shelters(self):
        """Process shelters from PDF file with comprehensive extraction"""
        logger.info("🏠 Processing Shelters...")
        
        try:
            file_path = os.path.join(self.data_folder, "National_Shelters_Network_a5a50b19.pdf")
            if not os.path.exists(file_path):
                logger.warning(f"Shelters file not found: {file_path}")
                return 0
            
            # Extract shelters using pdfplumber
            shelters = self._extract_shelters_from_pdf(file_path)
            
            created_count = 0
            
            for shelter in shelters:
                try:
                    with transaction.atomic():
                        # Get or create ward based on county
                        ward = self._get_or_create_ward_for_county(shelter.get('county', 'Nairobi'))
                        
                        # Get operational status
                        op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                        if not op_status:
                            op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                        
                        # Create facility
                        self.facility_code_counters['shel'] += 1
                        facility = Facility.objects.create(
                            facility_name=shelter['name'],
                            facility_code=f"SHEL_{self.facility_code_counters['shel']:06d}",
                            registration_number=f"SHEL_REG_{self.facility_code_counters['shel']:06d}",
                            operational_status=op_status,
                            ward=ward,
                            address_line_1=f"{shelter['name']} Location",
                            description=f"Shelter for GBV survivors (Capacity: {shelter.get('capacity', 'Unknown')})",
                            is_active=True,
                        )
                        
                        # Add contacts if available
                        for contact in shelter.get('contacts', []):
                            contact_type = self._determine_contact_type(contact)
                            if contact_type:
                                contact_type_obj = ContactType.objects.filter(type_name=contact_type).first()
                                if not contact_type_obj:
                                    contact_type_obj = ContactType.objects.create(
                                        type_name=contact_type,
                                        validation_regex=""
                                    )
                                
                                FacilityContact.objects.create(
                                    facility=facility,
                                    contact_type=contact_type_obj,
                                    contact_value=contact,
                                    is_primary=True,
                                    is_active=True,
                                    created_by=self.user,
                                    updated_by=self.user
                                )
                        
                        # Add infrastructure for capacity
                        infrastructure_type = InfrastructureType.objects.filter(type_name='Accommodation').first()
                        if not infrastructure_type:
                            infrastructure_type = InfrastructureType.objects.create(
                                type_name='Accommodation',
                                description='Accommodation facilities'
                            )
                        
                        # Get or create condition status
                        condition_status = ConditionStatus.objects.filter(status_name='Good').first()
                        if not condition_status:
                            condition_status = ConditionStatus.objects.create(
                                status_name='Good',
                                description='Good condition'
                            )
                        
                        FacilityInfrastructure.objects.create(
                            facility=facility,
                            infrastructure_type=infrastructure_type,
                            condition_status=condition_status,
                            capacity=shelter.get('capacity', 10),
                            current_utilization=0,
                            is_available=True,
                        )
                        
                        # Add GBV categories
                        gbv_categories = ['Physical Violence', 'Sexual Violence', 'Intimate Partner Violence', 'Child Abuse']
                        for gbv_name in gbv_categories:
                            gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                            if gbv_category:
                                FacilityGBVCategory.objects.create(
                                    facility=facility,
                                    gbv_category=gbv_category
                                )
                        
                        created_count += 1
                        
                except Exception as e:
                    logger.error(f"Error creating shelter {shelter.get('name', 'Unknown')}: {e}")
                    continue
            
            logger.info(f"✅ Created {created_count} shelters")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error processing shelters: {e}")
            return 0
    
    def process_fgm_resources(self):
        """Process FGM resources and create documents"""
        logger.info("📚 Processing FGM Resources...")
        
        try:
            file_path = os.path.join(self.data_folder, "FGM resources materials.xlsx")
            if not os.path.exists(file_path):
                logger.warning(f"FGM resources file not found: {file_path}")
                return 0
            
            df = pd.read_excel(file_path)
            created_count = 0
            
            for _, row in df.iterrows():
                try:
                    with transaction.atomic():
                        if pd.notna(row['Document title']):
                            # Get or create document type
                            doc_type_name = row.get('Document type', 'Resource material')
                            doc_type = DocumentType.objects.filter(type_name=doc_type_name).first()
                            if not doc_type:
                                doc_type = DocumentType.objects.create(
                                    type_name=doc_type_name,
                                    description=f"{doc_type_name} documents"
                                )
                            
                            # Create document
                            document = Document.objects.create(
                                title=row['Document title'],
                                document_type=doc_type,
                                description=row.get('Description ', ''),
                                file_url=row.get('File url ', ''),
                                file_name=row.get('File name', ''),
                                external_url=row.get('External url ', ''),
                                is_active=True,
                                uploaded_by=self.user
                            )
                            
                            created_count += 1
                            
                except Exception as e:
                    logger.error(f"Error creating FGM resource {row.get('Document title', 'Unknown')}: {e}")
                    continue
            
            logger.info(f"✅ Created {created_count} FGM resources")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error processing FGM resources: {e}")
            return 0
    
    def process_kmpdc_facilities(self):
        """Process KMPDC licensed facilities from cached JSON data"""
        logger.info("🏥 Processing KMPDC Facilities from cache...")
        
        # Initialize facility code counters if not exists
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {
                'police': 0,
                'gbv_pol': 0,
                'gbv_org': 0,
                'shel': 0,
                'kmpdc': 0
            }
        
        # Check if KMPDC facilities already exist
        existing_kmpdc = Facility.objects.filter(facility_code__startswith='KMPDC_').count()
        if existing_kmpdc > 0:
            logger.info(f"⚠️ Found {existing_kmpdc} existing KMPDC facilities. Skipping to avoid duplicates.")
            return existing_kmpdc
        
        # Try to load from cached JSON first
        cache_file = os.path.join(self.data_folder, 'facilities_cache.json')
        if os.path.exists(cache_file):
            logger.info("📁 Loading facilities from cache...")
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                facilities_data = cache_data.get('facilities', [])
                logger.info(f"📊 Loaded {len(facilities_data)} facilities from cache")
                
                created_count = 0
                for facility_data in facilities_data:
                    # Check if this facility already exists by registration number
                    if facility_data.get('registration_number'):
                        if Facility.objects.filter(registration_number=facility_data['registration_number']).exists():
                            continue
                    
                    # Also check by facility name
                    if Facility.objects.filter(facility_name__iexact=facility_data['name']).exists():
                        continue
                    
                    try:
                        with transaction.atomic():
                            # Get or create ward based on county
                            ward = self._get_or_create_ward_for_county(facility_data.get('county', 'Nairobi'))
                            
                            # Get operational status
                            op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                            if not op_status:
                                op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                            
                            # Create facility with real data only
                            self.facility_code_counters['kmpdc'] += 1
                            facility = Facility.objects.create(
                                facility_name=facility_data['name'],
                                facility_code=facility_data.get('code', f"KMPDC_{self.facility_code_counters['kmpdc']:06d}"),
                                registration_number=facility_data.get('registration_number', f'KMPDC_REG_{self.facility_code_counters["kmpdc"]:06d}'),
                                operational_status=op_status,
                                ward=ward,
                                address_line_1=facility_data.get('address', f"Located in {facility_data.get('county', 'Nairobi')} County"),
                                description=f"KMPDC Licensed Medical Facility",
                                is_active=True,
                            )
                            
                            # Add coordinates if available
                            if facility_data.get('has_coordinates'):
                                self._add_facility_coordinates(facility, facility_data)
                            
                            created_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error creating facility {facility_data.get('name', 'Unknown')}: {e}")
                        continue
                
                logger.info(f"✅ Created {created_count} KMPDC facilities from cache")
                return created_count
                
            except Exception as e:
                logger.error(f"Error loading cache file: {e}")
        
        # Fallback to PDF processing if cache doesn't exist
        logger.info("📄 Cache not found, processing PDF files...")
        return self._process_kmpdc_from_pdf()
    
    def _process_kmpdc_from_pdf(self):
        """Process KMPDC facilities from PDF files (fallback method)"""
        # Find all KMPDC PDF files
        kmpdc_files = []
        for file in os.listdir(self.data_folder):
            if file.endswith('.pdf') and 'KMPDC' in file.upper():
                kmpdc_files.append(os.path.join(self.data_folder, file))
        
        if not kmpdc_files:
            logger.warning("No KMPDC PDF files found")
            return 0
        
        created_count = 0
        
        for file_path in kmpdc_files:
            logger.info(f"Processing KMPDC file: {file_path}")
            
            # Extract facilities from PDF
            facilities = self._extract_kmpdc_facilities_from_pdf(file_path)
            
            if not facilities:
                logger.warning(f"No facilities extracted from {file_path}")
                continue
            
            logger.info(f"Extracted {len(facilities)} facilities from {file_path}")
            
            try:
                for facility_data in facilities:
                    # Check if this facility already exists by registration number
                    if facility_data.get('registration_number'):
                        if Facility.objects.filter(registration_number=facility_data['registration_number']).exists():
                            logger.info(f"Facility with registration number '{facility_data['registration_number']}' already exists. Skipping.")
                            continue
                    
                    # Also check by facility name
                    if Facility.objects.filter(facility_name__iexact=facility_data['facility_name']).exists():
                        logger.info(f"Facility '{facility_data['facility_name']}' already exists. Skipping.")
                        continue
                    
                    try:
                        with transaction.atomic():
                            # Get or create ward based on county
                            ward = self._get_or_create_ward_for_county(facility_data.get('county', 'Nairobi'))
                            
                            # Get operational status
                            op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                            if not op_status:
                                op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                            
                            # Create facility with real data only
                            self.facility_code_counters['kmpdc'] += 1
                            facility = Facility.objects.create(
                                facility_name=facility_data['facility_name'],
                                facility_code=f"KMPDC_{self.facility_code_counters['kmpdc']:06d}",
                                registration_number=facility_data.get('registration_number', f'KMPDC_REG_{self.facility_code_counters["kmpdc"]:06d}'),
                                operational_status=op_status,
                                ward=ward,
                                address_line_1=f"Located in {facility_data.get('county', 'Nairobi')} County",
                                description=f"KMPDC Licensed {facility_data.get('facility_type', 'Medical Facility')} - {facility_data.get('level', 'LEVEL 2')}",
                                is_active=True,
                            )
                            
                            # Add ownership information
                            ownership_type = self._map_ownership_type(facility_data.get('ownership', 'Private'))
                            if ownership_type:
                                owner_type = OwnerType.objects.filter(type_name=ownership_type).first()
                                if not owner_type:
                                    owner_type = OwnerType.objects.create(
                                        type_name=ownership_type,
                                        description=f"{ownership_type} ownership"
                                    )
                                
                                FacilityOwner.objects.create(
                                    facility=facility,
                                    owner_type=owner_type,
                                    owner_name=facility_data.get('owner_name', f"{ownership_type} Owner"),
                                )
                            
                            # Add services based on facility level
                            facility_level = self._extract_facility_level(facility_data.get('level', 'LEVEL 2'))
                            services = self._get_services_for_facility_level(facility_level)
                            
                            for service_name in services:
                                service_category = ServiceCategory.objects.filter(category_name=service_name).first()
                                if not service_category:
                                    service_category = ServiceCategory.objects.create(
                                        category_name=service_name,
                                        description=f"{service_name} services"
                                    )
                                
                                FacilityService.objects.create(
                                    facility=facility,
                                    service_category=service_category,
                                    service_name=service_name,
                                    service_description=f"Provides {service_name} services",
                                    is_free=True,
                                    availability_hours="8:00 AM - 5:00 PM",
                                    availability_days="Monday-Friday",
                                    appointment_required=False
                                )
                            
                            # Add GBV categories based on facility level
                            gbv_categories = self._get_gbv_categories_for_facility_level(facility_level)
                            for gbv_name in gbv_categories:
                                gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                                if gbv_category:
                                    FacilityGBVCategory.objects.create(
                                        facility=facility,
                                        gbv_category=gbv_category,
                                        created_by=self.user
                                    )
                            
                            created_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error creating KMPDC facility {facility_data.get('facility_name', 'Unknown')}: {e}")
                        continue
                
                logger.info(f"✅ Created {created_count} KMPDC facilities from {file_path}")
            
            except Exception as e:
                logger.error(f"❌ Error processing KMPDC file {file_path}: {e}")
                continue
        
        logger.info(f"✅ Total KMPDC facilities created: {created_count}")
        return created_count

    def process_police_stations(self):
        """Process police stations from Excel files"""
        logger.info("🚔 Processing Police Stations...")
        
        # Initialize facility code counters if not exists
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {
                'police': 0,
                'gbv_pol': 0,
                'gbv_org': 0,
                'shel': 0,
                'kmpdc': 0
            }
        
        # Check if police stations already exist
        existing_police = Facility.objects.filter(facility_code__startswith='POLICE_').count()
        if existing_police > 0:
            logger.info(f"⚠️ Found {existing_police} existing police stations. Skipping to avoid duplicates.")
            return existing_police
        
        # Find police station files
        police_files = []
        for file in os.listdir(self.data_folder):
            if file.endswith(('.xlsx', '.xls')) and 'POLICE' in file.upper():
                police_files.append(os.path.join(self.data_folder, file))
        
        if not police_files:
            logger.warning("No police station files found")
            return 0
        
        created_count = 0
        
        for file_path in police_files:
            logger.info(f"Processing police stations from: {file_path}")
            
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Clean column names
                df.columns = df.columns.str.strip()
                
                # Find the main data columns (skip header rows)
                data_start = 0
                for i, row in df.iterrows():
                    if 'POLICE STATION' in str(row.iloc[0]).upper():
                        data_start = i + 1
                        break
                
                if data_start >= len(df):
                    logger.warning(f"No police station data found in {file_path}")
                    continue
                
                # Process each police station
                for i in range(data_start, len(df)):
                    row = df.iloc[i]
                    
                    # Skip empty rows
                    if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == '':
                        continue
                    
                    station_name = str(row.iloc[0]).strip()
                    phone_number = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ''
                    sub_county = str(row.iloc[2]).strip() if not pd.isna(row.iloc[2]) else 'Nairobi'
                    
                    if not station_name or station_name == 'nan':
                        continue
                    
                    # Check if this police station already exists
                    if Facility.objects.filter(facility_name__iexact=station_name).exists():
                        logger.info(f"Police station '{station_name}' already exists. Skipping.")
                        continue
                    
                    try:
                        with transaction.atomic():
                            # Get or create ward based on sub-county
                            ward = self._get_or_create_ward_for_county('Nairobi')
                            
                            # Get operational status
                            op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                            if not op_status:
                                op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                            
                            # Create police station facility
                            self.facility_code_counters['police'] += 1
                            facility = Facility.objects.create(
                                facility_name=station_name,
                                facility_code=f"POLICE_{self.facility_code_counters['police']:06d}",
                                registration_number=f"POLICE_REG_{self.facility_code_counters['police']:06d}",
                                operational_status=op_status,
                                ward=ward,
                                address_line_1=f"Located in {sub_county} Sub-County, Nairobi",
                                description=f"Police Station - {sub_county} Sub-County",
                                is_active=True,
                                created_by=self.user,
                                updated_by=self.user
                            )
                            
                            # Add contact information
                            if phone_number and phone_number != 'nan':
                                phone_type = ContactType.objects.filter(type_name='Phone').first()
                                if not phone_type:
                                    phone_type = ContactType.objects.create(
                                        type_name='Phone',
                                        description='Phone number contact'
                                    )
                                
                                FacilityContact.objects.create(
                                    facility=facility,
                                    contact_type=phone_type,
                                    contact_value=phone_number,
                                    is_primary=True,
                                    is_active=True,
                                    created_by=self.user,
                                    updated_by=self.user
                                )
                            
                            # Add police-specific services
                            police_services = ['Emergency Response', 'Crime Reporting', 'GBV Support', 'Legal Assistance']
                            for service_name in police_services:
                                service_category = ServiceCategory.objects.filter(category_name=service_name).first()
                                if not service_category:
                                    service_category = ServiceCategory.objects.create(
                                        category_name=service_name,
                                        description=f"{service_name} services"
                                    )
                                
                                FacilityService.objects.create(
                                    facility=facility,
                                    service_category=service_category,
                                    service_name=service_name,
                                    service_description=f"Provides {service_name} services",
                                    is_free=True,
                                    availability_hours="24/7",
                                    availability_days="Daily",
                                    appointment_required=False,
                                    is_active=True,
                                )
                            
                            # Add GBV categories
                            gbv_categories = ['Physical Violence', 'Sexual Violence', 'Psychological Violence', 'Economic Violence']
                            for gbv_name in gbv_categories:
                                gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                                if gbv_category:
                                    FacilityGBVCategory.objects.create(
                                        facility=facility,
                                        gbv_category=gbv_category,
                                        created_by=self.user
                                    )
                            
                            created_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error creating police station {station_name}: {e}")
                        continue
                
                logger.info(f"✅ Created {created_count} police stations from {file_path}")
                
            except Exception as e:
                logger.error(f"❌ Error processing police stations file {file_path}: {e}")
                continue
        
        logger.info(f"✅ Total police stations created: {created_count}")
        return created_count

    def process_shelters(self):
        """Process shelters from PDF files"""
        logger.info("🏠 Processing Shelters...")
        
        # Initialize facility code counters if not exists
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {
                'police': 0,
                'gbv_pol': 0,
                'gbv_org': 0,
                'shel': 0,
                'kmpdc': 0
            }
        
        # Check if shelters already exist
        existing_shelters = Facility.objects.filter(facility_code__startswith='SHEL_').count()
        if existing_shelters > 0:
            logger.info(f"⚠️ Found {existing_shelters} existing shelters. Skipping to avoid duplicates.")
            return existing_shelters
        
        # Find shelter files
        shelter_files = []
        for file in os.listdir(self.data_folder):
            if file.endswith('.pdf') and 'SHELTER' in file.upper():
                shelter_files.append(os.path.join(self.data_folder, file))
        
        if not shelter_files:
            logger.warning("No shelter files found")
            return 0
        
        created_count = 0
        
        for file_path in shelter_files:
            logger.info(f"Processing shelters from: {file_path}")
            
            try:
                # Extract text from PDF
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                
                # Parse shelter information
                shelters = self._extract_shelters_from_text(text)
                
                if not shelters:
                    logger.warning(f"No shelters extracted from {file_path}")
                    continue
                
                logger.info(f"Extracted {len(shelters)} shelters from {file_path}")
                
                for shelter_data in shelters:
                    # Check if this shelter already exists
                    if Facility.objects.filter(facility_name__iexact=shelter_data['name']).exists():
                        logger.info(f"Shelter '{shelter_data['name']}' already exists. Skipping.")
                        continue
                    
                    try:
                        with transaction.atomic():
                            # Get or create ward based on county
                            ward = self._get_or_create_ward_for_county(shelter_data.get('county', 'Nairobi'))
                            
                            # Get operational status
                            op_status = OperationalStatus.objects.filter(status_name='Operational').first()
                            if not op_status:
                                op_status = OperationalStatus.objects.create(status_name='Operational', description='Operational')
                            
                            # Create shelter facility
                            self.facility_code_counters['shel'] += 1
                            facility = Facility.objects.create(
                                facility_name=shelter_data['name'],
                                facility_code=f"SHEL_{self.facility_code_counters['shel']:06d}",
                                registration_number=f"SHELTER_REG_{self.facility_code_counters['shel']:06d}",
                                operational_status=op_status,
                                ward=ward,
                                address_line_1=shelter_data.get('address', f"Located in {shelter_data.get('county', 'Nairobi')} County"),
                                description=f"Shelter - {shelter_data.get('type', 'GBV Shelter')}",
                                is_active=True,
                                created_by=self.user,
                                updated_by=self.user
                            )
                            
                            # Add contact information
                            if shelter_data.get('phone'):
                                phone_type = ContactType.objects.filter(type_name='Phone').first()
                                if not phone_type:
                                    phone_type = ContactType.objects.create(
                                        type_name='Phone',
                                        description='Phone number contact'
                                    )
                                
                                FacilityContact.objects.create(
                                    facility=facility,
                                    contact_type=phone_type,
                                    contact_value=shelter_data['phone'],
                                    is_primary=True,
                                    is_active=True,
                                    created_by=self.user,
                                    updated_by=self.user
                                )
                            
                            # Add shelter-specific services
                            shelter_services = ['Emergency Shelter', 'Counseling', 'Legal Support', 'Medical Care', 'Rehabilitation']
                            for service_name in shelter_services:
                                service_category = ServiceCategory.objects.filter(category_name=service_name).first()
                                if not service_category:
                                    service_category = ServiceCategory.objects.create(
                                        category_name=service_name,
                                        description=f"{service_name} services"
                                    )
                                
                                FacilityService.objects.create(
                                    facility=facility,
                                    service_category=service_category,
                                    service_name=service_name,
                                    service_description=f"Provides {service_name} services",
                                    is_free=True,
                                    availability_hours="24/7",
                                    availability_days="Daily",
                                    appointment_required=False,
                                    is_active=True,
                                )
                            
                            # Add GBV categories
                            gbv_categories = ['Physical Violence', 'Sexual Violence', 'Psychological Violence', 'Economic Violence', 'Domestic Violence']
                            for gbv_name in gbv_categories:
                                gbv_category = GBVCategory.objects.filter(category_name=gbv_name).first()
                                if gbv_category:
                                    FacilityGBVCategory.objects.create(
                                        facility=facility,
                                        gbv_category=gbv_category,
                                        created_by=self.user
                                    )
                            
                            created_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error creating shelter {shelter_data.get('name', 'Unknown')}: {e}")
                        continue
                
                logger.info(f"✅ Created {created_count} shelters from {file_path}")
                
            except Exception as e:
                logger.error(f"❌ Error processing shelter file {file_path}: {e}")
                continue
        
        logger.info(f"✅ Total shelters created: {created_count}")
        return created_count
    
    def _add_facility_coordinates(self, facility, facility_data):
        """Add coordinates to facility if available and within Kenya"""
        try:
            # Check if coordinates are provided
            if not facility_data.get('latitude') or not facility_data.get('longitude'):
                return
            
            lat = float(facility_data['latitude'])
            lng = float(facility_data['longitude'])
            
            # Validate coordinates are within Kenya bounds
            if not self._is_within_kenya(lat, lng):
                logger.warning(f"Coordinates ({lat}, {lng}) for {facility.facility_name} are outside Kenya bounds")
                return
            
            # Create coordinate record
            FacilityCoordinate.objects.create(
                facility=facility,
                latitude=lat,
                longitude=lng,
                collection_date=timezone.now().date(),
                data_source='KMPDC',
                collection_method='GPS',
            )
            
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid coordinates for {facility.facility_name}: {e}")
        except Exception as e:
            logger.error(f"Error adding coordinates for {facility.facility_name}: {e}")
    
    def _is_within_kenya(self, latitude, longitude):
        """Check if coordinates are within Kenya bounds"""
        # Kenya approximate bounds
        kenya_bounds = {
            'min_lat': -4.7,
            'max_lat': 5.5,
            'min_lng': 33.9,
            'max_lng': 41.9
        }
        
        return (kenya_bounds['min_lat'] <= latitude <= kenya_bounds['max_lat'] and
                kenya_bounds['min_lng'] <= longitude <= kenya_bounds['max_lng'])
    
    def enrich_facilities_from_cache(self):
        """Enrich existing facilities with data from cache"""
        logger.info("🔄 Enriching facilities from cache...")
        
        cache_file = os.path.join(self.data_folder, 'facilities_cache.json')
        if not os.path.exists(cache_file):
            logger.warning(f"Cache file not found at {cache_file}")
            return 0
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            facilities_data = cache_data.get('facilities', [])
            logger.info(f"📊 Loaded {len(facilities_data)} facilities from cache for enrichment")
            
            enriched_count = 0
            
            for facility_data in facilities_data:
                try:
                    # Try to find existing facility by registration number first
                    facility = None
                    if facility_data.get('registration_number'):
                        facility = Facility.objects.filter(
                            registration_number=facility_data['registration_number']
                        ).first()
                    
                    # If not found by registration, try by name
                    if not facility:
                        facility = Facility.objects.filter(
                            facility_name__iexact=facility_data['name']
                        ).first()
                    
                    if facility:
                        # Update ward if we have better location data
                        if facility_data.get('county') and facility_data.get('ward'):
                            try:
                                ward = self._get_or_create_ward_for_county(
                                    facility_data['county'], 
                                    facility_data['ward']
                                )
                                if ward != facility.ward:
                                    facility.ward = ward
                                    facility.save()
                                    logger.info(f"Updated ward for {facility.facility_name}")
                            except Exception as e:
                                logger.error(f"Error updating ward for {facility.facility_name}: {e}")
                        
                        # Add coordinates if not present and available
                        if not facility.facilitycoordinate_set.exists() and facility_data.get('has_coordinates'):
                            self._add_facility_coordinates(facility, facility_data)
                            enriched_count += 1
                    
                except Exception as e:
                    logger.error(f"Error enriching facility {facility_data.get('name', 'Unknown')}: {e}")
                    continue
            
            logger.info(f"✅ Enriched {enriched_count} facilities")
            return enriched_count
            
        except Exception as e:
            logger.error(f"Error loading cache file for enrichment: {e}")
            return 0

    def _extract_shelters_from_text(self, text):
        """Extract shelter information from PDF text"""
        shelters = []
        
        # Simple text parsing for shelter information
        lines = text.split('\n')
        current_shelter = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_shelter:
                    shelters.append(current_shelter)
                    current_shelter = {}
                continue
            
            # Look for shelter names (usually in caps or title case)
            if any(keyword in line.upper() for keyword in ['SHELTER', 'SAFE HOUSE', 'REFUGE', 'CENTER']):
                if current_shelter:
                    shelters.append(current_shelter)
                current_shelter = {
                    'name': line,
                    'type': 'GBV Shelter',
                    'county': 'Nairobi'  # Default county
                }
            elif 'PHONE' in line.upper() or 'TEL' in line.upper():
                # Extract phone number
                phone_match = re.search(r'(\+?254|0)?[0-9]{9,10}', line)
                if phone_match:
                    current_shelter['phone'] = phone_match.group()
            elif 'ADDRESS' in line.upper() or 'LOCATION' in line.upper():
                current_shelter['address'] = line
        
        # Add the last shelter
        if current_shelter:
            shelters.append(current_shelter)
        
        return shelters
    
    def process_documents(self):
        """Process additional documents"""
        logger.info("📄 Processing Additional Documents...")
        
        try:
            # Create some sample documents
            documents = [
                {
                    'title': 'GBV Response Guidelines',
                    'document_type': 'Guideline',
                    'description': 'Comprehensive guidelines for GBV response',
                    'file_url': 'https://gvrc.co.ke/guidelines',
                    'file_name': 'gbv_guidelines.pdf'
                },
                {
                    'title': 'Legal Framework for GBV',
                    'document_type': 'Legal Document',
                    'description': 'Legal framework and procedures for GBV cases',
                    'file_url': 'https://gvrc.co.ke/legal',
                    'file_name': 'legal_framework.pdf'
                },
                {
                    'title': 'Crisis Intervention Protocol',
                    'document_type': 'Protocol',
                    'description': 'Step-by-step crisis intervention protocol',
                    'file_url': 'https://gvrc.co.ke/protocols',
                    'file_name': 'crisis_protocol.pdf'
                }
            ]
            
            created_count = 0
            
            for doc_data in documents:
                try:
                    with transaction.atomic():
                        # Get or create document type
                        doc_type = DocumentType.objects.filter(type_name=doc_data['document_type']).first()
                        if not doc_type:
                            doc_type = DocumentType.objects.create(
                                type_name=doc_data['document_type'],
                                description=f"{doc_data['document_type']} documents"
                            )
                        
                        document = Document.objects.create(
                            title=doc_data['title'],
                            document_type=doc_type,
                            description=doc_data['description'],
                            file_url=doc_data['file_url'],
                            file_name=doc_data['file_name'],
                            is_active=True,
                            uploaded_by=self.user
                        )
                        
                        created_count += 1
                        
                except Exception as e:
                    logger.error(f"Error creating document {doc_data['title']}: {e}")
                    continue
            
            logger.info(f"✅ Created {created_count} additional documents")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error processing documents: {e}")
            return 0
    
    # Helper methods for comprehensive data extraction
    
    def _extract_gbv_organizations_from_docx(self, doc) -> List[Dict[str, Any]]:
        """Extract GBV organizations from DOCX document"""
        organizations = []
        current_org = {}
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            # Look for organization names (usually numbered)
            if re.match(r'^\d+\.', text) and len(text) > 10:
                if current_org:
                    organizations.append(current_org)
                current_org = {
                    'name': text,
                    'type': 'GBV Organization',
                    'county': 'Nairobi',  # Default
                    'contacts': [],
                    'services': [],
                    'description': ''
                }
            elif current_org and text:
                current_org['description'] += f" {text}"
                
                # Extract contact information
                if re.search(r'\b\d{3,4}\s*\d{3,4}\s*\d{3,4}\b', text) or '@' in text or 'http' in text:
                    current_org['contacts'].append(text)
                
                # Extract services
                if 'Services:' in text or 'services:' in text:
                    current_org['services'].append(text)
                
                # Extract county information
                if 'COUNTY' in text.upper():
                    county_match = re.search(r'(\w+)\s+COUNTY', text.upper())
                    if county_match:
                        current_org['county'] = county_match.group(1).title()
        
        # Add the last organization
        if current_org:
            organizations.append(current_org)
        
        return organizations
    
    def _extract_shelters_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract shelters from PDF using pdfplumber"""
        shelters = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Parse shelter data from text
                        lines = text.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line and re.match(r'^\d+\.', line):
                                shelter_data = self._parse_shelter_line(line)
                                if shelter_data:
                                    shelters.append(shelter_data)
        except Exception as e:
            logger.error(f"Error extracting shelters from PDF: {e}")
        
        return shelters
    
    def _parse_shelter_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single shelter line from PDF text"""
        try:
            # Format: NO. NAME OF SHELTER   COUNTY   SHELTER OPERATOR   CONTACT (PHONE/ EMAIL)
            parts = line.split()
            if len(parts) < 4:
                return None
            
            shelter_data = {
                'name': ' '.join(parts[1:-3]) if len(parts) > 4 else parts[1],
                'county': parts[-3] if len(parts) >= 3 else 'Nairobi',
                'operator': parts[-2] if len(parts) >= 2 else 'Unknown',
                'contacts': [parts[-1]] if len(parts) >= 1 else [],
                'capacity': 10  # Default capacity
            }
            
            return shelter_data
        except Exception as e:
            logger.error(f"Error parsing shelter line: {e}")
            return None
    
    def _extract_kmpdc_facilities_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract KMPDC facilities from PDF using tabula-py for better table extraction."""
        facilities = []
        
        try:
            import tabula
            import pandas as pd
            
            logger.info(f"Extracting tables from PDF: {file_path}")
            
            # Extract all tables from the PDF
            # Use 'lattice' mode for better table detection
            tables = tabula.read_pdf(
                file_path, 
                pages='all', 
                multiple_tables=True,
                pandas_options={'header': None}  # No header - we'll map columns by position
            )
            
            logger.info(f"Found {len(tables)} tables in PDF")
            
            for table_idx, table in enumerate(tables):
                if table.empty:
                    continue
                    
                logger.info(f"Processing table {table_idx + 1} with {len(table)} rows")
                
                # Map columns by position based on the actual PDF structure
                # The structure is: [No, Reg_No, Facility_Name, Facility_Type, Facility_Ownership, Level, County, Status]
                if table.shape[1] >= 8:  # Ensure we have enough columns
                    # Assign column names based on position
                    table.columns = ['no', 'registration_number', 'facility_name', 'facility_type', 'ownership', 'level', 'county', 'status']
                else:
                    logger.warning(f"Table {table_idx + 1} has insufficient columns: {table.shape[1]}")
                    continue
                
                # Debug: Print first few rows to understand the data structure
                if not table.empty:
                    logger.info(f"Table {table_idx + 1} first row: {table.iloc[0].to_dict()}")
                    logger.info(f"Table {table_idx + 1} columns after mapping: {list(table.columns)}")
                
                # Process each row
                for row_idx, row in table.iterrows():
                    try:
                        # Skip rows with missing essential data
                        if pd.isna(row.get('facility_name')) or pd.isna(row.get('registration_number')):
                            continue
                            
                        # Skip rows that look like headers (contain text like "No", "Reg_No", etc.)
                        facility_name = str(row.get('facility_name', '')).strip()
                        registration_number = str(row.get('registration_number', '')).strip()
                        
                        if (facility_name.upper() in ['NO', 'FACILITY_NAME', 'FACILITY NAME', 'S/NO', 'S/No'] or
                            registration_number.upper() in ['REG_NO', 'REG NO', 'REGISTRATION']):
                            continue
                            
                        facility_data = {
                            'registration_number': registration_number,
                            'facility_name': facility_name,
                            'address': '',  # Address not available in this PDF structure
                            'facility_type': str(row.get('facility_type', '')).strip(),
                            'ownership': str(row.get('ownership', '')).strip(),
                            'level': str(row.get('level', '')).strip(),
                            'county': str(row.get('county', '')).strip(),
                            'status': str(row.get('status', '')).strip()
                        }
                        
                        # Only process if we have essential data and it's not a header row
                        if (facility_data['facility_name'] and 
                            facility_data['registration_number'] and 
                            not facility_data['facility_name'].upper().startswith('NO') and
                            not facility_data['facility_name'].upper().startswith('FACILITY') and
                            not facility_data['facility_name'].upper().startswith('S/') and
                            not facility_data['registration_number'].upper().startswith('REG')):
                            facilities.append(facility_data)
                            
                    except Exception as row_error:
                        logger.warning(f"Error processing row: {str(row_error)}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error extracting facilities from PDF {file_path}: {str(e)}")
            # Fallback to pdfplumber if tabula fails
            try:
                import pdfplumber
                logger.info("Falling back to pdfplumber for PDF extraction")
                
                with pdfplumber.open(file_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        logger.info(f"Processing page {page_num + 1} of {len(pdf.pages)}")
                        
                        # Extract tables from the page
                        tables = page.extract_tables()
                        
                        for table in tables:
                            if not table or len(table) < 2:
                                continue
                                
                            # Skip header row
                            for row in table[1:]:
                                if len(row) < 8:  # Ensure we have enough columns
                                    continue
                                    
                                # Extract facility data
                                facility_data = {
                                    'registration_number': str(row[1]).strip() if row[1] else '',
                                    'facility_name': str(row[2]).strip() if row[2] else '',
                                    'address': str(row[3]).strip() if row[3] else '',
                                    'facility_type': str(row[4]).strip() if row[4] else '',
                                    'ownership': str(row[5]).strip() if row[5] else '',
                                    'level': str(row[6]).strip() if row[6] else '',
                                    'county': str(row[7]).strip() if row[7] else '',
                                    'status': str(row[8]).strip() if len(row) > 8 and row[8] else 'LICENSED'
                                }
                                
                                # Only process if we have essential data
                                if facility_data['facility_name'] and facility_data['registration_number']:
                                    facilities.append(facility_data)
                                    
            except Exception as fallback_error:
                logger.error(f"Fallback PDF extraction also failed: {str(fallback_error)}")
            
        logger.info(f"Extracted {len(facilities)} facilities from PDF")
        return facilities
    
    def _parse_kmpdc_facility_row(self, row: List[str]) -> Optional[Dict[str, Any]]:
        """Parse a KMPDC facility row from table"""
        try:
            if len(row) < 6:
                return None
            
            facility_data = {
                'registration': row[0] if row[0] else '',
                'name': row[1] if row[1] else '',
                'address': row[2] if row[2] else '',
                'type': row[3] if row[3] else 'Medical Facility',
                'ownership': row[4] if row[4] else 'Private',
                'level': row[5] if row[5] else 'LEVEL 2',
                'county': row[6] if len(row) > 6 and row[6] else 'Nairobi'
            }
            
            return facility_data
        except Exception as e:
            logger.error(f"Error parsing KMPDC facility row: {e}")
            return None
    
    def _parse_kmpdc_facility_text(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse KMPDC facility from text line"""
        try:
            # This is a simplified parser - would need more sophisticated parsing for real data
            parts = line.split()
            if len(parts) < 3:
                return None
            
            facility_data = {
                'registration': parts[0] if parts[0] else '',
                'name': ' '.join(parts[1:-2]) if len(parts) > 3 else parts[1],
                'address': 'Unknown',
                'type': 'Medical Facility',
                'ownership': 'Private',
                'level': 'LEVEL 2',
                'county': 'Nairobi'
            }
            
            return facility_data
        except Exception as e:
            logger.error(f"Error parsing KMPDC facility text: {e}")
            return None
    
    def _get_or_create_county(self, county_name: str) -> County:
        """Get or create a county"""
        try:
            county, _ = County.objects.get_or_create(
                county_name=county_name,
                defaults={'county_code': f'C{County.objects.count() + 1:03d}'}
            )
            return county
        except Exception as e:
            logger.error(f"Error creating county {county_name}: {e}")
            return County.objects.first() or County.objects.create(
                county_name="Default County",
                county_code="C001"
            )
    
    def _get_or_create_constituency(self, constituency_name: str, county: County) -> Constituency:
        """Get or create a constituency"""
        try:
            constituency, _ = Constituency.objects.get_or_create(
                constituency_name=constituency_name,
                county=county,
                defaults={'constituency_code': f'CONST_{Constituency.objects.count() + 1:03d}'}
            )
            return constituency
        except Exception as e:
            logger.error(f"Error creating constituency {constituency_name}: {e}")
            return Constituency.objects.first() or Constituency.objects.create(
                constituency_name="Default Constituency",
                county=county,
                constituency_code="CONST_001"
            )
    
    def _get_or_create_ward(self, ward_name: str, constituency: Constituency) -> Ward:
        """Get or create a ward"""
        try:
            ward, _ = Ward.objects.get_or_create(
                ward_name=ward_name,
                constituency=constituency,
                defaults={'ward_code': f'WARD_{Ward.objects.count() + 1:03d}'}
            )
            return ward
        except Exception as e:
            logger.error(f"Error creating ward {ward_name}: {e}")
            return Ward.objects.first() or Ward.objects.create(
                ward_name="Default Ward",
                constituency=constituency,
                ward_code="WARD_001"
            )
    
    def _get_or_create_ward_for_county(self, county_name: str, subcounty_name: str = None, 
                                     facility_coordinates: tuple = None) -> Ward:
        """Get or create ward for county with intelligent matching"""
        try:
            # First try to find existing ward by subcounty name if provided
            if subcounty_name:
                ward = Ward.objects.filter(
                    ward_name__icontains=subcounty_name,
                    constituency__county__county_name__icontains=county_name
                ).first()
                if ward:
                    return ward
            
            # Try to find ward by coordinates if provided
            if facility_coordinates:
                lat, lng = facility_coordinates
                # Find the closest ward in the same county
                wards_in_county = Ward.objects.filter(
                    constituency__county__county_name__icontains=county_name
                ).select_related('constituency__county')
                
                if wards_in_county.exists():
                    # For now, return the first ward in the county
                    # In a more sophisticated system, we'd calculate distances
                    return wards_in_county.first()
            
            # Try to find any ward in the county
            ward = Ward.objects.filter(
                constituency__county__county_name__icontains=county_name
            ).first()
            
            if ward:
                return ward
            
            # Create county if needed
            county = County.objects.filter(county_name__icontains=county_name).first()
            if not county:
                county = County.objects.create(
                    county_name=county_name,
                    county_code=f"CNT_{County.objects.count() + 1:03d}"
                )
            
            # Create constituency
            constituency_name = subcounty_name or county_name
            constituency = Constituency.objects.filter(constituency_name__icontains=constituency_name).first()
            if not constituency:
                # Create constituency code with length limit
                constituency_code = f"C{County.objects.count() + 1:05d}"
                constituency = Constituency.objects.create(
                    constituency_name=f"{county_name} Central",
                    county=county,
                    constituency_code=constituency_code
                )
            
            # Create ward
            ward_name = subcounty_name or f"{county_name} Central Ward"
            # Create ward code with strict length limit - use simple numeric approach
            ward_code = f"W{Ward.objects.count() + 1:06d}"
            
            ward = Ward.objects.create(
                ward_name=ward_name,
                constituency=constituency,
                ward_code=ward_code
            )
            
            return ward
        except Exception as e:
            logger.error(f"Error creating ward for county {county_name}: {e}")
            # Return first available ward as fallback
            return Ward.objects.first() or Ward.objects.create(
                ward_name="Default Ward",
                constituency=Constituency.objects.first() or Constituency.objects.create(
                    constituency_name="Default Constituency",
                    county=County.objects.first() or County.objects.create(
                        county_name="Default County",
                        county_code="DEF"
                    )
                )
            )
    
    def _determine_contact_type(self, contact: str) -> Optional[str]:
        """Determine contact type from contact string"""
        if re.search(r'\b\d{3,4}\s*\d{3,4}\s*\d{3,4}\b', contact):
            return 'Phone'
        elif '@' in contact:
            return 'Email'
        elif 'http' in contact.lower():
            return 'Website'
        else:
            return 'Other'
    
    def _get_services_for_organization_type(self, org_type: str) -> List[str]:
        """Get services based on organization type"""
        service_mapping = {
            'Legal Aid Center': ['Legal Representation', 'Legal Advice', 'Court Support'],
            'Crisis Center': ['Crisis Intervention', 'Emergency Response', 'Counseling'],
            'Child Protection Center': ['Child Counseling', 'Family Support', 'Emergency Response'],
            'General': ['Counseling', 'Legal Aid', 'Medical Support', 'Shelter']
        }
        return service_mapping.get(org_type, service_mapping['General'])
    
    def _get_gbv_categories_for_organization_type(self, org_type: str) -> List[str]:
        """Get GBV categories based on organization type"""
        category_mapping = {
            'Legal Aid Center': ['Physical Violence', 'Sexual Violence', 'Intimate Partner Violence'],
            'Crisis Center': ['Physical Violence', 'Sexual Violence', 'Intimate Partner Violence', 'Child Abuse'],
            'Child Protection Center': ['Child Abuse', 'Sexual Violence', 'Physical Violence'],
            'General': ['Physical Violence', 'Sexual Violence', 'Child Abuse', 'Intimate Partner Violence']
        }
        return category_mapping.get(org_type, category_mapping['General'])
    
    def _extract_facility_level(self, level_str: str) -> str:
        """Extract facility level from string"""
        level_match = re.search(r'LEVEL\s+(\d+[A-Z]?)', level_str.upper())
        if level_match:
            return f"LEVEL {level_match.group(1)}"
        return "LEVEL 2"
    
    def _get_services_for_facility_level(self, facility_level: str) -> List[str]:
        """Get services based on facility level - Level 5+ for psychological services"""
        level_num = int(re.search(r'LEVEL\s+(\d+)', facility_level).group(1)) if re.search(r'LEVEL\s+(\d+)', facility_level) else 2
        
        base_services = ['Medical Treatment', 'Emergency Response']
        
        if level_num >= 3:
            base_services.extend(['Counseling', 'Rehabilitation'])
        
        if level_num >= 5:
            base_services.extend(['Psychological Services', 'Mental Health Support'])
        
        return base_services
    
    def _get_gbv_categories_for_facility_level(self, facility_level: str) -> List[str]:
        """Get GBV categories based on facility level"""
        level_num = int(re.search(r'LEVEL\s+(\d+)', facility_level).group(1)) if re.search(r'LEVEL\s+(\d+)', facility_level) else 2
        
        base_categories = ['Physical Violence', 'Sexual Violence']
        
        if level_num >= 3:
            base_categories.extend(['Intimate Partner Violence'])
        
        if level_num >= 4:
            base_categories.extend(['Child Abuse'])
        
        return base_categories
    
    def _map_ownership_type(self, ownership: str) -> str:
        """Map ownership string to standard type"""
        ownership_mapping = {
            'Private': 'Private',
            'Public': 'Government',
            'County Government': 'Government',
            'Faith Based': 'Faith-Based',
            'NGO': 'NGO',
            'FBO': 'Faith-Based'
        }
        return ownership_mapping.get(ownership, 'Private')
    
    def process_healthcare_facilities(self):
        """Process healthcare facilities from GeoJSON file"""
        logger.info("🏥 Processing Healthcare Facilities from GeoJSON...")
        
        # Initialize facility code counters if not exists
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {
                'police': 0,
                'gbv_pol': 0,
                'gbv_org': 0,
                'shel': 0,
                'kmpdc': 0,
                'healthcare': 0
            }
        
        healthcare_file = os.path.join(self.data_folder, 'healthcare_facilities.json')
        if not os.path.exists(healthcare_file):
            logger.warning("Healthcare facilities file not found")
            return 0
        
        try:
            with open(healthcare_file, 'r') as f:
                geojson_data = json.load(f)
            
            features = geojson_data.get('features', [])
            logger.info(f"Found {len(features)} healthcare facilities in GeoJSON")
            
            created_count = 0
            enriched_count = 0
            
            for feature in features:
                try:
                    properties = feature.get('properties', {})
                    geometry = feature.get('geometry', {})
                    
                    facility_name = properties.get('Facility_N', '').strip()
                    if not facility_name:
                        continue
                    
                    # Check for duplicates using our prevention system
                    if self._is_duplicate_facility(facility_name):
                        continue
                    
                    # Check if facility already exists in database
                    existing_facility = Facility.objects.filter(
                        facility_name__iexact=facility_name
                    ).first()
                    
                    if existing_facility:
                        # Enrich existing facility with coordinates
                        if geometry.get('type') == 'Point' and geometry.get('coordinates'):
                            coords = geometry['coordinates']
                            if len(coords) >= 2:
                                lat, lng = float(coords[1]), float(coords[0])
                                if self._is_within_kenya(lat, lng):
                                    self._add_facility_coordinates(existing_facility, {
                                        'latitude': lat,
                                        'longitude': lng
                                    })
                                    enriched_count += 1
                        continue
                    
                    # Create new facility
                    county_name = properties.get('County', 'Nairobi')
                    sub_county = properties.get('Sub_County', '')
                    constituency = properties.get('Constituen', '')
                    location = properties.get('Location', '')
                    facility_type = properties.get('Type', 'Health Facility')
                    owner = properties.get('Owner', 'Ministry of Health')
                    
                    # Get or create county, constituency, and ward
                    county = self._get_or_create_county(county_name)
                    constituency_obj = self._get_or_create_constituency(constituency, county)
                    ward = self._get_or_create_ward(f"{location} Ward", constituency_obj)
                    
                    # Get operational status
                    op_status, _ = OperationalStatus.objects.get_or_create(
                        status_name='Operational',
                        defaults={'description': 'Facility is operational'}
                    )
                    
                    # Create facility
                    facility = Facility.objects.create(
                        facility_name=facility_name,
                        facility_code=f"HEALTH_{self.facility_code_counters['healthcare']:06d}",
                        registration_number=f"HEALTH_REG_{self.facility_code_counters['healthcare']:06d}",
                        operational_status=op_status,
                        ward=ward,
                        address_line_1=f"Located in {location}, {sub_county}, {county_name}",
                        description=f"{facility_type} - {owner}",
                        is_active=True,
                        created_by=self.user,
                        updated_by=self.user
                    )
                    
                    # Add to cache to prevent duplicates
                    self._add_facility_to_cache(
                        facility_name=facility_name,
                        facility_code=f"HEALTH_{self.facility_code_counters['healthcare']:06d}",
                        registration_number=f"HEALTH_REG_{self.facility_code_counters['healthcare']:06d}"
                    )
                    
                    # Add coordinates if available
                    if geometry.get('type') == 'Point' and geometry.get('coordinates'):
                        coords = geometry['coordinates']
                        if len(coords) >= 2:
                            lat, lng = float(coords[1]), float(coords[0])
                            if self._is_within_kenya(lat, lng):
                                self._add_facility_coordinates(facility, {
                                    'latitude': lat,
                                    'longitude': lng
                                })
                    
                    # Add services based on facility type
                    self._add_healthcare_services(facility, facility_type)
                    
                    self.facility_code_counters['healthcare'] += 1
                    created_count += 1
                    
                    if created_count % 1000 == 0:
                        logger.info(f"Processed {created_count} healthcare facilities...")
                        
                except Exception as e:
                    logger.warning(f"Error processing healthcare facility {facility_name}: {e}")
                    continue
            
            logger.info(f"✅ Created {created_count} new healthcare facilities")
            logger.info(f"✅ Enriched {enriched_count} existing facilities with coordinates")
            return created_count + enriched_count
            
        except Exception as e:
            logger.error(f"Error processing healthcare facilities: {e}")
            return 0
    
    def _add_healthcare_services(self, facility, facility_type):
        """Add appropriate services based on healthcare facility type"""
        try:
            # Map facility types to services
            service_mapping = {
                'Hospital': ['Emergency Care', 'Inpatient Care', 'Outpatient Care', 'Surgery', 'Maternity', 'Pediatrics'],
                'Health Centre': ['Outpatient Care', 'Maternity', 'Immunization', 'Family Planning'],
                'Dispensary': ['Outpatient Care', 'Immunization', 'Basic Health Services'],
                'Clinic': ['Outpatient Care', 'Basic Health Services'],
                'Medical Centre': ['Outpatient Care', 'Diagnostic Services', 'Specialist Care']
            }
            
            services = service_mapping.get(facility_type, ['Basic Health Services'])
            
            for service_name in services:
                service_category, _ = ServiceCategory.objects.get_or_create(
                    category_name=service_name,
                    defaults={'description': f'{service_name} services'}
                )
                
                FacilityService.objects.create(
                    facility=facility,
                    service_category=service_category
                )
                
        except Exception as e:
            logger.warning(f"Error adding services to facility {facility.facility_name}: {e}")
    
    def _get_cached_data(self, cache_key: str, data_folder: str) -> Optional[Dict]:
        """Get cached data if available and not expired"""
        cache_file = os.path.join(data_folder, f"{cache_key}_cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                # Check if cache is not older than 24 hours
                cache_time = datetime.fromisoformat(cache_data.get('timestamp', '1970-01-01'))
                if (datetime.now() - cache_time).total_seconds() < 86400:  # 24 hours
                    return cache_data.get('data')
            except Exception as e:
                logger.warning(f"Error reading cache file {cache_file}: {e}")
        return None
    
    def _save_cached_data(self, cache_key: str, data: Any, data_folder: str):
        """Save data to cache"""
        cache_file = os.path.join(data_folder, f"{cache_key}_cache.json")
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            logger.warning(f"Error saving cache file {cache_file}: {e}")
    
    def process_gbv_station_pilot(self):
        """Process GBV Station Pilot data from Excel with caching"""
        logger.info("🚨 Processing GBV Station Pilot data...")
        
        # Initialize facility code counters if not exists
        if not hasattr(self, 'facility_code_counters'):
            self.facility_code_counters = {
                'police': 0,
                'gbv_pol': 0,
                'gbv_org': 0,
                'shel': 0,
                'kmpdc': 0,
                'healthcare': 0,
                'gbv_pilot': 0
            }
        
        gbv_file = os.path.join(self.data_folder, 'GBV SDTATION PILOT.xlsx')
        if not os.path.exists(gbv_file):
            logger.warning("GBV Station Pilot file not found")
            return 0
        
        # Check cache first
        cached_data = self._get_cached_data('gbv_station_pilot', self.data_folder)
        if cached_data:
            logger.info("Using cached GBV Station Pilot data")
            return self._process_cached_gbv_stations(cached_data)
        
        try:
            # Load Excel file with pandas for better data handling
            df = pd.read_excel(gbv_file, header=None)
            
            # Extract data from the complex Excel structure
            gbv_stations = []
            current_region = None
            current_county = None
            current_subcounty = None
            
            for index, row in df.iterrows():
                if row.isna().all():
                    continue
                
                # Convert row to list for easier processing
                row_data = [str(cell) if pd.notna(cell) else '' for cell in row]
                
                # Check for region headers (e.g., "1. COAST REGION")
                if any('REGION' in str(cell).upper() for cell in row if pd.notna(cell)):
                    region_cell = next((str(cell) for cell in row if pd.notna(cell) and 'REGION' in str(cell).upper()), '')
                    if region_cell:
                        current_region = region_cell.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('6. ', '').replace('7. ', '').replace('8. ', '').strip()
                        logger.info(f"Processing region: {current_region}")
                    continue
                
                # Check for county headers (e.g., "KWALE", "KILIFI")
                county_candidates = [cell for cell in row if pd.notna(cell) and str(cell).strip()]
                for cell in county_candidates:
                    cell_str = str(cell).strip()
                    # Common county names in Kenya
                    if cell_str.upper() in ['KWALE', 'KILIFI', 'MOMBASA', 'TAITA TAVETA', 'LAMU', 'TANA RIVER', 
                                          'MURANGA', 'KIAMBU', 'NYERI', 'KIRINYAGA', 'NYANDARUA', 'NYERI',
                                          'NAIROBI', 'MACHAKOS', 'KITUI', 'MAKUENI', 'MAKUENI', 'KITUI',
                                          'KAKAMEGA', 'VIHIGA', 'BUNGOMA', 'BUSIA', 'SIAYA', 'KISUMU',
                                          'HOMA BAY', 'MIGORI', 'KISII', 'NYAMIRA', 'NAKURU', 'NAROK',
                                          'KAJIADO', 'KERICHO', 'BOMET', 'LAIKIPIA', 'NAKURU', 'NANDI',
                                          'UASIN GISHU', 'ELGEYO MARAKWET', 'WEST POKOT', 'SAMBURU',
                                          'TURKANA', 'BARINGO', 'SAMBURU', 'ISIOLO', 'GARISSA', 'WAJIR',
                                          'MANDERA', 'MERU', 'THARAKA NITHI', 'EMBU', 'KITUI', 'MAKUENI',
                                          'MARSABIT', 'ISIOLO', 'GARISSA', 'WAJIR', 'MANDERA']:
                        current_county = cell_str.upper()
                        logger.info(f"Processing county: {current_county}")
                        break
                
                # Check for subcounty headers (e.g., "KWALE", "KINANGO", "MSAMBWENI")
                if current_county and len(row_data) > 1:
                    for i, cell in enumerate(row_data):
                        if cell and cell.strip() and not any(x in cell.upper() for x in ['REGION', 'COUNTY', 'STATION', 'POST', 'POLICE']):
                            # This might be a subcounty
                            potential_subcounty = cell.strip()
                            if len(potential_subcounty) > 2:  # Avoid single letters
                                current_subcounty = potential_subcounty
                                break
                
                # Extract police stations and posts from the data
                for i, cell in enumerate(row_data):
                    if not cell or cell.strip() == '' or cell == 'nan':
                        continue
                    
                    cell_str = str(cell).strip()
                    
                    # Skip headers and empty cells
                    if any(x in cell_str.upper() for x in ['REGION', 'COUNTY', 'STATION', 'POST', 'POLICE', 'MAPPING']):
                        continue
                    
                    # Extract station/post name and contact
                    station_info = cell_str
                    contact = None
                    
                    # Look for phone numbers in the same cell or adjacent cells
                    import re
                    phone_match = re.search(r'(\d{10,13})', cell_str)
                    if phone_match:
                        contact = phone_match.group(1)
                        station_info = cell_str.replace(contact, '').strip()
                    
                    # Clean up station name
                    station_name = station_info.replace('\n', ' ').strip()
                    if not station_name or len(station_name) < 2:
                        continue
                    
                    # Determine if it's a station or post based on context
                    facility_type = 'Police Station'
                    if 'POST' in str(row_data).upper() or 'post' in station_name.lower():
                        facility_type = 'Police Post'
                    
                    # Create facility data
                    facility_data = {
                        'facility_name': station_name,
                        'facility_type': facility_type,
                        'county': current_county or 'Unknown',
                        'subcounty': current_subcounty or 'Unknown',
                        'region': current_region or 'Unknown',
                        'contact': contact,
                        'source': 'GBV Station Pilot'
                    }
                    
                    gbv_stations.append(facility_data)
            
            logger.info(f"Extracted {len(gbv_stations)} GBV stations/posts from Excel")
            
            # Save to cache
            cache_data = {
                'total_facilities': len(gbv_stations),
                'facilities': gbv_stations,
                'last_updated': timezone.now().isoformat()
            }
            self._save_cached_data('gbv_station_pilot', cache_data, self.data_folder)
            
            # Process the extracted data
            return self._process_cached_gbv_stations(cache_data)
            
        except Exception as e:
            logger.error(f"Error processing GBV Station Pilot file: {e}")
            return 0
    
    def _process_cached_gbv_stations(self, gbv_data: Dict) -> int:
        """Process cached GBV station data"""
        created_count = 0
        
        # Handle both old format (list) and new format (dict with facilities)
        if isinstance(gbv_data, list):
            facilities_data = gbv_data
        else:
            facilities_data = gbv_data.get('facilities', [])
        
        for station_data in facilities_data:
            try:
                with transaction.atomic():
                    # Check if station already exists
                    facility_name = station_data.get('facility_name', station_data.get('name', ''))
                    if not facility_name:
                        continue
                        
                    existing_station = Facility.objects.filter(
                        facility_name__iexact=facility_name
                    ).first()
                    
                    if existing_station:
                        continue
                    
                    # Get county and ward information
                    county_name = station_data.get('county', 'Unknown')
                    subcounty_name = station_data.get('subcounty', 'Unknown')
                    
                    # Get or create ward
                    ward = self._get_or_create_ward_for_county(county_name, subcounty_name)
                    
                    # Get operational status
                    op_status, _ = OperationalStatus.objects.get_or_create(
                        status_name='Operational',
                        defaults={'description': 'Facility is operational'}
                    )
                    
                    # Get facility type
                    facility_type_name = station_data.get('facility_type', 'Police Station')
                    
                    # Increment counter before creation
                    self.facility_code_counters['gbv_pilot'] += 1
                    
                    # Create facility
                    facility = Facility.objects.create(
                        facility_name=facility_name,
                        facility_code=f"GBV_PILOT_{self.facility_code_counters['gbv_pilot']:06d}",
                        registration_number=f"GBV_PILOT_REG_{self.facility_code_counters['gbv_pilot']:06d}",
                        operational_status=op_status,
                        ward=ward,
                        address_line_1=f"Located in {county_name} County, {subcounty_name}",
                        description=f"GBV Station Pilot - {facility_type_name} in {county_name} County",
                        is_active=True,
                        created_by=self.user,
                        updated_by=self.user
                    )
                    
                    # Add contact information
                    contact = station_data.get('contact', station_data.get('phone'))
                    if contact:
                        phone_type, _ = ContactType.objects.get_or_create(
                            type_name='Phone',
                            defaults={'validation_regex': r'^\+?[\d\s\-\(\)]+$'}
                        )
                        FacilityContact.objects.create(
                            facility=facility,
                            contact_type=phone_type,
                            contact_value=contact,
                            is_primary=True,
                            is_active=True,
                            created_by=self.user,
                            updated_by=self.user
                        )
                    
                    # Add GBV-specific services
                    gbv_services = ['GBV Support', 'Emergency Response', 'Counseling', 'Legal Assistance', 'Medical Care']
                    for service_name in gbv_services:
                        service_category, _ = ServiceCategory.objects.get_or_create(
                            category_name=service_name,
                            defaults={'description': f'{service_name} services'}
                        )
                        FacilityService.objects.create(
                            facility=facility,
                            service_category=service_category
                        )
                    
                    # Add GBV categories
                    gbv_categories = ['Physical Violence', 'Sexual Violence', 'Psychological Violence', 'Economic Violence']
                    for gbv_name in gbv_categories:
                        gbv_category, _ = GBVCategory.objects.get_or_create(
                            category_name=gbv_name,
                            defaults={'description': f'{gbv_name} support services'}
                        )
                        FacilityGBVCategory.objects.create(
                            facility=facility,
                            gbv_category=gbv_category,
                            created_by=self.user
                        )
                    
                    created_count += 1
                    
            except Exception as e:
                logger.warning(f"Error creating GBV station {station_data.get('name', 'Unknown')}: {e}")
                continue
        
        logger.info(f"✅ Created {created_count} GBV Station Pilot facilities")
        return created_count
    
    def process_fgm_resources(self):
        """Process FGM Resources data from Excel with caching"""
        logger.info("📚 Processing FGM Resources data...")
        
        fgm_file = os.path.join(self.data_folder, 'FGM resources materials.xlsx')
        if not os.path.exists(fgm_file):
            logger.warning("FGM Resources file not found")
            return 0
        
        # Check cache first
        cached_data = self._get_cached_data('fgm_resources', self.data_folder)
        if cached_data:
            logger.info("Using cached FGM Resources data")
            return self._process_cached_fgm_resources(cached_data)
        
        try:
            # Load Excel file
            df = pd.read_excel(fgm_file)
            
            # Process the data
            fgm_resources = []
            for _, row in df.iterrows():
                if pd.notna(row['Document title']):
                    fgm_resources.append({
                        'title': str(row['Document title']),
                        'type': str(row['Document type']) if pd.notna(row['Document type']) else 'Document',
                        'description': str(row['Description ']) if pd.notna(row['Description ']) else '',
                        'file_url': str(row['File url ']) if pd.notna(row['File url ']) else '',
                        'file_name': str(row['File name']) if pd.notna(row['File name']) else '',
                        'gbv_category': str(row['Gbv category ']) if pd.notna(row['Gbv category ']) else 'FGM',
                        'image_url': str(row['image url']) if pd.notna(row['image url']) else '',
                        'external_url': str(row['External url ']) if pd.notna(row['External url ']) else ''
                    })
            
            # Cache the processed data
            self._save_cached_data('fgm_resources', fgm_resources, self.data_folder)
            
            return self._process_cached_fgm_resources(fgm_resources)
            
        except Exception as e:
            logger.error(f"Error processing FGM Resources file: {e}")
            return 0
    
    def _process_cached_fgm_resources(self, fgm_resources: List[Dict]) -> int:
        """Process cached FGM resources data"""
        created_count = 0
        
        for resource_data in fgm_resources:
            try:
                with transaction.atomic():
                    # Create or get document type
                    doc_type, _ = DocumentType.objects.get_or_create(
                        type_name=resource_data['type'],
                        defaults={'description': f'{resource_data["type"]} document type'}
                    )
                    
                    # Create document
                    document = Document.objects.create(
                        title=resource_data['title'],
                        document_type=doc_type,
                        description=resource_data['description'],
                        file_url=resource_data['file_url'],
                        file_name=resource_data['file_name'],
                        external_url=resource_data['external_url'],
                        is_active=True,
                        uploaded_by=self.user
                    )
                    
                    created_count += 1
                    
            except Exception as e:
                logger.warning(f"Error creating FGM resource {resource_data.get('title', 'Unknown')}: {e}")
                continue
        
        logger.info(f"✅ Created {created_count} FGM Resources")
        return created_count


# Global data populator instance
data_populator = DataPopulator()