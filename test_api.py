#!/usr/bin/env python3
"""
Simple API test script for GVRC Admin API
Run this script to test the API endpoints
"""

import requests
import json
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:8000"  # Change this to your server URL
API_BASE = urljoin(BASE_URL, "api/")

def test_api_endpoint(endpoint, method="GET", data=None, headers=None):
    """Test a specific API endpoint"""
    url = urljoin(API_BASE, endpoint)
    
    print(f"\n{'='*60}")
    print(f"Testing: {method} {url}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(f"Response Data: {json.dumps(response_data, indent=2)}")
                return True
            except json.JSONDecodeError:
                print(f"Response Text: {response.text}")
                return False
        else:
            print(f"Error Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return False

def test_authentication():
    """Test authentication endpoints"""
    print("\n🔐 Testing Authentication Endpoints")
    
    # Test API status (should work without auth)
    test_api_endpoint("status/")
    
    # Test hello world (should work without auth)
    test_api_endpoint("hello/")

def test_facility_endpoints():
    """Test facility-related endpoints"""
    print("\n🏥 Testing Facility Endpoints")
    
    # Test facility list (will require authentication)
    test_api_endpoint("facilities/")
    
    # Test facility map view
    test_api_endpoint("facilities/map/")
    
    # Test facility search
    search_data = {
        "search": "health",
        "page": 1,
        "page_size": 10
    }
    test_api_endpoint("facilities/search/", method="POST", data=search_data)

def test_geography_endpoints():
    """Test geography endpoints"""
    print("\n🗺️ Testing Geography Endpoints")
    
    test_api_endpoint("geography/counties/")
    test_api_endpoint("geography/constituencies/")
    test_api_endpoint("geography/wards/")

def test_statistics_and_lookups():
    """Test statistics and lookup endpoints"""
    print("\n📊 Testing Statistics and Lookup Endpoints")
    
    test_api_endpoint("statistics/")
    test_api_endpoint("lookups/")

def test_with_authentication():
    """Test endpoints with authentication token"""
    print("\n🔑 Testing with Authentication")
    
    # You would need to get a valid token first
    # This is just an example structure
    auth_headers = {
        "Authorization": "Token YOUR_TOKEN_HERE",
        "Content-Type": "application/json"
    }
    
    print("Note: To test authenticated endpoints, you need to:")
    print("1. Create a user account")
    print("2. Get an authentication token")
    print("3. Update the auth_headers in this script")
    
    # Test with auth headers (will fail without valid token)
    test_api_endpoint("facilities/", headers=auth_headers)

def main():
    """Main test function"""
    print("🚀 GVRC Admin API Test Script")
    print(f"Testing API at: {BASE_URL}")
    
    # Test public endpoints
    test_authentication()
    
    # Test facility endpoints (will show auth required)
    test_facility_endpoints()
    
    # Test geography endpoints (will show auth required)
    test_geography_endpoints()
    
    # Test statistics and lookups (will show auth required)
    test_statistics_and_lookups()
    
    # Show how to test with authentication
    test_with_authentication()
    
    print("\n✅ API testing completed!")
    print("\n📝 Next steps:")
    print("1. Start your Django server: python manage.py runserver")
    print("2. Create a user account through the admin interface")
    print("3. Get an authentication token")
    print("4. Update the test script with your token")
    print("5. Run the tests again to verify authenticated endpoints")

if __name__ == "__main__":
    main()
