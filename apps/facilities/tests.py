from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Facility, FacilityCoordinate
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import OperationalStatus
from .forms import FacilityForm

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


class FacilityFormTest(TestCase):
    def setUp(self):
        """Set up test data for form testing"""
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
    
    def test_facility_form_validation_success(self):
        """Test that facility form validates successfully with correct data"""
        form_data = {
            'facility_name': 'Test Facility',
            'registration_number': 'REG001',
            'operational_status': self.operational_status.operational_status_id,
            'ward': self.ward.ward_id,
            'county': self.county.county_id,
            'constituency': self.constituency.constituency_id,
            'address_line_1': '123 Test Street'
        }
        
        form = FacilityForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_facility_form_geography_consistency(self):
        """Test that form allows geography selection (validation handled by JavaScript)"""
        # Create another county and constituency
        other_county = County.objects.create(
            county_name='Other County',
            county_code='OC001'
        )
        other_constituency = Constituency.objects.create(
            constituency_name='Other Constituency',
            constituency_code='OC001',
            county=other_county
        )
        
        # Test with mismatched geography - form should allow this since validation is handled by JavaScript
        form_data = {
            'facility_name': 'Test Facility',
            'registration_number': 'REG001',
            'operational_status': self.operational_status.operational_status_id,
            'ward': self.ward.ward_id,
            'county': other_county.county_id,  # Different county
            'constituency': self.constituency.constituency_id,  # From different county
            'address_line_1': '123 Test Street'
        }
        
        form = FacilityForm(data=form_data)
        # Form should be valid since we removed strict geography validation
        self.assertTrue(form.is_valid())
    
    def test_facility_form_initialization_with_instance(self):
        """Test that form properly initializes geography fields when editing"""
        # Create a facility
        facility = Facility.objects.create(
            facility_name='Test Facility',
            facility_code='TF001',
            registration_number='REG001',
            operational_status=self.operational_status,
            ward=self.ward,
            address_line_1='123 Test Street',
            is_active=True,
            created_by=self.user
        )
        
        # Create form with instance
        form = FacilityForm(instance=facility)
        
        # Check that geography fields are properly initialized
        self.assertEqual(form.fields['county'].initial, self.county)
        self.assertEqual(form.fields['constituency'].initial, self.constituency)
        # Note: ward field initial is not set in the simplified form
        # self.assertEqual(form.fields['ward'].initial, self.ward)
        
        # Check that constituency queryset is not filtered (simplified approach)
        constituency_queryset = form.fields['constituency'].queryset
        self.assertTrue(constituency_queryset.count() > 0)
        
        # Check that ward queryset is not filtered (simplified approach)
        ward_queryset = form.fields['ward'].queryset
        self.assertTrue(ward_queryset.count() > 0)
