# -*- encoding: utf-8 -*-
"""
API Serializers for GVRC Admin
"""

from rest_framework import serializers
from apps.facilities.models import (
    Facility, FacilityContact, FacilityService, 
    FacilityOwner, FacilityCoordinate, FacilityGBVCategory, FacilityInfrastructure
)
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import (
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


class ConsolidatedGeographySerializer(serializers.ModelSerializer):
    """Consolidated geography serializer that includes counties with nested constituencies and wards"""
    constituencies = serializers.SerializerMethodField()
    
    class Meta:
        model = County
        fields = ['county_id', 'county_name', 'county_code', 'constituencies']
    
    def get_constituencies(self, obj):
        """Get constituencies for this county with nested wards"""
        constituencies = obj.constituency_set.all().prefetch_related('ward_set').order_by('constituency_name')
        constituency_data = []
        
        for constituency in constituencies:
            constituency_dict = {
                'constituency_id': constituency.constituency_id,
                'constituency_name': constituency.constituency_name,
                'constituency_code': constituency.constituency_code,
                'wards': []
            }
            
            # Get wards for this constituency
            wards = constituency.ward_set.all().order_by('ward_name')
            for ward in wards:
                ward_dict = {
                    'ward_id': ward.ward_id,
                    'ward_name': ward.ward_name,
                    'ward_code': ward.ward_code
                }
                constituency_dict['wards'].append(ward_dict)
            
            constituency_data.append(constituency_dict)
        
        return constituency_data


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
            'collection_date', 'data_source', 'collection_method',
            'created_at', 'updated_at'
        ]


class FacilityContactSerializer(serializers.ModelSerializer):
    """Facility contact serializer"""
    contact_type = ContactTypeSerializer(read_only=True)
    
    class Meta:
        model = FacilityContact
        fields = [
            'contact_id', 'contact_type', 'contact_value', 'contact_person_name', 
            'is_primary', 'is_active', 'created_at', 'updated_at'
        ]


class FacilityServiceSerializer(serializers.ModelSerializer):
    """Facility service serializer"""
    service_category = ServiceCategorySerializer(read_only=True)
    
    class Meta:
        model = FacilityService
        fields = [
            'service_id', 'service_name', 'service_category', 'service_description',
            'is_free', 'cost_range', 'currency', 'availability_hours', 
            'availability_days', 'appointment_required', 'is_active',
            'created_at', 'updated_at'
        ]


class FacilityOwnerSerializer(serializers.ModelSerializer):
    """Facility owner serializer"""
    owner_type = OwnerTypeSerializer(read_only=True)
    
    class Meta:
        model = FacilityOwner
        fields = ['owner_id', 'owner_name', 'owner_type', 'created_at', 'updated_at']


class FacilityGBVCategorySerializer(serializers.ModelSerializer):
    """Facility GBV category serializer"""
    gbv_category = GBVCategorySerializer(read_only=True)
    
    class Meta:
        model = FacilityGBVCategory
        fields = ['gbv_category', 'created_at']


class FacilityInfrastructureSerializer(serializers.ModelSerializer):
    """Facility infrastructure serializer"""
    infrastructure_type = serializers.SerializerMethodField()
    condition_status = serializers.SerializerMethodField()
    
    class Meta:
        model = FacilityInfrastructure
        fields = [
            'infrastructure_id', 'infrastructure_type', 'condition_status', 
            'description', 'capacity', 'current_utilization', 'is_available',
            'created_at', 'updated_at'
        ]
    
    def get_infrastructure_type(self, obj):
        """Get infrastructure type information"""
        if obj.infrastructure_type:
            return {
                'type_id': obj.infrastructure_type.infrastructure_type_id,
                'type_name': obj.infrastructure_type.type_name,
                'description': obj.infrastructure_type.description
            }
        return None
    
    def get_condition_status(self, obj):
        """Get condition status information"""
        if obj.condition_status:
            return {
                'status_id': obj.condition_status.condition_status_id,
                'status_name': obj.condition_status.status_name,
                'description': obj.condition_status.description
            }
        return None


class FacilityListSerializer(serializers.ModelSerializer):
    """Facility list serializer for mobile app optimization"""
    ward = WardSerializer(read_only=True)
    operational_status = OperationalStatusSerializer(read_only=True)
    coordinates = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'facility_name', 'registration_number',
            'ward', 'operational_status', 'coordinates',
            'services', 'contacts'
        ]
    
    def get_coordinates(self, obj):
        """Get facility coordinates if available"""
        coords = obj.facilitycoordinate_set.filter(is_active=True).first()
        if coords and coords.latitude and coords.longitude:
            return {
                'latitude': float(coords.latitude),
                'longitude': float(coords.longitude)
            }
        return None
    
    def get_services(self, obj):
        """Get active facility services using prefetched queryset"""
        # Use prefetched queryset if available, otherwise fallback to regular queryset
        if hasattr(obj, 'active_services'):
            services = obj.active_services
        else:
            services = obj.facilityservice_set.filter(is_active=True).select_related('service_category')
        
        return FacilityServiceSerializer(services, many=True).data
    
    def get_contacts(self, obj):
        """Get active facility contacts using prefetched queryset"""
        # Use prefetched queryset if available, otherwise fallback to regular queryset
        if hasattr(obj, 'active_contacts'):
            contacts = obj.active_contacts
        else:
            contacts = obj.facilitycontact_set.filter(is_active=True).select_related('contact_type')
        
        return FacilityContactSerializer(contacts, many=True).data


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
        coords = obj.facilitycoordinate_set.filter(is_active=True).first()
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


