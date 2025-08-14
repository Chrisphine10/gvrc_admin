import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal

from facilities.models import (
    County, Constituency, Ward, Facility, FacilityContact,
    FacilityCoordinate, FacilityService, OperationalStatus,
    ContactType, ServiceCategory
)

User = get_user_model()


class ModelTestCase(TestCase):
    """Test cases for models"""
    
    def setUp(self):
        self.county = County.objects.create(county_name="Test County")
        self.constituency = Constituency.objects.create(
            constituency_name="Test Constituency",
            county=self.county
        )
        self.ward = Ward.objects.create(
            ward_name="Test Ward",
            constituency=self.constituency
        )
        self.operational_status = OperationalStatus.objects.create(
            status_name="Operational"
        )
        self.user = User.objects.create_user(
            email="test@example.com",
            full_name="Test User",
            password="testpass123"
        )

    def test_county_creation(self):
        """Test county model creation"""
        self.assertEqual(str(self.county), "Test County")
        self.assertEqual(self.county.county_name, "Test County")

    def test_constituency_creation(self):
        """Test constituency model creation"""
        self.assertEqual(str(self.constituency), "Test Constituency")
        self.assertEqual(self.constituency.county, self.county)

    def test_ward_creation(self):
        """Test ward model creation"""
        self.assertEqual(str(self.ward), "Test Ward")
        self.assertEqual(self.ward.constituency, self.constituency)

    def test_user_creation(self):
        """Test user model creation"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.full_name, "Test User")
        self.assertTrue(self.user.check_password("testpass123"))

    def test_facility_creation(self):
        """Test facility model creation"""
        facility = Facility.objects.create(
            facility_name="Test Hospital",
            registration_number="REG123",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        self.assertEqual(str(facility), "Test Hospital")
        self.assertEqual(facility.ward, self.ward)
        self.assertEqual(facility.created_by, self.user)

    def test_facility_coordinate_creation(self):
        """Test facility coordinate model"""
        facility = Facility.objects.create(
            facility_name="Test Hospital",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        coordinate = FacilityCoordinate.objects.create(
            facility=facility,
            latitude=Decimal("-1.2921"),
            longitude=Decimal("36.8219")
        )
        
        self.assertEqual(coordinate.facility, facility)
        self.assertEqual(coordinate.coordinates_string, "-1.2921,36.8219")


class APITestCase(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test data
        self.county = County.objects.create(county_name="Test County")
        self.constituency = Constituency.objects.create(
            constituency_name="Test Constituency",
            county=self.county
        )
        self.ward = Ward.objects.create(
            ward_name="Test Ward",
            constituency=self.constituency
        )
        self.operational_status = OperationalStatus.objects.create(
            status_name="Operational"
        )
        self.contact_type = ContactType.objects.create(type_name="Phone")
        self.service_category = ServiceCategory.objects.create(
            category_name="General Medicine"
        )
        
        # Create test user
        self.user = User.objects.create_user(
            email="test@example.com",
            full_name="Test User",
            password="testpass123"
        )
        
        # Create token for authentication
        self.token = Token.objects.create(user=self.user)

    def authenticate(self):
        """Helper method to authenticate requests"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('api:register')
        data = {
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'phone_number': '1234567890',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_login(self):
        """Test user login endpoint"""
        url = reverse('api:login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_facility_list_authenticated(self):
        """Test facility list endpoint with authentication"""
        self.authenticate()
        
        # Create test facility
        facility = Facility.objects.create(
            facility_name="Test Hospital",
            registration_number="REG123",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        url = reverse('api:facility-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_facility_list_unauthenticated(self):
        """Test facility list endpoint without authentication"""
        url = reverse('api:facility-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_facility_creation(self):
        """Test facility creation endpoint"""
        self.authenticate()
        
        url = reverse('api:facility-list-create')
        data = {
            'facility_name': 'New Hospital',
            'registration_number': 'REG456',
            'operational_status': self.operational_status.operational_status_id,
            'ward': self.ward.ward_id,
            'active_status': True
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['facility_name'], 'New Hospital')

    def test_facility_detail(self):
        """Test facility detail endpoint"""
        self.authenticate()
        
        facility = Facility.objects.create(
            facility_name="Test Hospital",
            registration_number="REG123",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        url = reverse('api:facility-detail', kwargs={'facility_id': facility.facility_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['facility_name'], 'Test Hospital')

    def test_facility_search(self):
        """Test facility search endpoint"""
        self.authenticate()
        
        # Create test facilities
        facility1 = Facility.objects.create(
            facility_name="General Hospital",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        facility2 = Facility.objects.create(
            facility_name="Specialist Clinic",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        url = reverse('api:facility-search')
        
        # Search by name
        response = self.client.get(url, {'q': 'General'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['facility_name'], 'General Hospital')

    def test_facility_contact_creation(self):
        """Test facility contact creation"""
        self.authenticate()
        
        facility = Facility.objects.create(
            facility_name="Test Hospital",
            operational_status=self.operational_status,
            ward=self.ward,
            created_by=self.user
        )
        
        url = reverse('api:facility-contact-list-create', kwargs={'facility_id': facility.facility_id})
        data = {
            'facility': facility.facility_id,
            'contact_type': self.contact_type.contact_type_id,
            'contact_value': '+254712345678',
            'active_status': True
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contact_value'], '+254712345678')

    def test_user_profile(self):
        """Test user profile endpoint"""
        self.authenticate()
        
        url = reverse('api:user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_counties_list(self):
        """Test counties list endpoint"""
        self.authenticate()
        
        url = reverse('api:county-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['county_name'], 'Test County')

    def test_constituencies_by_county(self):
        """Test constituencies filtered by county"""
        self.authenticate()
        
        url = reverse('api:constituency-list')
        response = self.client.get(url, {'county': self.county.county_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['constituency_name'], 'Test Constituency')

    def test_wards_by_constituency(self):
        """Test wards filtered by constituency"""
        self.authenticate()
        
        url = reverse('api:ward-list')
        response = self.client.get(url, {'constituency': self.constituency.constituency_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ward_name'], 'Test Ward')


class FacilityFilterTestCase(APITestCase):
    """Test cases for facility filtering and searching"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test data
        self.county1 = County.objects.create(county_name="County A")
        self.county2 = County.objects.create(county_name="County B")
        
        self.constituency1 = Constituency.objects.create(
            constituency_name="Constituency A",
            county=self.county1
        )
        
        self.ward1 = Ward.objects.create(
            ward_name="Ward A",
            constituency=self.constituency1
        )
        
        self.operational_status = OperationalStatus.objects.create(
            status_name="Operational"
        )
        
        self.user = User.objects.create_user(
            email="test@example.com",
            full_name="Test User",
            password="testpass123"
        )
        
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_facility_filter_by_county(self):
        """Test filtering facilities by county"""
        # Create facilities in different counties
        facility1 = Facility.objects.create(
            facility_name="Hospital A",
            operational_status=self.operational_status,
            ward=self.ward1,
            created_by=self.user
        )
        
        url = reverse('api:facility-search')
        response = self.client.get(url, {'county': self.county1.county_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_facility_filter_by_status(self):
        """Test filtering facilities by operational status"""
        closed_status = OperationalStatus.objects.create(status_name="Closed")
        
        facility1 = Facility.objects.create(
            facility_name="Open Hospital",
            operational_status=self.operational_status,
            ward=self.ward1,
            created_by=self.user
        )
        
        facility2 = Facility.objects.create(
            facility_name="Closed Hospital",
            operational_status=closed_status,
            ward=self.ward1,
            created_by=self.user
        )
        
        url = reverse('api:facility-list-create')
        response = self.client.get(url, {'operational_status': self.operational_status.operational_status_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should only return operational facility
        facility_names = [f['facility_name'] for f in response.data['results']]
        self.assertIn("Open Hospital", facility_names)
        self.assertNotIn("Closed Hospital", facility_names)


# Pytest fixtures and tests
@pytest.fixture
def user():
    return User.objects.create_user(
        email="pytest@example.com",
        full_name="Pytest User",
        password="testpass123"
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client


@pytest.mark.django_db
def test_user_creation(user):
    """Pytest test for user creation"""
    assert user.email == "pytest@example.com"
    assert user.full_name == "Pytest User"
    assert user.check_password("testpass123")


@pytest.mark.django_db
def test_facility_api_requires_auth(api_client):
    """Pytest test for authentication requirement"""
    url = reverse('api:facility-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_facility_creation_api(authenticated_client, user):
    """Pytest test for facility creation through API"""
    # Create required objects
    county = County.objects.create(county_name="Test County")
    constituency = Constituency.objects.create(
        constituency_name="Test Constituency",
        county=county
    )
    ward = Ward.objects.create(
        ward_name="Test Ward",
        constituency=constituency
    )
    operational_status = OperationalStatus.objects.create(
        status_name="Operational"
    )
    
    url = reverse('api:facility-list-create')
    data = {
        'facility_name': 'Pytest Hospital',
        'registration_number': 'PYTEST123',
        'operational_status': operational_status.operational_status_id,
        'ward': ward.ward_id,
        'active_status': True
    }
    
    response = authenticated_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['facility_name'] == 'Pytest Hospital'
    assert Facility.objects.count() == 1