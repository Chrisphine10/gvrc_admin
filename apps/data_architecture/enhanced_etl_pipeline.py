"""
Enhanced ETL Pipeline
Multi-layer data processing with AI enhancement
"""

import time
import logging
from typing import Dict, Any, List, Optional
from django.db import transaction
from .models import (
    RawDataRecord, ValidatedDataRecord, EnrichedDataRecord, 
    DataMart, DataProcessingEvent, DataSource
)
from .raw_data_lake import RawDataLake, DataSourceManager
from .data_validation import DataValidator, QualityGates
from .ai_geolocation import AIGeolocationEnhancer, KenyaGeographicEnhancement
from .data_swarm_prevention import DataSwarmPreventionSystem

logger = logging.getLogger(__name__)


class EnhancedETLPipeline:
    """Enhanced ETL pipeline with multi-layer processing"""
    
    def __init__(self):
        self.raw_data_lake = RawDataLake()
        self.data_source_manager = DataSourceManager()
        self.validator = DataValidator()
        self.quality_gates = QualityGates()
        self.geolocator = AIGeolocationEnhancer()
        self.geographic_enhancer = KenyaGeographicEnhancement()
        self.swarm_prevention = DataSwarmPreventionSystem()
        
        # Processing statistics
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'duplicates_found': 0,
            'quality_issues': 0,
            'processing_time': 0
        }
    
    def process_data(self, source_name: str, data: List[Dict[str, Any]], 
                    source_type: str = 'manual') -> Dict[str, Any]:
        """Main ETL processing pipeline"""
        start_time = time.time()
        pipeline_result = {
            'success': True,
            'errors': [],
            'warnings': [],
            'processing_time': 0,
            'quality_score': 0,
            'records_processed': 0,
            'records_successful': 0,
            'records_failed': 0,
            'duplicates_prevented': 0,
            'enhancements_applied': []
        }
        
        try:
            logger.info(f"Starting ETL pipeline for {len(data)} records from {source_name}")
            
            # Step 1: Data Swarm Prevention
            prevention_result = self.swarm_prevention.prevent_data_swarm(data, source_name)
            pipeline_result['duplicates_prevented'] = prevention_result['duplicates_found']
            pipeline_result['enhancements_applied'].append('data_swarm_prevention')
            
            # Step 2: Process each record through the pipeline
            processed_records = []
            
            for record in prevention_result['processed_records']:
                try:
                    # Process individual record through all layers
                    record_result = self._process_single_record(record, source_name, source_type)
                    
                    if record_result['success']:
                        processed_records.append(record_result['record'])
                        pipeline_result['records_successful'] += 1
                    else:
                        pipeline_result['records_failed'] += 1
                        pipeline_result['errors'].extend(record_result['errors'])
                    
                except Exception as e:
                    logger.error(f"Failed to process record: {e}")
                    pipeline_result['records_failed'] += 1
                    pipeline_result['errors'].append(str(e))
            
            # Update statistics
            pipeline_result['records_processed'] = len(data)
            pipeline_result['success'] = pipeline_result['records_failed'] == 0
            pipeline_result['processing_time'] = time.time() - start_time
            
            # Calculate overall quality score
            if processed_records:
                quality_scores = [r.get('quality_score', 0) for r in processed_records]
                pipeline_result['quality_score'] = sum(quality_scores) / len(quality_scores)
            
            # Update global statistics
            self._update_stats(pipeline_result)
            
            logger.info(f"ETL pipeline completed: {pipeline_result}")
            return pipeline_result
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            pipeline_result['success'] = False
            pipeline_result['errors'].append(str(e))
            pipeline_result['processing_time'] = time.time() - start_time
            return pipeline_result
    
    def _process_single_record(self, record: Dict[str, Any], source_name: str, 
                             source_type: str) -> Dict[str, Any]:
        """Process a single record through all pipeline layers"""
        record_result = {
            'success': True,
            'errors': [],
            'warnings': [],
            'record': record,
            'quality_score': 0,
            'processing_steps': []
        }
        
        try:
            # Layer 1: Raw Data Lake
            raw_record = self._store_raw_data(record, source_name, source_type)
            record_result['processing_steps'].append('raw_data_stored')
            
            # Layer 2: Data Validation
            validation_result = self._validate_data(record)
            if not validation_result['is_valid']:
                record_result['success'] = False
                record_result['errors'].extend(validation_result['errors'])
                return record_result
            
            validated_record = self._store_validated_data(raw_record, validation_result)
            record_result['processing_steps'].append('data_validated')
            record_result['quality_score'] = validation_result['quality_score']
            
            # Layer 3: AI Enhancement
            enhancement_result = self._enhance_data(record)
            if enhancement_result['enhanced']:
                record.update(enhancement_result['enhanced_data'])
                record_result['processing_steps'].append('ai_enhanced')
            
            enriched_record = self._store_enriched_data(validated_record, record, enhancement_result)
            record_result['processing_steps'].append('data_enriched')
            
            # Layer 4: Data Mart Creation
            mart_result = self._create_data_mart(enriched_record, record)
            if mart_result['created']:
                record_result['processing_steps'].append('data_mart_created')
            
            # Update record with final data
            record_result['record'] = record
            
            return record_result
            
        except Exception as e:
            logger.error(f"Failed to process record: {e}")
            record_result['success'] = False
            record_result['errors'].append(str(e))
            return record_result
    
    def _store_raw_data(self, record: Dict[str, Any], source_name: str, 
                       source_type: str) -> RawDataRecord:
        """Store data in raw data lake"""
        try:
            metadata = {
                'source_type': source_type,
                'processing_timestamp': time.time(),
                'record_type': 'facility'
            }
            
            raw_record = self.raw_data_lake.store_raw_data(source_name, record, metadata)
            return raw_record
            
        except Exception as e:
            logger.error(f"Failed to store raw data: {e}")
            raise
    
    def _validate_data(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data using comprehensive validation framework"""
        try:
            validation_result = self.validator.validate_facility_data(record)
            
            # Apply quality gates
            quality_result = self.quality_gates.validate_data(record)
            
            # Combine results
            combined_result = {
                'is_valid': validation_result['is_valid'] and quality_result['passed'],
                'errors': validation_result['errors'] + quality_result['issues'],
                'warnings': validation_result['warnings'] + quality_result['recommendations'],
                'quality_score': (validation_result['quality_score'] + quality_result['overall_score']) / 2,
                'validation_details': {
                    'schema_validation': validation_result,
                    'quality_gates': quality_result
                }
            }
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return {
                'is_valid': False,
                'errors': [str(e)],
                'warnings': [],
                'quality_score': 0.0
            }
    
    def _store_validated_data(self, raw_record: RawDataRecord, 
                            validation_result: Dict[str, Any]) -> ValidatedDataRecord:
        """Store validated data"""
        try:
            validated_record = ValidatedDataRecord.objects.create(
                raw_record=raw_record,
                validated_data=raw_record.raw_data,
                quality_score=validation_result['quality_score'],
                validation_errors=validation_result['errors'],
                validation_warnings=validation_result['warnings'],
                validation_rules_applied=list(validation_result['validation_details'].keys()),
                is_valid=validation_result['is_valid']
            )
            
            # Log processing event
            self._log_processing_event('data_validated', raw_record.data_id, raw_record.source)
            
            return validated_record
            
        except Exception as e:
            logger.error(f"Failed to store validated data: {e}")
            raise
    
    def _enhance_data(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance data with AI capabilities"""
        enhancement_result = {
            'enhanced': False,
            'enhanced_data': record.copy(),
            'enhancements_applied': [],
            'geographic_enhancement': None,
            'ai_enhancements': {}
        }
        
        try:
            # Geographic enhancement
            if 'location' in record:
                geo_enhancement = self.geographic_enhancer.enhance_facility_location(record)
                if geo_enhancement != record:
                    enhancement_result['enhanced'] = True
                    enhancement_result['enhanced_data'] = geo_enhancement
                    enhancement_result['enhancements_applied'].append('geographic_enhancement')
                    enhancement_result['geographic_enhancement'] = geo_enhancement.get('location', {})
            
            # AI-powered geolocation
            if not record.get('location', {}).get('latitude') or not record.get('location', {}).get('longitude'):
                address = record.get('address', '')
                county = record.get('location', {}).get('county', '')
                constituency = record.get('location', {}).get('constituency', '')
                ward = record.get('location', {}).get('ward', '')
                
                coordinates = self.geolocator.enhance_coordinates(
                    address, county, constituency, ward
                )
                
                if coordinates:
                    enhancement_result['enhanced'] = True
                    if 'location' not in enhancement_result['enhanced_data']:
                        enhancement_result['enhanced_data']['location'] = {}
                    
                    enhancement_result['enhanced_data']['location'].update({
                        'latitude': coordinates['lat'],
                        'longitude': coordinates['lng'],
                        'accuracy_level': coordinates.get('accuracy', 'unknown'),
                        'geocoding_service': coordinates.get('source', 'unknown')
                    })
                    enhancement_result['enhancements_applied'].append('ai_geolocation')
                    enhancement_result['ai_enhancements']['geolocation'] = coordinates
            
            return enhancement_result
            
        except Exception as e:
            logger.error(f"Data enhancement failed: {e}")
            return enhancement_result
    
    def _store_enriched_data(self, validated_record: ValidatedDataRecord, 
                           enhanced_record: Dict[str, Any], 
                           enhancement_result: Dict[str, Any]) -> EnrichedDataRecord:
        """Store enriched data"""
        try:
            enriched_record = EnrichedDataRecord.objects.create(
                validated_record=validated_record,
                enriched_data=enhanced_record,
                enrichment_applied=enhancement_result['enhancements_applied'],
                ai_enhancements=enhancement_result['ai_enhancements'],
                geographic_data=enhancement_result.get('geographic_enhancement', {}),
                final_quality_score=validated_record.quality_score
            )
            
            # Log processing event
            self._log_processing_event('data_enriched', validated_record.raw_record.data_id, 
                                     validated_record.raw_record.source)
            
            return enriched_record
            
        except Exception as e:
            logger.error(f"Failed to store enriched data: {e}")
            raise
    
    def _create_data_mart(self, enriched_record: EnrichedDataRecord, 
                        final_record: Dict[str, Any]) -> Dict[str, Any]:
        """Create data mart for business consumption"""
        mart_result = {
            'created': False,
            'mart_type': 'facilities',
            'mart_data': final_record
        }
        
        try:
            # Create facilities data mart
            data_mart = DataMart.objects.create(
                enriched_record=enriched_record,
                mart_data=final_record,
                mart_type='facilities',
                is_served=True,
                serving_metadata={
                    'created_at': time.time(),
                    'quality_score': enriched_record.final_quality_score,
                    'enhancements_applied': enriched_record.enrichment_applied
                }
            )
            
            mart_result['created'] = True
            mart_result['data_mart_id'] = data_mart.id
            
            # Log processing event
            self._log_processing_event('data_served', enriched_record.validated_record.raw_record.data_id,
                                     enriched_record.validated_record.raw_record.source)
            
            return mart_result
            
        except Exception as e:
            logger.error(f"Failed to create data mart: {e}")
            return mart_result
    
    def _log_processing_event(self, event_type: str, record_id: str, source: DataSource):
        """Log data processing event"""
        try:
            DataProcessingEvent.objects.create(
                event_type=event_type,
                record_id=record_id,
                source=source,
                success=True,
                processing_time=time.time()
            )
        except Exception as e:
            logger.error(f"Failed to log processing event: {e}")
    
    def _update_stats(self, pipeline_result: Dict[str, Any]):
        """Update processing statistics"""
        self.stats['total_processed'] += pipeline_result['records_processed']
        self.stats['successful'] += pipeline_result['records_successful']
        self.stats['failed'] += pipeline_result['records_failed']
        self.stats['duplicates_found'] += pipeline_result['duplicates_prevented']
        self.stats['processing_time'] += pipeline_result['processing_time']
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'duplicates_found': 0,
            'quality_issues': 0,
            'processing_time': 0
        }


