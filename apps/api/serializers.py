# -*- encoding: utf-8 -*-
"""
API Serializers for GVRC Admin
"""

from rest_framework import serializers
from apps.facilities.models import (
    Facility, FacilityContact, FacilityService, 
    FacilityOwner, FacilityCoordinate, FacilityGBVCategory
)
from apps.common.geography import County, Constituency, Ward
from apps.common.lookups import (
    OperationalStatus, ContactType, ServiceCategory, 
    OwnerType, GBVCategory
)


class CountySerializer(serializers.ModelSerializer):
    """County serializer for API responses"""
    class Meta:
        model = County
        fields = ['county_id', 'county_name']


class ConstituencySerializer(serializers.ModelSerializer):
    """Constituency serializer for API responses"""
    county = CountySerializer(read_only=True)
    
    class Meta:
        model = Constituency
        fields = ['constituency_id', 'constituency_name', 'county']


class WardSerializer(serializers.ModelSerializer):
    """Ward serializer for API responses"""
    constituency = ConstituencySerializer(read_only=True)
    
    class Meta:
        model = Ward
        fields = ['ward_id', 'ward_name', 'constituency']


class OperationalStatusSerializer(serializers.ModelSerializer):
    """Operational status serializer"""
    class Meta:
        model = OperationalStatus
        fields = ['operational_status_id', 'status_name']


