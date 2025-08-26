from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Facility, FacilityCoordinate
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import OperationalStatus

User = get_user_model()

class FacilityMapViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            full_name='Test User',
            phone_number='+254700000000',
            password='testpass123'
        )
        
        # Create test county, constituency, and ward
        self.county = County.objects.create(
            county_name='Test County',
            county_code='TC001'
        )
        self.constituency = Constituency.objects.create(
            constituency_name='Test Constituency',
            constituency_code='TC001',
            county=self.county
        )
        self.ward = Ward.objects.create(
            ward_name='Test Ward',
            ward_code='TW001',
            constituency=self.constituency
        )
        
        # Create operational status
        self.operational_status = OperationalStatus.objects.create(
            status_name='Operational',
            description='Fully operational facility',
            sort_order=1
        )
        
        # Create test facility
        self.facility = Facility.objects.create(
            facility_name='Test Facility',
            facility_code='TF001',
            registration_number='REG001',
            operational_status=self.operational_status,
            ward=self.ward,
            address_line_1='123 Test Street',
            is_active=True,
            created_by=self.user
        )
        
        # Create test coordinates
        self.coordinates = FacilityCoordinate.objects.create(
            facility=self.facility,
            latitude=-1.2921,
            longitude=36.8219,
            collection_date='2024-01-01'
        )
        
        # Create client
        self.client = Client()
    
    def test_facility_map_view_requires_login(self):
        """Test that facility map view requires login"""
        url = reverse('facilities:facility_map')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_facility_map_view_with_login(self):
        """Test that facility map view works with login"""
        self.client.login(username='test@example.com', password='testpass123')
        url = reverse('facilities:facility_map')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facilities/facility_map.html')
        
        # Check context data
        self.assertIn('facilities_with_coords', response.context)
        self.assertIn('total_facilities', response.context)
        self.assertIn('facilities_with_coords_count', response.context)
        self.assertIn('google_maps_api_key', response.context)
        
        # Check that facility with coordinates is included
        self.assertEqual(len(response.context['facilities_with_coords']), 1)
        self.assertEqual(response.context['total_facilities'], 1)
        self.assertEqual(response.context['facilities_with_coords_count'], 1)
        
        # Check that Google Maps API key is present
        self.assertIsNotNone(response.context['google_maps_api_key'])
        self.assertTrue(len(response.context['google_maps_api_key']) > 0)
    
    def test_facility_map_view_no_coordinates(self):
        """Test facility map view when no facilities have coordinates"""
        # Delete coordinates
        self.coordinates.delete()
        
        self.client.login(username='test@example.com', password='testpass123')
        url = reverse('facilities:facility_map')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['facilities_with_coords_count'], 0)
        self.assertEqual(response.context['total_facilities'], 1)
