#!/usr/bin/env python3
"""
Test Script for Emergency Chat System
"""

import requests
import json
import time

# Base URL for the chat system
BASE_URL = "http://localhost:8000"

def create_mobile_session():
    """Create a mobile session for testing"""
    print("🧪 Creating Mobile Session...")
    
    # First, let's try to create a mobile session via the mobile_sessions API
    # If that doesn't exist, we'll need to create it directly in the database
    url = f"{BASE_URL}/api/mobile/sessions/"
    data = {
        "device_id": "test-device-123",
        "notification_enabled": True,
        "preferred_language": "en"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Mobile session created: {result.get('device_id')}")
            return True
        else:
            print(f"❌ Failed to create mobile session: {response.text}")
            print("⚠️  Mobile session API not available, will need to create manually")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_mobile_conversation_start():
    """Test starting a mobile conversation"""
    print("🧪 Testing Mobile Conversation Start...")
    
    url = f"{BASE_URL}/chat/mobile/conversations/start/"
    data = {
        "device_id": "test-device-123",
        "subject": "Emergency test message"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Success! Conversation ID: {result.get('conversation_id')}")
            print(f"Status: {result.get('status')}")
            return result.get('conversation_id')
        else:
            print(f"❌ Failed: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_mobile_send_message(conversation_id):
    """Test sending a message from mobile"""
    if not conversation_id:
        print("❌ No conversation ID to test with")
        return
    
    print(f"🧪 Testing Mobile Message Send for Conversation {conversation_id}...")
    
    url = f"{BASE_URL}/chat/mobile/conversations/{conversation_id}/send-message/"
    data = {
        "content": "This is a test emergency message!",
        "message_type": "text",
        "is_urgent": True
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Success! Message ID: {result.get('message_id')}")
            return result.get('message_id')
        else:
            print(f"❌ Failed: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_mobile_conversation_list():
    """Test listing mobile conversations"""
    print("🧪 Testing Mobile Conversation List...")
    
    url = f"{BASE_URL}/chat/mobile/conversations/list/"
    params = {"device_id": "test-device-123"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Found {len(result)} conversations")
            for conv in result:
                print(f"  - Conversation {conv.get('conversation_id')}: {conv.get('subject')}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_admin_conversation_list():
    """Test admin conversation list (will fail without auth)"""
    print("🧪 Testing Admin Conversation List (should fail without auth)...")
    
    url = f"{BASE_URL}/chat/admin/conversations/list/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Expected failure - authentication required")
            return True
        else:
            print(f"❌ Unexpected response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_swagger_documentation():
    """Test if Swagger documentation is accessible"""
    print("🧪 Testing Swagger Documentation...")
    
    url = f"{BASE_URL}/swagger/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Swagger documentation accessible")
            return True
        else:
            print(f"❌ Swagger not accessible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_mobile_sessions_api():
    """Test if mobile sessions API is available"""
    print("🧪 Testing Mobile Sessions API...")
    
    url = f"{BASE_URL}/api/mobile/sessions/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Mobile sessions API accessible")
            return True
        else:
            print(f"❌ Mobile sessions API not accessible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚨 Emergency Chat System Test Suite")
    print("=" * 50)
    
    # Test API availability first
    test_mobile_sessions_api()
    time.sleep(1)
    
    # Try to create mobile session
    session_created = create_mobile_session()
    time.sleep(1)
    
    # Test basic functionality
    conversation_id = test_mobile_conversation_start()
    time.sleep(1)
    
    if conversation_id:
        test_mobile_send_message(conversation_id)
        time.sleep(1)
    
    test_mobile_conversation_list()
    time.sleep(1)
    
    test_admin_conversation_list()
    time.sleep(1)
    
    test_swagger_documentation()
    
    print("\n" + "=" * 50)
    print("🏁 Test Suite Complete!")
    print("\nNext Steps:")
    print("1. Access admin interface: http://localhost:8000/admin/")
    print("2. View Swagger docs: http://localhost:8000/swagger/")
    print("3. Test WebSocket connections manually")
    print("4. Create admin user and test admin endpoints")
    
    if not session_created:
        print("\n⚠️  IMPORTANT: Mobile session creation failed!")
        print("   You may need to create a mobile session manually in the database")
        print("   or implement the mobile sessions API endpoint")

if __name__ == "__main__":
    main()
