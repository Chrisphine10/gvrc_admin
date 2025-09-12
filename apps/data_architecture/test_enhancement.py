"""
Test Enhancement System
Quick test script for debugging and verification
"""

import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from apps.data_architecture.management.commands.enhance_facilities import Command
from django.core.management import call_command
from django.test import TestCase
import json


def test_enhancement_system():
    """Test the enhancement system with sample data"""
    print("🧪 Testing Enhancement System")
    print("=" * 50)
    
    # Test 1: Dry run with specific facility IDs
    print("\n1. Testing dry run with specific facilities...")
    try:
        call_command('enhance_facilities', 
                    facility_ids='1,2,3', 
                    dry_run=True, 
                    verbose=True,
                    step='extract')
        print("✅ Extract step completed successfully")
    except Exception as e:
        print(f"❌ Extract step failed: {e}")
        return False
    
    # Test 2: Test validation step
    print("\n2. Testing validation step...")
    try:
        call_command('enhance_facilities', 
                    facility_ids='1,2,3', 
                    dry_run=True, 
                    verbose=True,
                    step='validate')
        print("✅ Validation step completed successfully")
    except Exception as e:
        print(f"❌ Validation step failed: {e}")
        return False
    
    # Test 3: Test geolocation step
    print("\n3. Testing geolocation step...")
    try:
        call_command('enhance_facilities', 
                    facility_ids='1,2,3', 
                    dry_run=True, 
                    verbose=True,
                    step='geolocate')
        print("✅ Geolocation step completed successfully")
    except Exception as e:
        print(f"❌ Geolocation step failed: {e}")
        return False
    
    # Test 4: Test enhancement step
    print("\n4. Testing enhancement step...")
    try:
        call_command('enhance_facilities', 
                    facility_ids='1,2,3', 
                    dry_run=True, 
                    verbose=True,
                    step='enhance')
        print("✅ Enhancement step completed successfully")
    except Exception as e:
        print(f"❌ Enhancement step failed: {e}")
        return False
    
    # Test 5: Test full pipeline with output file
    print("\n5. Testing full pipeline with output...")
    try:
        output_file = '/tmp/enhanced_facilities_test.json'
        call_command('enhance_facilities', 
                    facility_ids='1,2,3', 
                    dry_run=True, 
                    verbose=True,
                    output_file=output_file)
        print("✅ Full pipeline completed successfully")
        
        # Check if output file was created
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                data = json.load(f)
            print(f"📄 Output file created with {len(data)} facilities")
            os.remove(output_file)  # Clean up
        else:
            print("⚠️  Output file not created")
            
    except Exception as e:
        print(f"❌ Full pipeline failed: {e}")
        return False
    
    print("\n🎉 All tests passed!")
    return True


def test_standalone_integration():
    """Test the standalone integration system"""
    print("\n🔧 Testing Standalone Integration")
    print("=" * 50)
    
    try:
        from apps.data_architecture.standalone_integration import StandaloneDataArchitecture
        
        # Initialize the system
        standalone = StandaloneDataArchitecture()
        print("✅ Standalone system initialized")
        
        # Test facility enhancement
        sample_facility = {
            'id': 1,
            'facility_name': 'Test Health Center',
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
        
        enhanced = standalone.enhance_facility_data(sample_facility)
        print("✅ Facility enhancement completed")
        print(f"📊 Enhanced facility: {enhanced['facility_name']}")
        
        # Test batch enhancement
        batch_result = standalone.batch_enhance_facilities([1, 2, 3])
        print("✅ Batch enhancement completed")
        print(f"📊 Batch result: {batch_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Standalone integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_quality():
    """Test data quality validation"""
    print("\n📊 Testing Data Quality Validation")
    print("=" * 50)
    
    try:
        from apps.data_architecture.data_validation import DataValidator, QualityGates
        
        # Test data validator
        validator = DataValidator()
        print("✅ Data validator initialized")
        
        # Test quality gates
        quality_gates = QualityGates()
        print("✅ Quality gates initialized")
        
        # Test with sample facility data
        sample_data = {
            'facility_name': 'Test Health Center',
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
        
        # Validate data
        validation_result = validator.validate_facility_data(sample_data)
        print(f"✅ Validation completed: {validation_result['is_valid']}")
        print(f"📊 Quality score: {validation_result['quality_score']:.2f}")
        
        # Test quality gates
        quality_result = quality_gates.validate_data(sample_data)
        print(f"✅ Quality gates completed: {quality_result['passed']}")
        print(f"📊 Overall score: {quality_result['overall_score']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data quality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Data Architecture Enhancement Tests")
    print("=" * 60)
    
    tests = [
        ("Enhancement System", test_enhancement_system),
        ("Standalone Integration", test_standalone_integration),
        ("Data Quality", test_data_quality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
