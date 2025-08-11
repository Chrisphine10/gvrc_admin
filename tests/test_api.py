import pytest
import django
from django.conf import settings

# Ensure Django is properly configured
if not settings.configured:
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
    django.setup()

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class APIEndpointsTestCase(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_hello_endpoint(self):
        """Test /api/hello/ endpoint"""
        url = reverse('api:hello')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello, world!')
    
    def test_status_endpoint(self):
        """Test /api/status/ endpoint"""
        url = reverse('api:status')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'active')
        self.assertEqual(response.data['version'], 'v1')
        self.assertEqual(response.data['message'], 'API is running successfully')
    
    def test_endpoint_anonymous(self):
        """Test /api/endpoint/ with anonymous user"""
        url = reverse('api:endpoint')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'This is a test endpoint')
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['user'], 'anonymous')
        self.assertEqual(response.data['is_staff'], False)
        self.assertEqual(response.data['is_superuser'], False)
        self.assertEqual(response.data['example'], [1, 2, 3, 4])
    
    def test_endpoint_authenticated(self):
        """Test /api/endpoint/ with authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:endpoint')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'This is a test endpoint')
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['user'], 'testuser')
        self.assertEqual(response.data['is_staff'], False)
        self.assertEqual(response.data['is_superuser'], False)
    
    def test_public_endpoint(self):
        """Test /api/public/ endpoint"""
        url = reverse('api:public')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'This is a public endpoint')
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['access'], 'public')


@pytest.mark.django_db
class TestAPIEndpointsPytest:
    """Pytest-style tests for API endpoints"""
    
    def test_hello_endpoint_pytest(self, client):
        """Test /api/hello/ endpoint using pytest"""
        url = reverse('api:hello')
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.json()['message'] == 'Hello, world!'
    
    def test_status_endpoint_pytest(self, client):
        """Test /api/status/ endpoint using pytest"""
        url = reverse('api:status')
        response = client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'active'
        assert data['version'] == 'v1'
        assert data['message'] == 'API is running successfully'
    
    def test_endpoint_pytest(self, client):
        """Test /api/endpoint/ endpoint using pytest"""
        url = reverse('api:endpoint')
        response = client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'This is a test endpoint'
        assert data['status'] == 'success'
        assert data['user'] == 'anonymous'
        assert data['example'] == [1, 2, 3, 4]