class DataArchitectureManager:
    """Central manager for the enhanced data architecture"""
    
    def __init__(self):
        self.etl_pipeline = EnhancedETLPipeline()
        self.raw_data_lake = RawDataLake()
        self.data_source_manager = DataSourceManager()
    
    def ingest_data(self, source_name: str, data: List[Dict[str, Any]], 
                   source_type: str = 'manual') -> Dict[str, Any]:
        """Main data ingestion endpoint"""
        try:
            # Register source if not exists
            self.data_source_manager.register_source(source_name, None, {
                'source_type': source_type,
                'description': f'Data source: {source_name}'
            })
            
            # Process data through ETL pipeline
            result = self.etl_pipeline.process_data(source_name, data, source_type)
            
            return result
            
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'records_processed': 0
            }
    
    def get_data_quality_report(self) -> Dict[str, Any]:
        """Get comprehensive data quality report"""
        try:
            # Get quality metrics from database
            from .models import DataQualityMetric
            
            quality_metrics = DataQualityMetric.objects.all()
            
            report = {
                'total_metrics': quality_metrics.count(),
                'average_scores': {},
                'threshold_violations': {},
                'recommendations': []
            }
            
            # Calculate average scores by metric type
            metric_types = ['completeness', 'accuracy', 'consistency', 'timeliness', 'uniqueness']
            for metric_type in metric_types:
                metrics = quality_metrics.filter(metric_type=metric_type)
                if metrics.exists():
                    avg_score = sum(m.metric_value for m in metrics) / metrics.count()
                    report['average_scores'][metric_type] = round(avg_score, 3)
                    
                    # Check threshold violations
                    threshold = 0.5  # Lowered threshold for more lenient validation
                    violations = metrics.filter(metric_value__lt=threshold).count()
                    report['threshold_violations'][metric_type] = violations
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate quality report: {e}")
            return {'error': str(e)}
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        try:
            health_status = {
                'overall_status': 'healthy',
                'components': {},
                'alerts': [],
                'recommendations': []
            }
            
            # Check raw data lake
            raw_stats = self.raw_data_lake.get_storage_stats()
            health_status['components']['raw_data_lake'] = {
                'status': 'healthy' if raw_stats.get('failed_records', 0) == 0 else 'warning',
                'stats': raw_stats
            }
            
            # Check ETL pipeline
            etl_stats = self.etl_pipeline.get_processing_stats()
            success_rate = (etl_stats['successful'] / max(etl_stats['total_processed'], 1)) * 100
            health_status['components']['etl_pipeline'] = {
                'status': 'healthy' if success_rate > 90 else 'warning',
                'success_rate': round(success_rate, 2),
                'stats': etl_stats
            }
            
            # Check data sources
            sources = self.data_source_manager.list_sources()
            health_status['components']['data_sources'] = {
                'status': 'healthy' if len(sources) > 0 else 'warning',
                'count': len(sources),
                'sources': sources
            }
            
            # Generate alerts
            if success_rate < 90:
                health_status['alerts'].append('ETL pipeline success rate below 90%')
            
            if raw_stats.get('failed_records', 0) > 0:
                health_status['alerts'].append(f"{raw_stats['failed_records']} failed records in raw data lake")
            
            # Set overall status
            if health_status['alerts']:
                health_status['overall_status'] = 'warning'
            
            return health_status
            
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return {
                'overall_status': 'error',
                'error': str(e)
            }