class ContactTypeSerializer(serializers.ModelSerializer):
    """Contact type serializer"""
    class Meta:
        model = ContactType
        fields = ['contact_type_id', 'type_name']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Service category serializer"""
    class Meta:
        model = ServiceCategory
        fields = ['service_category_id', 'category_name']


class OwnerTypeSerializer(serializers.ModelSerializer):
    """Owner type serializer"""
    class Meta:
        model = OwnerType
        fields = ['owner_type_id', 'type_name']


class GBVCategorySerializer(serializers.ModelSerializer):
    """GBV category serializer"""
    class Meta:
        model = GBVCategory
        fields = ['gbv_category_id', 'category_name', 'description']


class FacilityCoordinateSerializer(serializers.ModelSerializer):
    """Facility coordinate serializer"""
    class Meta:
        model = FacilityCoordinate
        fields = [
            'coordinate_id', 'latitude', 'longitude', 
            'coordinates_string', 'collection_date', 
            'data_source', 'collection_method'
        ]


class FacilityContactSerializer(serializers.ModelSerializer):
    """Facility contact serializer"""
    contact_type = ContactTypeSerializer(read_only=True)
    
    class Meta:
        model = FacilityContact
        fields = ['contact_id', 'contact_type', 'contact_value']


class FacilityServiceSerializer(serializers.ModelSerializer):
    """Facility service serializer"""
    service_category = ServiceCategorySerializer(read_only=True)
    
    class Meta:
        model = FacilityService
        fields = ['service_id', 'service_category', 'service_description']


class FacilityOwnerSerializer(serializers.ModelSerializer):
    """Facility owner serializer"""
    owner_type = OwnerTypeSerializer(read_only=True)
    
    class Meta:
        model = FacilityOwner
        fields = ['owner_id', 'owner_name', 'owner_type']


class FacilityGBVCategorySerializer(serializers.ModelSerializer):
    """Facility GBV category serializer"""
    gbv_category = GBVCategorySerializer(read_only=True)
    
    class Meta:
        model = FacilityGBVCategory
        fields = ['gbv_category']


class FacilityListSerializer(serializers.ModelSerializer):
    """Facility list serializer for mobile app optimization"""
    ward = WardSerializer(read_only=True)
    operational_status = OperationalStatusSerializer(read_only=True)
    coordinates = serializers.SerializerMethodField()
    services_count = serializers.SerializerMethodField()
    contacts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'facility_name', 'registration_number',
            'ward', 'operational_status', 'coordinates',
            'services_count', 'contacts_count'
        ]
    
    def get_coordinates(self, obj):
        """Get facility coordinates if available"""
        coords = obj.facilitycoordinate_set.filter(active_status=True).first()
        if coords and coords.latitude and coords.longitude:
            return {
                'latitude': float(coords.latitude),
                'longitude': float(coords.longitude)
            }
        return None
    
    def get_services_count(self, obj):
        """Get count of active services"""
        return obj.facilityservice_set.filter(active_status=True).count()
    
    def get_contacts_count(self, obj):
        """Get count of active contacts"""
        return obj.facilitycontact_set.filter(active_status=True).count()


class FacilityDetailSerializer(serializers.ModelSerializer):
    """Comprehensive facility detail serializer"""
    ward = WardSerializer(read_only=True)
    operational_status = OperationalStatusSerializer(read_only=True)
    coordinates = FacilityCoordinateSerializer(read_only=True)
    contacts = FacilityContactSerializer(many=True, read_only=True)
    services = FacilityServiceSerializer(many=True, read_only=True)
    owners = FacilityOwnerSerializer(many=True, read_only=True)
    gbv_categories = FacilityGBVCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'facility_name', 'registration_number',
            'ward', 'operational_status', 'coordinates',
            'contacts', 'services', 'owners', 'gbv_categories'
        ]


class FacilitySearchSerializer(serializers.Serializer):
    """Facility search parameters serializer"""
    search = serializers.CharField(required=False, help_text="Search query for facility name, registration number, or location")
    county = serializers.IntegerField(required=False, help_text="Filter by county ID")
    constituency = serializers.IntegerField(required=False, help_text="Filter by constituency ID")
    ward = serializers.IntegerField(required=False, help_text="Filter by ward ID")
    status = serializers.IntegerField(required=False, help_text="Filter by operational status ID")
    service_category = serializers.IntegerField(required=False, help_text="Filter by service category ID")
    has_coordinates = serializers.BooleanField(required=False, help_text="Filter facilities with GPS coordinates")
    page = serializers.IntegerField(required=False, default=1, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, default=20, help_text="Number of items per page")


class FacilityMapSerializer(serializers.ModelSerializer):
    """Facility map serializer for mobile app map views"""
    ward = WardSerializer(read_only=True)
    coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'facility_name', 'registration_number',
            'ward', 'coordinates'
        ]
    
    def get_coordinates(self, obj):
        """Get facility coordinates for map display"""
        coords = obj.facilitycoordinate_set.filter(active_status=True).first()
        if coords and coords.latitude and coords.longitude:
            return {
                'latitude': float(coords.latitude),
                'longitude': float(coords.longitude)
            }
        return None


class StatisticsSerializer(serializers.Serializer):
    """Statistics response serializer"""
    total_facilities = serializers.IntegerField()
    operational_facilities = serializers.IntegerField()
    counties_count = serializers.IntegerField()
    constituencies_count = serializers.IntegerField()
    wards_count = serializers.IntegerField()
    facilities_with_coordinates = serializers.IntegerField()
    facilities_by_status = serializers.DictField()
    facilities_by_county = serializers.ListField()


class LookupDataResponseSerializer(serializers.Serializer):
    """Serializer for lookup data endpoint response"""
    counties = CountySerializer(many=True)
    operational_statuses = OperationalStatusSerializer(many=True)
    service_categories = ServiceCategorySerializer(many=True)
    contact_types = ContactTypeSerializer(many=True)
    owner_types = OwnerTypeSerializer(many=True)
    gbv_categories = GBVCategorySerializer(many=True)


class EmergencySearchSerializer(serializers.Serializer):
    """Serializer for emergency SOS search parameters"""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True, help_text="User's current latitude")
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True, help_text="User's current longitude")
    radius_km = serializers.IntegerField(default=10, help_text="Search radius in kilometers")
    service_types = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=['Emergency Services', 'Security Services'],
        help_text="Types of services needed"
    )
    urgent = serializers.BooleanField(default=True, help_text="Whether this is an urgent emergency")


class GBVServiceSearchSerializer(serializers.Serializer):
    """Serializer for GBV-specific service search"""
    gbv_category = serializers.CharField(max_length=100, required=True, help_text="GBV category name")
    service_types = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        help_text="Service types needed"
    )
    county = serializers.IntegerField(required=False, help_text="County ID")
    constituency = serializers.IntegerField(required=False, help_text="Constituency ID")
    ward = serializers.IntegerField(required=False, help_text="Ward ID")
    available_24_7 = serializers.BooleanField(default=False, help_text="Only 24/7 available services")


class ReferralChainSerializer(serializers.Serializer):
    """Serializer for multi-service referral chain requests"""
    case_type = serializers.CharField(max_length=100, required=True, help_text="Type of GBV case")
    location = serializers.DictField(required=True, help_text="Location information (county, ward)")
    immediate_needs = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=True,
        help_text="Immediate service needs"
    )
    followup_needs = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        help_text="Follow-up service needs"
    )


class ContactClickSerializer(serializers.Serializer):
    """Serializer for contact click tracking"""
    facility_id = serializers.IntegerField(required=True, help_text="ID of the facility contacted")
    contact_id = serializers.IntegerField(required=True, help_text="ID of the specific contact used")
    contact_type = serializers.CharField(max_length=50, required=True, help_text="Type of contact (Phone, Email, etc.)")
    helpful = serializers.BooleanField(default=True, help_text="Whether the contact was helpful")
    user_location = serializers.DictField(required=False, help_text="User's location when contact was made")


class ReferralOutcomeSerializer(serializers.Serializer):
    """Serializer for referral outcome tracking"""
    from_facility = serializers.IntegerField(required=True, help_text="ID of facility making the referral")
    to_facility = serializers.IntegerField(required=True, help_text="ID of facility receiving the referral")
    service_accessed = serializers.BooleanField(required=True, help_text="Whether the service was successfully accessed")
    satisfaction_rating = serializers.IntegerField(min_value=1, max_value=5, required=False, help_text="Satisfaction rating (1-5)")
    case_type = serializers.CharField(max_length=100, required=False, help_text="Type of GBV case")
    notes = serializers.CharField(max_length=500, required=False, help_text="Additional notes about the referral")


class FacilityCompleteSerializer(serializers.ModelSerializer):
    """Complete facility serializer with all relations for single request optimization"""
    ward = WardSerializer(read_only=True)
    operational_status = OperationalStatusSerializer(read_only=True)
    coordinates = FacilityCoordinateSerializer(many=True, read_only=True, source='facilitycoordinate_set')
    contacts = FacilityContactSerializer(many=True, read_only=True, source='facilitycontact_set')
    services = FacilityServiceSerializer(many=True, read_only=True, source='facilityservice_set')
    owners = FacilityOwnerSerializer(many=True, read_only=True, source='facilityowner_set')
    gbv_categories = FacilityGBVCategorySerializer(many=True, read_only=True, source='facilitygbvcategory_set')
    recent_clicks = serializers.SerializerMethodField()
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'facility_name', 'registration_number',
            'ward', 'operational_status', 'coordinates',
            'contacts', 'services', 'owners', 'gbv_categories',
            'recent_clicks', 'created_at', 'updated_at'
        ]
    
    def get_recent_clicks(self, obj):
        """Get recent contact clicks for analytics"""
        # This would be implemented with ContactClick model
        return 0  # Placeholder