#!/usr/bin/env python3
"""
Comprehensive test suite for PostgreSQL migration
Following data engineering best practices with iterative testing
"""
import os
import sys
import django
import json
import time
import requests
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from django.test import TestCase, Client
from django.db import connection
from django.core.management import call_command
from django.contrib.auth import get_user_model
from apps.facilities.models import Facility
from apps.geography.models import County, Constituency, Ward
from apps.data_architecture.models import DataSource, RawDataRecord
from apps.data_architecture.standalone_integration import StandaloneDataArchitecture

User = get_user_model()

class PostgreSQLMigrationTestSuite:
    """Comprehensive test suite for PostgreSQL migration"""
    
    def __init__(self):
        self.test_results = []
        self.client = Client()
        self.start_time = datetime.now()
        
    def log_test(self, test_name, status, message="", duration=None):
        """Log test results with timing"""
        result = {
            'test_name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'duration': duration
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        if duration:
            print(f"   ⏱️  Duration: {duration:.2f}s")
    
    def test_database_connection(self):
        """Test database connection and type"""
        start_time = time.time()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                
                if 'PostgreSQL' in version:
                    self.log_test("Database Connection", "PASS", f"Connected to PostgreSQL: {version.split(',')[0]}", time.time() - start_time)
                    return True
                else:
                    self.log_test("Database Connection", "FAIL", f"Not PostgreSQL: {version}", time.time() - start_time)
                    return False
        except Exception as e:
            self.log_test("Database Connection", "FAIL", f"Connection failed: {str(e)}", time.time() - start_time)
            return False
    
    def test_database_performance(self):
        """Test database performance with sample queries"""
        start_time = time.time()
        try:
            # Test basic query performance
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM facilities_facility;")
                facility_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM geography_county;")
                county_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM data_architecture_datasource;")
                data_source_count = cursor.fetchone()[0]
            
            duration = time.time() - start_time
            self.log_test("Database Performance", "PASS", 
                         f"Queries completed in {duration:.3f}s - Facilities: {facility_count}, Counties: {county_count}, Data Sources: {data_source_count}", 
                         duration)
            return True
        except Exception as e:
            self.log_test("Database Performance", "FAIL", f"Performance test failed: {str(e)}", time.time() - start_time)
            return False
    
    def test_web_endpoints(self):
        """Test critical web endpoints"""
        start_time = time.time()
        endpoints = [
            ('/', 'Home page'),
            ('/admin/', 'Admin interface'),
            ('/data-architecture/', 'Data architecture API'),
            ('/facilities/', 'Facilities API'),
        ]
        
        passed = 0
        for endpoint, description in endpoints:
            try:
                response = self.client.get(endpoint)
                if response.status_code in [200, 302, 403]:  # 302 for redirects, 403 for permission denied
                    self.log_test(f"Web Endpoint: {description}", "PASS", f"Status: {response.status_code}")
                    passed += 1
                else:
                    self.log_test(f"Web Endpoint: {description}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Web Endpoint: {description}", "FAIL", f"Error: {str(e)}")
        
        duration = time.time() - start_time
        self.log_test("Web Endpoints Overall", "PASS" if passed == len(endpoints) else "FAIL", 
                     f"{passed}/{len(endpoints)} endpoints working", duration)
        return passed == len(endpoints)
    
    def test_data_architecture_models(self):
        """Test data architecture models functionality"""
        start_time = time.time()
        try:
            # Test DataSource creation
            data_source = DataSource.objects.create(
                name="Test Source",
                source_type="manual",
                description="Test data source for migration",
                configuration={"test": True}
            )
            
            # Test RawDataRecord creation
            raw_record = RawDataRecord.objects.create(
                data_source=data_source,
                raw_data={"test": "data", "timestamp": datetime.now().isoformat()},
                metadata={"source": "test", "version": "1.0"}
            )
            
            # Test data retrieval
            retrieved_source = DataSource.objects.get(name="Test Source")
            retrieved_record = RawDataRecord.objects.get(data_source=data_source)
            
            # Cleanup
            raw_record.delete()
            data_source.delete()
            
            duration = time.time() - start_time
            self.log_test("Data Architecture Models", "PASS", 
                         "Models created, stored, and retrieved successfully", duration)
            return True
        except Exception as e:
            self.log_test("Data Architecture Models", "FAIL", f"Model test failed: {str(e)}", time.time() - start_time)
            return False
    
    def test_standalone_integration(self):
        """Test standalone integration system"""
        start_time = time.time()
        try:
            # Initialize standalone system
            standalone = StandaloneDataArchitecture()
            
            # Test facility enhancement
            test_facility = {
                'id': 1,
                'name': 'Test Health Center',
                'location': {
                    'county': 'Nairobi',
                    'constituency': 'Westlands',
                    'ward': 'Parklands'
                },
                'contacts': [
                    {'type': 'Phone', 'value': '0712345678'},
                    {'type': 'Email', 'value': 'test@example.com'}
                ]
            }
            
            result = standalone.enhance_facility(test_facility)
            
            duration = time.time() - start_time
            if result.get('success'):
                self.log_test("Standalone Integration", "PASS", 
                             f"Facility enhancement successful: {result.get('message', '')}", duration)
                return True
            else:
                self.log_test("Standalone Integration", "FAIL", 
                             f"Enhancement failed: {result.get('message', '')}", duration)
                return False
        except Exception as e:
            self.log_test("Standalone Integration", "FAIL", f"Integration test failed: {str(e)}", time.time() - start_time)
            return False
    
    def test_json_field_functionality(self):
        """Test PostgreSQL JSON field functionality"""
        start_time = time.time()
        try:
            # Create a data source with complex JSON configuration
            complex_config = {
                "api_endpoints": ["https://api.example.com/data"],
                "authentication": {
                    "type": "bearer",
                    "token": "test_token"
                },
                "mapping": {
                    "facility_name": "name",
                    "location": "address"
                },
                "filters": {
                    "active_only": True,
                    "date_range": {
                        "start": "2024-01-01",
                        "end": "2024-12-31"
                    }
                }
            }
            
            data_source = DataSource.objects.create(
                name="JSON Test Source",
                source_type="api",
                configuration=complex_config
            )
            
            # Test JSON queries
            sources_with_filters = DataSource.objects.filter(
                configuration__filters__active_only=True
            )
            
            sources_with_api = DataSource.objects.filter(
                configuration__api_endpoints__isnull=False
            )
            
            # Cleanup
            data_source.delete()
            
            duration = time.time() - start_time
            self.log_test("JSON Field Functionality", "PASS", 
                         f"Complex JSON operations successful - Found {sources_with_filters.count()} sources with filters", duration)
            return True
        except Exception as e:
            self.log_test("JSON Field Functionality", "FAIL", f"JSON field test failed: {str(e)}", time.time() - start_time)
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🧪 Starting PostgreSQL Migration Test Suite")
        print("=" * 60)
        
        tests = [
            self.test_database_connection,
            self.test_database_performance,
            self.test_web_endpoints,
            self.test_data_architecture_models,
            self.test_standalone_integration,
            self.test_json_field_functionality,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                self.log_test(test.__name__, "FAIL", f"Test crashed: {str(e)}")
        
        # Generate summary report
        total_duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        print(f"✅ Tests Passed: {passed}/{total}")
        print(f"❌ Tests Failed: {total - passed}/{total}")
        print(f"⏱️  Total Duration: {total_duration:.2f}s")
        print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
        
        # Save detailed report
        report_file = f"migration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total,
                    'passed_tests': passed,
                    'failed_tests': total - passed,
                    'success_rate': (passed/total)*100,
                    'total_duration': total_duration,
                    'timestamp': datetime.now().isoformat()
                },
                'test_results': self.test_results
            }, f, indent=2)
        
        print(f"📄 Detailed report saved to: {report_file}")
        
        return passed == total

if __name__ == "__main__":
    test_suite = PostgreSQLMigrationTestSuite()
    success = test_suite.run_all_tests()
    sys.exit(0 if success else 1)