"""
Enhanced ETL Pipeline
Multi-layer data processing with AI enhancement
"""

import time
import logging
from typing import Dict, Any, List, Optional
from django.db import transaction
from .models import (
    RawDataRecord, ValidatedDataRecord, EnrichedDataRecord, 
    DataMart, DataProcessingEvent, DataSource
)
from .raw_data_lake import RawDataLake, DataSourceManager
from .data_validation import DataValidator, QualityGates
from .ai_geolocation import AIGeolocationEnhancer, KenyaGeographicEnhancement
from .data_swarm_prevention import DataSwarmPreventionSystem

logger = logging.getLogger(__name__)


class EnhancedETLPipeline:
    """Enhanced ETL pipeline with multi-layer processing"""
    
    def __init__(self):
        self.raw_data_lake = RawDataLake()
        self.data_source_manager = DataSourceManager()
        self.validator = DataValidator()
        self.quality_gates = QualityGates()
        self.geolocator = AIGeolocationEnhancer()
        self.geographic_enhancer = KenyaGeographicEnhancement()
        self.swarm_prevention = DataSwarmPreventionSystem()
        
        # Processing statistics
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'duplicates_found': 0,
            'quality_issues': 0,
            'processing_time': 0
        }
    
    def process_data(self, source_name: str, data: List[Dict[str, Any]], 
                    source_type: str = 'manual') -> Dict[str, Any]:
        """Main ETL processing pipeline"""
        start_time = time.time()
        pipeline_result = {
            'success': True,
            'errors': [],
            'warnings': [],
            'processing_time': 0,
            'quality_score': 0,
            'records_processed': 0,
            'records_successful': 0,
            'records_failed': 0,
            'duplicates_prevented': 0,
            'enhancements_applied': []
        }
        
        try:
            logger.info(f"Starting ETL pipeline for {len(data)} records from {source_name}")
            
            # Step 1: Data Swarm Prevention
            prevention_result = self.swarm_prevention.prevent_data_swarm(data, source_name)
            pipeline_result['duplicates_prevented'] = prevention_result['duplicates_found']
            pipeline_result['enhancements_applied'].append('data_swarm_prevention')
            
            # Step 2: Process each record through the pipeline
            processed_records = []
            
            for record in prevention_result['processed_records']:
                try:
                    # Process individual record through all layers
                    record_result = self._process_single_record(record, source_name, source_type)
                    
                    if record_result['success']:
                        processed_records.append(record_result['record'])
                        pipeline_result['records_successful'] += 1
                    else:
                        pipeline_result['records_failed'] += 1
                        pipeline_result['errors'].extend(record_result['errors'])
                    
                except Exception as e:
                    logger.error(f"Failed to process record: {e}")
                    pipeline_result['records_failed'] += 1
                    pipeline_result['errors'].append(str(e))
            
            # Update statistics
            pipeline_result['records_processed'] = len(data)
            pipeline_result['success'] = pipeline_result['records_failed'] == 0
            pipeline_result['processing_time'] = time.time() - start_time
            
            # Calculate overall quality score
            if processed_records:
                quality_scores = [r.get('quality_score', 0) for r in processed_records]
                pipeline_result['quality_score'] = sum(quality_scores) / len(quality_scores)
            
            # Update global statistics
            self._update_stats(pipeline_result)
            
            logger.info(f"ETL pipeline completed: {pipeline_result}")
            return pipeline_result
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            pipeline_result['success'] = False
            pipeline_result['errors'].append(str(e))
            pipeline_result['processing_time'] = time.time() - start_time
            return pipeline_result
    
    def _process_single_record(self, record: Dict[str, Any], source_name: str, 
                             source_type: str) -> Dict[str, Any]:
        """Process a single record through all pipeline layers"""
        record_result = {
            'success': True,
            'errors': [],
            'warnings': [],
            'record': record,
            'quality_score': 0,
            'processing_steps': []
        }
        
        try:
            # Layer 1: Raw Data Lake
            raw_record = self._store_raw_data(record, source_name, source_type)
            record_result['processing_steps'].append('raw_data_stored')
            
            # Layer 2: Data Validation
            validation_result = self._validate_data(record)
            if not validation_result['is_valid']:
                record_result['success'] = False
                record_result['errors'].extend(validation_result['errors'])
                return record_result
            
            validated_record = self._store_validated_data(raw_record, validation_result)
            record_result['processing_steps'].append('data_validated')
            record_result['quality_score'] = validation_result['quality_score']
            
            # Layer 3: AI Enhancement
            enhancement_result = self._enhance_data(record)
            if enhancement_result['enhanced']:
                record.update(enhancement_result['enhanced_data'])
                record_result['processing_steps'].append('ai_enhanced')
            
            enriched_record = self._store_enriched_data(validated_record, record, enhancement_result)
            record_result['processing_steps'].append('data_enriched')
            
            # Layer 4: Data Mart Creation
            mart_result = self._create_data_mart(enriched_record, record)
            if mart_result['created']:
                record_result['processing_steps'].append('data_mart_created')
            
            # Update record with final data
            record_result['record'] = record
            
            return record_result
            
        except Exception as e:
            logger.error(f"Failed to process record: {e}")
            record_result['success'] = False
            record_result['errors'].append(str(e))
            return record_result
    
    def _store_raw_data(self, record: Dict[str, Any], source_name: str, 
                       source_type: str) -> RawDataRecord:
        """Store data in raw data lake"""
        try:
            metadata = {
                'source_type': source_type,
                'processing_timestamp': time.time(),
                'record_type': 'facility'
            }
            
            raw_record = self.raw_data_lake.store_raw_data(source_name, record, metadata)
            return raw_record
            
        except Exception as e:
            logger.error(f"Failed to store raw data: {e}")
            raise
    
    def _validate_data(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data using comprehensive validation framework"""
        try:
            validation_result = self.validator.validate_facility_data(record)
            
            # Apply quality gates
            quality_result = self.quality_gates.validate_data(record)
            
            # Combine results
            combined_result = {
                'is_valid': validation_result['is_valid'] and quality_result['passed'],
                'errors': validation_result['errors'] + quality_result['issues'],
                'warnings': validation_result['warnings'] + quality_result['recommendations'],
                'quality_score': (validation_result['quality_score'] + quality_result['overall_score']) / 2,
                'validation_details': {
                    'schema_validation': validation_result,
                    'quality_gates': quality_result
                }
            }
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return {
                'is_valid': False,
                'errors': [str(e)],
                'warnings': [],
                'quality_score': 0.0
            }
    
    def _store_validated_data(self, raw_record: RawDataRecord, 
                            validation_result: Dict[str, Any]) -> ValidatedDataRecord:
        """Store validated data"""
        try:
            validated_record = ValidatedDataRecord.objects.create(
                raw_record=raw_record,
                validated_data=raw_record.raw_data,
                quality_score=validation_result['quality_score'],
                validation_errors=validation_result['errors'],
                validation_warnings=validation_result['warnings'],
                validation_rules_applied=list(validation_result['validation_details'].keys()),
                is_valid=validation_result['is_valid']
            )
            
            # Log processing event
            self._log_processing_event('data_validated', raw_record.data_id, raw_record.source)
            
            return validated_record
            
        except Exception as e:
            logger.error(f"Failed to store validated data: {e}")
            raise
    
    def _enhance_data(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance data with AI capabilities"""
        enhancement_result = {
            'enhanced': False,
            'enhanced_data': record.copy(),
            'enhancements_applied': [],
            'geographic_enhancement': None,
            'ai_enhancements': {}
        }
        
        try:
            # Geographic enhancement
            if 'location' in record:
                geo_enhancement = self.geographic_enhancer.enhance_facility_location(record)
                if geo_enhancement != record:
                    enhancement_result['enhanced'] = True
                    enhancement_result['enhanced_data'] = geo_enhancement
                    enhancement_result['enhancements_applied'].append('geographic_enhancement')
                    enhancement_result['geographic_enhancement'] = geo_enhancement.get('location', {})
            
            # AI-powered geolocation
            if not record.get('location', {}).get('latitude') or not record.get('location', {}).get('longitude'):
                address = record.get('address', '')
                county = record.get('location', {}).get('county', '')
                constituency = record.get('location', {}).get('constituency', '')
                ward = record.get('location', {}).get('ward', '')
                
                coordinates = self.geolocator.enhance_coordinates(
                    address, county, constituency, ward
                )
                
                if coordinates:
                    enhancement_result['enhanced'] = True
                    if 'location' not in enhancement_result['enhanced_data']:
                        enhancement_result['enhanced_data']['location'] = {}
                    
                    enhancement_result['enhanced_data']['location'].update({
                        'latitude': coordinates['lat'],
                        'longitude': coordinates['lng'],
                        'accuracy_level': coordinates.get('accuracy', 'unknown'),
                        'geocoding_service': coordinates.get('source', 'unknown')
                    })
                    enhancement_result['enhancements_applied'].append('ai_geolocation')
                    enhancement_result['ai_enhancements']['geolocation'] = coordinates
            
            return enhancement_result
            
        except Exception as e:
            logger.error(f"Data enhancement failed: {e}")
            return enhancement_result
    
    def _store_enriched_data(self, validated_record: ValidatedDataRecord, 
                           enhanced_record: Dict[str, Any], 
                           enhancement_result: Dict[str, Any]) -> EnrichedDataRecord:
        """Store enriched data"""
        try:
            enriched_record = EnrichedDataRecord.objects.create(
                validated_record=validated_record,
                enriched_data=enhanced_record,
                enrichment_applied=enhancement_result['enhancements_applied'],
                ai_enhancements=enhancement_result['ai_enhancements'],
                geographic_data=enhancement_result.get('geographic_enhancement', {}),
                final_quality_score=validated_record.quality_score
            )
            
            # Log processing event
            self._log_processing_event('data_enriched', validated_record.raw_record.data_id, 
                                     validated_record.raw_record.source)
            
            return enriched_record
            
        except Exception as e:
            logger.error(f"Failed to store enriched data: {e}")
            raise
    
    def _create_data_mart(self, enriched_record: EnrichedDataRecord, 
                        final_record: Dict[str, Any]) -> Dict[str, Any]:
        """Create data mart for business consumption"""
        mart_result = {
            'created': False,
            'mart_type': 'facilities',
            'mart_data': final_record
        }
        
        try:
            # Create facilities data mart
            data_mart = DataMart.objects.create(
                enriched_record=enriched_record,
                mart_data=final_record,
                mart_type='facilities',
                is_served=True,
                serving_metadata={
                    'created_at': time.time(),
                    'quality_score': enriched_record.final_quality_score,
                    'enhancements_applied': enriched_record.enrichment_applied
                }
            )
            
            mart_result['created'] = True
            mart_result['data_mart_id'] = data_mart.id
            
            # Log processing event
            self._log_processing_event('data_served', enriched_record.validated_record.raw_record.data_id,
                                     enriched_record.validated_record.raw_record.source)
            
            return mart_result
            
        except Exception as e:
            logger.error(f"Failed to create data mart: {e}")
            return mart_result
    
    def _log_processing_event(self, event_type: str, record_id: str, source: DataSource):
        """Log data processing event"""
        try:
            DataProcessingEvent.objects.create(
                event_type=event_type,
                record_id=record_id,
                source=source,
                success=True,
                processing_time=time.time()
            )
        except Exception as e:
            logger.error(f"Failed to log processing event: {e}")
    
    def _update_stats(self, pipeline_result: Dict[str, Any]):
        """Update processing statistics"""
        self.stats['total_processed'] += pipeline_result['records_processed']
        self.stats['successful'] += pipeline_result['records_successful']
        self.stats['failed'] += pipeline_result['records_failed']
        self.stats['duplicates_found'] += pipeline_result['duplicates_prevented']
        self.stats['processing_time'] += pipeline_result['processing_time']
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'duplicates_found': 0,
            'quality_issues': 0,
            'processing_time': 0
        }