class MobileAppFacilitySerializer(serializers.ModelSerializer):
    """Simplified facility serializer for mobile app with all essential information"""
    ward = WardSerializer(read_only=True)
    operational_status = OperationalStatusSerializer(read_only=True)
    coordinates = FacilityCoordinateSerializer(source='facilitycoordinate_set.first', read_only=True)
    contacts = FacilityContactSerializer(source='facilitycontact_set', many=True, read_only=True)
    services = FacilityServiceSerializer(source='facilityservice_set', many=True, read_only=True)
    owners = FacilityOwnerSerializer(source='facilityowner_set', many=True, read_only=True)
    gbv_categories = FacilityGBVCategorySerializer(source='facilitygbvcategory_set', many=True, read_only=True)
    infrastructure = FacilityInfrastructureSerializer(source='facilityinfrastructure_set', many=True, read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'facility_id', 'facility_name', 'facility_code', 'registration_number',
            'ward', 'operational_status', 'coordinates', 'contacts', 'services',
            'owners', 'gbv_categories', 'infrastructure', 'address_line_1', 
            'address_line_2', 'description', 'website_url', 'is_active',
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Custom representation to filter active items and handle coordinates"""
        data = super().to_representation(instance)
        
        # Filter active contacts
        if data.get('contacts'):
            data['contacts'] = [contact for contact in data['contacts'] if contact.get('is_active', True)]
        
        # Filter active services
        if data.get('services'):
            data['services'] = [service for service in data['services'] if service.get('is_active', True)]
        
        # Filter active infrastructure
        if data.get('infrastructure'):
            data['infrastructure'] = [infra for infra in data['infrastructure'] if infra.get('is_available', True)]
        
        # Handle coordinates - get the first valid coordinate
        if data.get('coordinates') is None:
            coords = instance.facilitycoordinate_set.filter(
                latitude__isnull=False, 
                longitude__isnull=False
            ).first()
            if coords:
                data['coordinates'] = FacilityCoordinateSerializer(coords).data
        
        return data
    

    



class MusicSerializer(serializers.ModelSerializer):
    """Music serializer for mobile app"""
    class Meta:
        model = None  # Will be set dynamically
        fields = [
            'music_id', 'name', 'description', 'link', 'music_file',
            'artist', 'duration', 'genre', 'is_active', 'created_at'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        try:
            from apps.music.models import Music
            self.Meta.model = Music
        except ImportError:
            pass


class DocumentSerializer(serializers.ModelSerializer):
    """Document serializer for mobile app"""
    class Meta:
        model = None  # Will be set dynamically
        fields = [
            'document_id', 'title', 'description', 'file_url', 'file_name',
            'file_size_bytes', 'content', 'gbv_category', 'image_url',
            'external_url', 'document_type', 'is_public', 'is_active',
            'uploaded_at'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        try:
            from apps.documents.models import Document
            self.Meta.model = Document
        except ImportError:
            pass


class MobileSessionSerializer(serializers.ModelSerializer):
    """Mobile session serializer for device management"""
    class Meta:
        model = None  # Will be set dynamically
        fields = [
            'device_id', 'notification_enabled', 'dark_mode_enabled',
            'preferred_language', 'latitude', 'longitude', 'location_updated_at',
            'location_permission_granted', 'is_active', 'last_active_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        try:
            from apps.mobile_sessions.models import MobileSession
            self.Meta.model = MobileSession
        except ImportError:
            pass


class MobileSessionCreateSerializer(serializers.Serializer):
    """Serializer for creating new mobile sessions"""
    device_id = serializers.CharField(max_length=128, help_text="Device UUID")
    notification_enabled = serializers.BooleanField(default=True, help_text="Whether notifications are enabled")
    dark_mode_enabled = serializers.BooleanField(default=False, help_text="Whether dark mode is enabled")
    preferred_language = serializers.CharField(max_length=5, default='en-US', help_text="Preferred language code")
    latitude = serializers.DecimalField(max_digits=10, decimal_places=8, required=False, help_text="Device latitude")
    longitude = serializers.DecimalField(max_digits=11, decimal_places=8, required=False, help_text="Device longitude")
    location_permission_granted = serializers.BooleanField(default=False, help_text="Whether location permission is granted")


class MobileSessionUpdateSerializer(serializers.Serializer):
    """Serializer for updating mobile sessions"""
    notification_enabled = serializers.BooleanField(required=False, help_text="Whether notifications are enabled")
    dark_mode_enabled = serializers.BooleanField(required=False, help_text="Whether dark mode is enabled")
    preferred_language = serializers.CharField(max_length=5, required=False, help_text="Preferred language code")
    latitude = serializers.DecimalField(max_digits=10, decimal_places=8, required=False, help_text="Device latitude")
    longitude = serializers.DecimalField(max_digits=11, decimal_places=8, required=False, help_text="Device longitude")
    location_permission_granted = serializers.BooleanField(required=False, help_text="Whether location permission is granted")


class EmergencySOSSerializer(serializers.Serializer):
    """Emergency SOS serializer for urgent situations"""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    emergency_type = serializers.CharField(max_length=100, required=True, help_text="Type of emergency")
    description = serializers.CharField(max_length=500, required=False, help_text="Emergency description")
    user_id = serializers.IntegerField(required=False, help_text="User ID if available")
    device_id = serializers.CharField(max_length=255, required=False, help_text="Device identifier")
    radius_km = serializers.IntegerField(default=5, help_text="Search radius in kilometers")


class PaginatedResponseSerializer(serializers.Serializer):
    """Generic paginated response serializer"""
    count = serializers.IntegerField(help_text="Total number of items")
    next = serializers.CharField(allow_null=True, help_text="URL for next page")
    previous = serializers.CharField(allow_null=True, help_text="URL for previous page")
    results = serializers.ListField(help_text="List of items for current page")