import pytest
import django
from django.conf import settings

# Configure Django settings before importing models
if not settings.configured:
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
    django.setup()

# Now safe to import Django models
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Fixture for DRF API client"""
    return APIClient()


@pytest.fixture
def test_user():
    """Fixture for creating a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Fixture for authenticated API client"""
    api_client.force_authenticate(user=test_user)
    return api_client