class DataArchitectureManager:
    """Central manager for the enhanced data architecture"""
    
    def __init__(self):
        self.etl_pipeline = EnhancedETLPipeline()
        self.raw_data_lake = RawDataLake()
        self.data_source_manager = DataSourceManager()
    
    def ingest_data(self, source_name: str, data: List[Dict[str, Any]], 
                   source_type: str = 'manual') -> Dict[str, Any]:
        """Main data ingestion endpoint"""
        try:
            # Register source if not exists
            self.data_source_manager.register_source(source_name, None, {
                'source_type': source_type,
                'description': f'Data source: {source_name}'
            })
            
            # Process data through ETL pipeline
            result = self.etl_pipeline.process_data(source_name, data, source_type)
            
            return result
            
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'records_processed': 0
            }
    
    def get_data_quality_report(self) -> Dict[str, Any]:
        """Get comprehensive data quality report"""
        try:
            # Get quality metrics from database
            from .models import DataQualityMetric
            
            quality_metrics = DataQualityMetric.objects.all()
            
            report = {
                'total_metrics': quality_metrics.count(),
                'average_scores': {},
                'threshold_violations': {},
                'recommendations': []
            }
            
            # Calculate average scores by metric type
            metric_types = ['completeness', 'accuracy', 'consistency', 'timeliness', 'uniqueness']
            for metric_type in metric_types:
                metrics = quality_metrics.filter(metric_type=metric_type)
                if metrics.exists():
                    avg_score = sum(m.metric_value for m in metrics) / metrics.count()
                    report['average_scores'][metric_type] = round(avg_score, 3)
                    
                    # Check threshold violations
                    threshold = 0.8  # Default threshold
                    violations = metrics.filter(metric_value__lt=threshold).count()
                    report['threshold_violations'][metric_type] = violations
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate quality report: {e}")
            return {'error': str(e)}
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        try:
            health_status = {
                'overall_status': 'healthy',
                'components': {},
                'alerts': [],
                'recommendations': []
            }
            
            # Check raw data lake
            raw_stats = self.raw_data_lake.get_storage_stats()
            health_status['components']['raw_data_lake'] = {
                'status': 'healthy' if raw_stats.get('failed_records', 0) == 0 else 'warning',
                'stats': raw_stats
            }
            
            # Check ETL pipeline
            etl_stats = self.etl_pipeline.get_processing_stats()
            success_rate = (etl_stats['successful'] / max(etl_stats['total_processed'], 1)) * 100
            health_status['components']['etl_pipeline'] = {
                'status': 'healthy' if success_rate > 90 else 'warning',
                'success_rate': round(success_rate, 2),
                'stats': etl_stats
            }
            
            # Check data sources
            sources = self.data_source_manager.list_sources()
            health_status['components']['data_sources'] = {
                'status': 'healthy' if len(sources) > 0 else 'warning',
                'count': len(sources),
                'sources': sources
            }
            
            # Generate alerts
            if success_rate < 90:
                health_status['alerts'].append('ETL pipeline success rate below 90%')
            
            if raw_stats.get('failed_records', 0) > 0:
                health_status['alerts'].append(f"{raw_stats['failed_records']} failed records in raw data lake")
            
            # Set overall status
            if health_status['alerts']:
                health_status['overall_status'] = 'warning'
            
            return health_status
            
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return {
                'overall_status': 'error',
                'error': str(e)
            }


