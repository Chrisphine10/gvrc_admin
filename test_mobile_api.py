#!/usr/bin/env python3
"""
Test script for Mobile API endpoints
Run this to test the mobile API functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_mobile_session_creation():
    """Test creating a mobile session"""
    print("\n🔐 Testing Mobile Session Creation")
    print("=" * 50)
    
    url = f"{API_BASE}/mobile/sessions/"
    data = {
        "device_id": "test_device_123",
        "latitude": -1.2921,
        "longitude": 36.8219,
        "location_permission_granted": True
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Mobile session created successfully")
            return True
        else:
            print("❌ Failed to create mobile session")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_contact_interaction():
    """Test contact interaction endpoint"""
    print("\n📞 Testing Contact Interaction")
    print("=" * 50)
    
    url = f"{API_BASE}/mobile/contact-interaction/"
    data = {
        "device_id": "test_device_123",
        "contact_id": 1,  # Use a valid contact ID
        "is_helpful": True
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Contact interaction tracked successfully")
            return True
        else:
            print("❌ Failed to track contact interaction")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_emergency_sos():
    """Test emergency SOS endpoint"""
    print("\n🚨 Testing Emergency SOS")
    print("=" * 50)
    
    url = f"{API_BASE}/mobile/emergency-sos/"
    data = {
        "device_id": "test_device_123",
        "emergency_type": "Medical",
        "radius_km": 5
    }
    
    print(f"Request URL: {url}")
    print(f"Request Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Emergency SOS request successful")
            return True
        else:
            print("❌ Failed to process emergency SOS")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mobile_facilities():
    """Test mobile facilities endpoint"""
    print("\n🏥 Testing Mobile Facilities")
    print("=" * 50)
    
    url = f"{API_BASE}/mobile/facilities/"
    params = {
        "device_id": "test_device_123",
        "page": 1,
        "page_size": 5
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")  # Show first 200 chars
        
        if response.status_code == 200:
            print("✅ Mobile facilities retrieved successfully")
            return True
        else:
            print("❌ Failed to retrieve mobile facilities")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mobile_session_status():
    """Test checking mobile session status"""
    print("\n📱 Testing Mobile Session Status")
    print("=" * 50)
    
    # Try to access a protected endpoint to see session status
    url = f"{API_BASE}/mobile/facilities/"
    params = {"device_id": "test_device_123"}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Mobile session is active and valid")
            return True
        elif response.status_code == 401:
            print("❌ Mobile session not found or inactive")
            return False
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Mobile API Testing Suite")
    print("=" * 50)
    
    # Test sequence
    tests = [
        ("Mobile Session Creation", test_mobile_session_creation),
        ("Mobile Session Status Check", test_mobile_session_status),
        ("Contact Interaction", test_contact_interaction),
        ("Emergency SOS", test_emergency_sos),
        ("Mobile Facilities", test_mobile_facilities)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()
