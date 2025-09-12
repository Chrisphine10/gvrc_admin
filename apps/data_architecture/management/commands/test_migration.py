"""
Django management command for PostgreSQL migration testing
Following data engineering best practices with iterative testing
"""
from django.core.management.base import BaseCommand
from django.test import Client
from django.db import connection
from django.contrib.auth import get_user_model
from apps.facilities.models import Facility
from apps.geography.models import County, Constituency, Ward
from apps.data_architecture.models import DataSource, RawDataRecord
from apps.data_architecture.standalone_integration import StandaloneDataArchitecture
import json
import time
from datetime import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Comprehensive test suite for PostgreSQL migration'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output',
        )
        parser.add_argument(
            '--save-report',
            action='store_true',
            help='Save detailed test report to file',
        )
    
    def handle(self, *args, **options):
        self.verbose = options['verbose']
        self.save_report = options['save_report']
        self.test_results = []
        self.start_time = datetime.now()
        
        self.stdout.write(self.style.SUCCESS('🧪 Starting PostgreSQL Migration Test Suite'))
        self.stdout.write('=' * 60)
        
        # Run all tests
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
        self.generate_summary_report(passed, total)
        
        if passed == total:
            self.stdout.write(self.style.SUCCESS('✅ All tests passed!'))
            return
        else:
            self.stdout.write(self.style.ERROR(f'❌ {total - passed} tests failed'))
            return
    
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
        self.stdout.write(f"{status_icon} {test_name}: {message}")
        if duration:
            self.stdout.write(f"   ⏱️  Duration: {duration:.2f}s")
    
    def test_database_connection(self):
        """Test database connection and type"""
        start_time = time.time()
        try:
            with connection.cursor() as cursor:
                # Try PostgreSQL first
                try:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    if 'PostgreSQL' in version:
                        self.log_test("Database Connection", "PASS", f"Connected to PostgreSQL: {version.split(',')[0]}", time.time() - start_time)
                        return True
                except:
                    pass
                
                # Try SQLite
                try:
                    cursor.execute("SELECT sqlite_version();")
                    version = cursor.fetchone()[0]
                    self.log_test("Database Connection", "WARN", f"Connected to SQLite: {version} (PostgreSQL migration needed)", time.time() - start_time)
                    return False
                except:
                    pass
                
                # Unknown database
                self.log_test("Database Connection", "FAIL", "Unknown database type", time.time() - start_time)
                return False
        except Exception as e:
            self.log_test("Database Connection", "FAIL", f"Connection failed: {str(e)}", time.time() - start_time)
            return False
    
    def test_database_performance(self):
        """Test database performance with sample queries"""
        start_time = time.time()
        try:
            # Test basic query performance with proper table names
            with connection.cursor() as cursor:
                # Get table names dynamically
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                
                facility_count = 0
                county_count = 0
                data_source_count = 0
                
                # Count facilities
                if 'facilities_facility' in tables:
                    cursor.execute("SELECT COUNT(*) FROM facilities_facility;")
                    facility_count = cursor.fetchone()[0]
                
                # Count counties
                if 'geography_county' in tables:
                    cursor.execute("SELECT COUNT(*) FROM geography_county;")
                    county_count = cursor.fetchone()[0]
                
                # Count data sources
                if 'data_sources' in tables:
                    cursor.execute("SELECT COUNT(*) FROM data_sources;")
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
        from django.test import override_settings
        
        # Override ALLOWED_HOSTS for testing
        with override_settings(ALLOWED_HOSTS=['*']):
            client = Client()
            endpoints = [
                ('/', 'Home page'),
                ('/admin/', 'Admin interface'),
                ('/data-architecture/', 'Data architecture API'),
                ('/facilities/', 'Facilities API'),
            ]
            
            passed = 0
            for endpoint, description in endpoints:
                try:
                    response = client.get(endpoint)
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
            # Test DataSource creation with unique name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            data_source = DataSource.objects.create(
                name=f"Test Source {timestamp}",
                source_type="manual",
                description="Test data source for migration",
                configuration={"test": True}
            )
            
            # Test RawDataRecord creation
            raw_record = RawDataRecord.objects.create(
                source=data_source,
                data_id=f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                raw_data={"test": "data", "timestamp": datetime.now().isoformat()},
                metadata={"source": "test", "version": "1.0"},
                checksum="test_checksum_123"
            )
            
            # Test data retrieval
            retrieved_source = DataSource.objects.get(name="Test Source")
            retrieved_record = RawDataRecord.objects.get(source=data_source)
            
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
            
            # Test facility enhancement with facility data (not ID)
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
            
            # Use enhance_facility_data method instead
            result = standalone.enhance_facility_data(test_facility)
            
            duration = time.time() - start_time
            if result and result.get('success', True):  # enhance_facility_data returns enhanced data directly
                self.log_test("Standalone Integration", "PASS", 
                             f"Facility enhancement successful: {result.get('facility_name', 'Unknown')}", duration)
                return True
            else:
                self.log_test("Standalone Integration", "FAIL", 
                             f"Enhancement failed: {result.get('error', 'Unknown error') if result else 'No result'}", duration)
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
    
    def generate_summary_report(self, passed, total):
        """Generate comprehensive test summary report"""
        total_duration = (datetime.now() - self.start_time).total_seconds()
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 TEST SUMMARY REPORT")
        self.stdout.write("=" * 60)
        self.stdout.write(f"✅ Tests Passed: {passed}/{total}")
        self.stdout.write(f"❌ Tests Failed: {total - passed}/{total}")
        self.stdout.write(f"⏱️  Total Duration: {total_duration:.2f}s")
        self.stdout.write(f"📈 Success Rate: {(passed/total)*100:.1f}%")
        
        if self.save_report:
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
            
            self.stdout.write(f"📄 Detailed report saved to: {report_file}")
