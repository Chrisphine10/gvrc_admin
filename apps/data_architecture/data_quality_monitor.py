"""
Data Quality Monitoring System
Comprehensive data quality gates and monitoring for the enhanced data architecture
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from django.db import connection
from django.conf import settings
from .models import DataQualityMetric, DataProcessingEvent, RawDataRecord, ValidatedDataRecord
import json

logger = logging.getLogger(__name__)


class DataQualityMonitor:
    """
    Comprehensive data quality monitoring system
    Implements data quality gates, metrics collection, and alerting
    """
    
    def __init__(self):
        self.quality_thresholds = {
            'completeness': 0.95,  # 95% completeness required
            'accuracy': 0.90,      # 90% accuracy required
            'consistency': 0.95,   # 95% consistency required
            'timeliness': 0.90,    # 90% timeliness required
            'uniqueness': 0.98,    # 98% uniqueness required
        }
        
        self.alert_thresholds = {
            'critical': 0.80,      # Below 80% triggers critical alert
            'warning': 0.90,       # Below 90% triggers warning
        }
    
    def run_quality_checks(self) -> Dict[str, Any]:
        """
        Run comprehensive data quality checks
        Returns quality metrics and alerts
        """
        logger.info("Starting comprehensive data quality checks")
        
        quality_results = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0.0,
            'status': 'unknown',
            'metrics': {},
            'alerts': [],
            'recommendations': []
        }
        
        try:
            # Run individual quality checks
            completeness = self._check_completeness()
            accuracy = self._check_accuracy()
            consistency = self._check_consistency()
            timeliness = self._check_timeliness()
            uniqueness = self._check_uniqueness()
            
            # Store metrics
            quality_results['metrics'] = {
                'completeness': completeness,
                'accuracy': accuracy,
                'consistency': consistency,
                'timeliness': timeliness,
                'uniqueness': uniqueness
            }
            
            # Calculate overall score
            overall_score = sum(quality_results['metrics'].values()) / len(quality_results['metrics'])
            quality_results['overall_score'] = round(overall_score, 3)
            
            # Determine status and generate alerts
            quality_results['status'] = self._determine_status(overall_score)
            quality_results['alerts'] = self._generate_alerts(quality_results['metrics'])
            quality_results['recommendations'] = self._generate_recommendations(quality_results['metrics'])
            
            # Store metrics in database
            self._store_quality_metrics(quality_results)
            
            logger.info(f"Quality checks completed. Overall score: {overall_score:.3f}")
            return quality_results
            
        except Exception as e:
            logger.error(f"Quality checks failed: {str(e)}")
            quality_results['status'] = 'error'
            quality_results['alerts'].append({
                'level': 'critical',
                'message': f'Quality check failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
            return quality_results
    
    def _check_completeness(self) -> float:
        """Check data completeness across all tables"""
        try:
            with connection.cursor() as cursor:
                # Check facilities table completeness
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(facility_name) as name_complete,
                        COUNT(facility_type_id) as type_complete,
                        COUNT(county_id) as county_complete,
                        COUNT(operational_status_id) as status_complete
                    FROM facilities 
                    WHERE is_active = true
                """)
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return 0.0
                
                total = result[0]
                complete_fields = sum([1 for x in result[1:] if x == total])
                total_fields = len(result) - 1
                
                completeness = complete_fields / total_fields
                return round(completeness, 3)
                
        except Exception as e:
            logger.error(f"Completeness check failed: {str(e)}")
            return 0.0
    
    def _check_accuracy(self) -> float:
        """Check data accuracy using validation rules"""
        try:
            with connection.cursor() as cursor:
                # Check for valid email formats in facility contacts
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_contacts,
                        COUNT(CASE WHEN contact_value ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' 
                                   THEN 1 END) as valid_emails
                    FROM facility_contacts 
                    WHERE contact_type_id IN (
                        SELECT contact_type_id FROM contact_types WHERE type_name = 'Email'
                    )
                """)
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return 1.0  # No email data to validate
                
                accuracy = result[1] / result[0]
                return round(accuracy, 3)
                
        except Exception as e:
            logger.error(f"Accuracy check failed: {str(e)}")
            return 0.0
    
    def _check_consistency(self) -> float:
        """Check data consistency across related tables"""
        try:
            with connection.cursor() as cursor:
                # Check referential integrity
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_facilities,
                        COUNT(CASE WHEN f.ward_id IS NOT NULL AND w.ward_id IS NOT NULL 
                                   THEN 1 END) as consistent_wards
                    FROM facilities f
                    LEFT JOIN wards w ON f.ward_id = w.ward_id
                    WHERE f.is_active = true
                """)
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return 1.0
                
                consistency = result[1] / result[0]
                return round(consistency, 3)
                
        except Exception as e:
            logger.error(f"Consistency check failed: {str(e)}")
            return 0.0
    
    def _check_timeliness(self) -> float:
        """Check data timeliness (recent updates)"""
        try:
            with connection.cursor() as cursor:
                # Check for recent data updates
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_facilities,
                        COUNT(CASE WHEN updated_at > NOW() - INTERVAL '30 days' 
                                   THEN 1 END) as recent_updates
                    FROM facilities 
                    WHERE is_active = true
                """)
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return 1.0
                
                timeliness = result[1] / result[0]
                return round(timeliness, 3)
                
        except Exception as e:
            logger.error(f"Timeliness check failed: {str(e)}")
            return 0.0
    
    def _check_uniqueness(self) -> float:
        """Check data uniqueness (no duplicates)"""
        try:
            with connection.cursor() as cursor:
                # Check for duplicate facility names
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_facilities,
                        COUNT(DISTINCT facility_name) as unique_names
                    FROM facilities 
                    WHERE is_active = true AND facility_name IS NOT NULL
                """)
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return 1.0
                
                uniqueness = result[1] / result[0]
                return round(uniqueness, 3)
                
        except Exception as e:
            logger.error(f"Uniqueness check failed: {str(e)}")
            return 0.0
    
    def _determine_status(self, overall_score: float) -> str:
        """Determine overall quality status based on score"""
        if overall_score >= self.quality_thresholds['completeness']:
            return 'excellent'
        elif overall_score >= self.alert_thresholds['warning']:
            return 'good'
        elif overall_score >= self.alert_thresholds['critical']:
            return 'warning'
        else:
            return 'critical'
    
    def _generate_alerts(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate quality alerts based on metrics"""
        alerts = []
        
        for metric_name, score in metrics.items():
            if score < self.alert_thresholds['critical']:
                alerts.append({
                    'level': 'critical',
                    'metric': metric_name,
                    'score': score,
                    'threshold': self.alert_thresholds['critical'],
                    'message': f'{metric_name.title()} is critically low: {score:.1%}',
                    'timestamp': datetime.now().isoformat()
                })
            elif score < self.alert_thresholds['warning']:
                alerts.append({
                    'level': 'warning',
                    'metric': metric_name,
                    'score': score,
                    'threshold': self.alert_thresholds['warning'],
                    'message': f'{metric_name.title()} is below warning threshold: {score:.1%}',
                    'timestamp': datetime.now().isoformat()
                })
        
        return alerts
    
    def _generate_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """Generate improvement recommendations based on metrics"""
        recommendations = []
        
        for metric_name, score in metrics.items():
            if score < self.quality_thresholds[metric_name]:
                if metric_name == 'completeness':
                    recommendations.append("Implement data validation rules to ensure required fields are filled")
                elif metric_name == 'accuracy':
                    recommendations.append("Add data validation for email formats and other structured data")
                elif metric_name == 'consistency':
                    recommendations.append("Review and fix referential integrity issues")
                elif metric_name == 'timeliness':
                    recommendations.append("Implement automated data refresh processes")
                elif metric_name == 'uniqueness':
                    recommendations.append("Add duplicate detection and deduplication processes")
        
        return recommendations
    
    def _store_quality_metrics(self, quality_results: Dict[str, Any]):
        """Store quality metrics in database"""
        try:
            from django.utils import timezone
            
            # Store overall quality metric
            DataQualityMetric.objects.create(
                record_type='raw',
                record_id='overall_quality',
                metric_type='completeness',  # Use existing metric type
                metric_value=quality_results['overall_score'],
                threshold=self.quality_thresholds['completeness'],
                passed=quality_results['overall_score'] >= self.quality_thresholds['completeness'],
                details=quality_results
            )
            
            # Store individual metrics
            for metric_name, value in quality_results['metrics'].items():
                DataQualityMetric.objects.create(
                    record_type='raw',
                    record_id=f'quality_check_{metric_name}',
                    metric_type=metric_name,
                    metric_value=value,
                    threshold=self.quality_thresholds[metric_name],
                    passed=value >= self.quality_thresholds[metric_name],
                    details={'timestamp': timezone.now().isoformat()}
                )
            
            # Log processing event
            DataProcessingEvent.objects.create(
                event_type='quality_check',
                status='completed',
                message=f"Quality check completed. Overall score: {quality_results['overall_score']:.3f}",
                metadata=json.dumps({
                    'alerts_count': len(quality_results['alerts']),
                    'recommendations_count': len(quality_results['recommendations'])
                })
            )
            
        except Exception as e:
            logger.error(f"Failed to store quality metrics: {str(e)}")
    
    def get_quality_dashboard_data(self) -> Dict[str, Any]:
        """Get data for quality dashboard"""
        try:
            from django.utils import timezone
            
            # Get recent quality metrics
            recent_metrics = DataQualityMetric.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).order_by('-created_at')
            
            # Get quality trends
            trends = {}
            for metric in recent_metrics:
                if metric.metric_type not in trends:
                    trends[metric.metric_type] = []
                trends[metric.metric_type].append({
                    'timestamp': metric.created_at.isoformat(),
                    'value': float(metric.metric_value)
                })
            
            # Get current status
            latest_overall = DataQualityMetric.objects.filter(
                record_id='overall_quality'
            ).order_by('-created_at').first()
            
            return {
                'current_status': 'good' if latest_overall and latest_overall.passed else 'warning',
                'current_score': float(latest_overall.metric_value) if latest_overall else 0.0,
                'trends': trends,
                'last_check': latest_overall.created_at.isoformat() if latest_overall else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {str(e)}")
            return {
                'current_status': 'error',
                'current_score': 0.0,
                'trends': {},
                'last_check': None
            }
    
    def setup_quality_gates(self) -> Dict[str, Any]:
        """Set up automated quality gates"""
        try:
            # Create quality gate rules
            gate_rules = {
                'data_ingestion': {
                    'completeness_threshold': 0.90,
                    'validation_rules': ['required_fields', 'email_format', 'phone_format'],
                    'enabled': True
                },
                'data_processing': {
                    'accuracy_threshold': 0.85,
                    'consistency_threshold': 0.90,
                    'enabled': True
                },
                'data_export': {
                    'uniqueness_threshold': 0.95,
                    'timeliness_threshold': 0.80,
                    'enabled': True
                }
            }
            
            # Store gate rules in database
            DataProcessingEvent.objects.create(
                event_type='quality_gate_setup',
                status='completed',
                message='Quality gates configured successfully',
                metadata=json.dumps(gate_rules)
            )
            
            logger.info("Quality gates set up successfully")
            return {
                'status': 'success',
                'message': 'Quality gates configured',
                'rules': gate_rules
            }
            
        except Exception as e:
            logger.error(f"Failed to set up quality gates: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }


# Global quality monitor instance
quality_monitor = DataQualityMonitor()
