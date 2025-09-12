"""
Standalone Data Architecture Integration
Works alongside main GVRC system without modifications
"""

import logging
import json
from typing import Dict, Any, List, Optional
from django.conf import settings
from django.db import connections
from .enhanced_etl_pipeline import DataArchitectureManager
from .raw_data_lake import RawDataLake
from .ai_geolocation import AIGeolocationEnhancer, KenyaGeographicEnhancement
from .data_swarm_prevention import DataSwarmPreventionSystem

logger = logging.getLogger(__name__)


class StandaloneDataArchitecture:
    """Standalone data architecture that integrates with existing GVRC system"""
    
    def __init__(self):
        self.architecture_manager = DataArchitectureManager()
        self.raw_data_lake = RawDataLake()
        self.geolocator = AIGeolocationEnhancer()
        self.geographic_enhancer = KenyaGeographicEnhancement()
        self.swarm_prevention = DataSwarmPreventionSystem()
        
        # Integration settings
        self.integration_config = {
            'main_db_alias': 'default',
            'data_arch_db_alias': 'data_architecture',
            'sync_enabled': True,
            'batch_size': 100
        }
    
    def sync_from_main_system(self, table_name: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Sync data from main GVRC system to data architecture"""
        try:
            logger.info(f"Starting sync from main system table: {table_name}")
            
            # Get data from main system
            main_data = self._extract_from_main_system(table_name, filters)
            
            if not main_data:
                return {
                    'success': True,
                    'message': 'No data to sync',
                    'records_processed': 0
                }
            
            # Process through data architecture
            result = self.architecture_manager.ingest_data(
                source_name=f'main_system_{table_name}',
                data=main_data,
                source_type='external'
            )
            
            logger.info(f"Sync completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Sync from main system failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'records_processed': 0
            }
    
    def enhance_facility_data(self, facility_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance facility data with AI capabilities"""
        try:
            # Apply data swarm prevention
            prevention_result = self.swarm_prevention.prevent_data_swarm([facility_data], 'enhancement')
            
            if not prevention_result['processed_records']:
                return facility_data
            
            enhanced_record = prevention_result['processed_records'][0]
            
            # Apply geographic enhancement
            enhanced_record = self.geographic_enhancer.enhance_facility_location(enhanced_record)
            
            # Apply AI geolocation if coordinates missing
            if not enhanced_record.get('location', {}).get('latitude'):
                location = enhanced_record.get('location', {})
                address = enhanced_record.get('address', '')
                
                coordinates = self.geolocator.enhance_coordinates(
                    address,
                    location.get('county', ''),
                    location.get('constituency', ''),
                    location.get('ward', '')
                )
                
                if coordinates:
                    if 'location' not in enhanced_record:
                        enhanced_record['location'] = {}
                    
                    enhanced_record['location'].update({
                        'latitude': coordinates['lat'],
                        'longitude': coordinates['lng'],
                        'accuracy_level': coordinates.get('accuracy', 'unknown'),
                        'geocoding_service': coordinates.get('source', 'unknown')
                    })
            
            return enhanced_record
            
        except Exception as e:
            logger.error(f"Facility data enhancement failed: {e}")
            return facility_data
    
    def batch_enhance_facilities(self, facility_ids: List[int]) -> Dict[str, Any]:
        """Batch enhance multiple facilities"""
        try:
            logger.info(f"Starting batch enhancement for {len(facility_ids)} facilities")
            
            # Extract facilities from main system
            facilities = self._extract_facilities_by_ids(facility_ids)
            
            if not facilities:
                return {
                    'success': True,
                    'message': 'No facilities found',
                    'records_processed': 0
                }
            
            # Enhance each facility
            enhanced_facilities = []
            for facility in facilities:
                enhanced_facility = self.enhance_facility_data(facility)
                enhanced_facilities.append(enhanced_facility)
            
            # Store enhanced data in data architecture
            result = self.architecture_manager.ingest_data(
                source_name='batch_enhancement',
                data=enhanced_facilities,
                source_type='batch_processing'
            )
            
            logger.info(f"Batch enhancement completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Batch enhancement failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'records_processed': 0
            }
    
    def get_enhanced_facility_data(self, facility_id: int) -> Optional[Dict[str, Any]]:
        """Get enhanced facility data from data architecture"""
        try:
            # This would query the data architecture database
            # For now, return None as placeholder
            return None
            
        except Exception as e:
            logger.error(f"Failed to get enhanced facility data: {e}")
            return None
    
    def create_quality_report(self, table_name: str = None) -> Dict[str, Any]:
        """Create data quality report for main system data"""
        try:
            if table_name:
                # Sync specific table first
                sync_result = self.sync_from_main_system(table_name)
                if not sync_result['success']:
                    return sync_result
            
            # Get quality report from data architecture
            quality_report = self.architecture_manager.get_data_quality_report()
            
            # Add main system specific metrics
            quality_report['main_system_integration'] = {
                'sync_status': 'enabled' if self.integration_config['sync_enabled'] else 'disabled',
                'last_sync': 'N/A',  # Would track actual sync time
                'tables_monitored': ['facilities', 'geography', 'users']
            }
            
            return quality_report
            
        except Exception as e:
            logger.error(f"Failed to create quality report: {e}")
            return {'error': str(e)}
    
    def _extract_from_main_system(self, table_name: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Extract data from main GVRC system database"""
        try:
            # Use Django's database connection to query main system
            with connections[self.integration_config['main_db_alias']].cursor() as cursor:
                # Build query based on table name
                if table_name == 'facilities':
                    query = self._build_facilities_query(filters)
                elif table_name == 'geography':
                    query = self._build_geography_query(filters)
                elif table_name == 'users':
                    query = self._build_users_query(filters)
                else:
                    raise ValueError(f"Unsupported table: {table_name}")
                
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                data = []
                for row in rows:
                    data.append(dict(zip(columns, row)))
                
                return data
                
        except Exception as e:
            logger.error(f"Failed to extract from main system: {e}")
            return []
    
    def _extract_facilities_by_ids(self, facility_ids: List[int]) -> List[Dict[str, Any]]:
        """Extract specific facilities by IDs"""
        try:
            with connections[self.integration_config['main_db_alias']].cursor() as cursor:
                # Build comprehensive facilities query
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
                    fc.contact_type_id,
                    fc.contact_value,
                    ct.type_name,
                    fco.latitude,
                    fco.longitude
                FROM facilities f
                LEFT JOIN wards w ON f.ward_id = w.id
                LEFT JOIN constituencies c ON w.constituency_id = c.id
                LEFT JOIN counties co ON c.county_id = co.id
                LEFT JOIN operational_statuses os ON f.operational_status_id = os.id
                LEFT JOIN facility_contacts fc ON f.id = fc.facility_id
                LEFT JOIN contact_types ct ON fc.contact_type_id = ct.id
                LEFT JOIN facility_coordinates fco ON f.id = fco.facility_id
                WHERE f.id = ANY(%s)
                ORDER BY f.id
                """
                
                cursor.execute(query, [facility_ids])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
                # Group by facility and structure data
                facilities = {}
                for row in rows:
                    facility_id = row[0]
                    if facility_id not in facilities:
                        facilities[facility_id] = {
                            'id': row[0],
                            'facility_name': row[1],
                            'registration_number': row[2],
                            'operational_status': row[8] if row[8] else 'Unknown',
                            'location': {
                                'ward': row[8] if row[8] else '',
                                'constituency': row[9] if row[9] else '',
                                'county': row[10] if row[10] else '',
                                'latitude': float(row[15]) if row[15] else None,
                                'longitude': float(row[16]) if row[16] else None
                            },
                            'contacts': [],
                            'active_status': row[5],
                            'created_at': row[6],
                            'updated_at': row[7]
                        }
                    
                    # Add contact information
                    if row[12] and row[13]:  # contact_type_id and contact_value
                        facilities[facility_id]['contacts'].append({
                            'type': row[14] if row[14] else 'Unknown',
                            'value': row[13]
                        })
                
                return list(facilities.values())
                
        except Exception as e:
            logger.error(f"Failed to extract facilities by IDs: {e}")
            return []
    
    def _build_facilities_query(self, filters: Dict[str, Any] = None) -> str:
        """Build query for facilities table"""
        base_query = """
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
            os.status_name
        FROM facilities f
        LEFT JOIN wards w ON f.ward_id = w.id
        LEFT JOIN constituencies c ON w.constituency_id = c.id
        LEFT JOIN counties co ON c.county_id = co.id
        LEFT JOIN operational_statuses os ON f.operational_status_id = os.id
        """
        
        if filters:
            where_conditions = []
            if 'active_status' in filters:
                where_conditions.append(f"f.active_status = {filters['active_status']}")
            if 'county' in filters:
                where_conditions.append(f"co.county_name = '{filters['county']}'")
            
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)
        
        base_query += " ORDER BY f.id"
        return base_query
    
    def _build_geography_query(self, filters: Dict[str, Any] = None) -> str:
        """Build query for geography data"""
        return """
        SELECT 
            co.id as county_id,
            co.county_name,
            c.id as constituency_id,
            c.constituency_name,
            w.id as ward_id,
            w.ward_name
        FROM counties co
        LEFT JOIN constituencies c ON co.id = c.county_id
        LEFT JOIN wards w ON c.id = w.constituency_id
        ORDER BY co.id, c.id, w.id
        """
    
    def _build_users_query(self, filters: Dict[str, Any] = None) -> str:
        """Build query for users data"""
        return """
        SELECT 
            u.id,
            u.full_name,
            u.email,
            u.phone_number,
            u.is_active,
            u.facility_id,
            f.facility_name,
            u.created_at,
            u.updated_at
        FROM users u
        LEFT JOIN facilities f ON u.facility_id = f.id
        ORDER BY u.id
        """
    
    def export_enhanced_data(self, table_name: str, format: str = 'json') -> Dict[str, Any]:
        """Export enhanced data in specified format"""
        try:
            # Get enhanced data from data architecture
            # This would query the data architecture database
            # For now, return placeholder
            
            return {
                'success': True,
                'message': f'Enhanced data exported in {format} format',
                'table_name': table_name,
                'format': format,
                'download_url': f'/data-architecture/export/{table_name}.{format}'
            }
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


class DataArchitectureAPI:
    """API wrapper for standalone data architecture"""
    
    def __init__(self):
        self.standalone = StandaloneDataArchitecture()
    
    def enhance_facility(self, facility_id: int) -> Dict[str, Any]:
        """API endpoint to enhance a single facility"""
        try:
            # Get facility from main system
            facilities = self.standalone._extract_facilities_by_ids([facility_id])
            
            if not facilities:
                return {
                    'success': False,
                    'error': 'Facility not found'
                }
            
            # Enhance facility
            enhanced_facility = self.standalone.enhance_facility_data(facilities[0])
            
            return {
                'success': True,
                'facility_id': facility_id,
                'enhanced_data': enhanced_facility
            }
            
        except Exception as e:
            logger.error(f"Facility enhancement API failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def batch_enhance_facilities(self, facility_ids: List[int]) -> Dict[str, Any]:
        """API endpoint for batch facility enhancement"""
        return self.standalone.batch_enhance_facilities(facility_ids)
    
    def get_quality_report(self) -> Dict[str, Any]:
        """API endpoint for quality report"""
        return self.standalone.create_quality_report()
    
    def sync_main_system(self, table_name: str) -> Dict[str, Any]:
        """API endpoint to sync from main system"""
        return self.standalone.sync_from_main_system(table_name)

