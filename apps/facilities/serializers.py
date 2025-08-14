from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import (
    User, Facility, FacilityContact, FacilityCoordinate, 
    FacilityService, FacilityOwner, UserLocation, UserSession,
    County, Constituency, Ward, OperationalStatus, ContactType,
    ServiceCategory, OwnerType, DocumentType, AuthenticationMethod,
    GbvCategory, UserAuthMethod, AccessLevel, UserAccessLevel,
    ApiToken, ResetToken, ContactClick, FacilityGbvCategory, Document
)


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class ConstituencySerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.county_name', read_only=True)
    
    class Meta:
        model = Constituency
        fields = ['constituency_id', 'constituency_name', 'county', 'county_name']


class WardSerializer(serializers.ModelSerializer):
    constituency_name = serializers.CharField(source='constituency.constituency_name', read_only=True)
    county_name = serializers.CharField(source='constituency.county.county_name', read_only=True)
    
    class Meta:
        model = Ward
        fields = ['ward_id', 'ward_name', 'constituency', 'constituency_name', 'county_name']


class OperationalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalStatus
        fields = '__all__'


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = '__all__'


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class OwnerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerType
        fields = '__all__'


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'


class AuthenticationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationMethod
        fields = '__all__'


class GbvCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GbvCategory
        fields = '__all__'


class UserLocationSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source='ward.ward_name', read_only=True)
    constituency_name = serializers.CharField(source='ward.constituency.constituency_name', read_only=True)
    county_name = serializers.CharField(source='ward.constituency.county.county_name', read_only=True)
    
    class Meta:
        model = UserLocation
        fields = ['location_id', 'user', 'ward', 'ward_name', 'constituency_name', 'county_name', 'captured_at']


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = '__all__'
        read_only_fields = ['session_id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    locations = UserLocationSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'email', 'phone_number', 'password',
            'created_at', 'updated_at', 'is_active', 'facility', 'facility_name',
            'locations'
        ]
        read_only_fields = ['user_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password_hash = make_password(password)
        user.set_password(password)  # This sets the proper Django password
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.password_hash = make_password(password)
            instance.set_password(password)
        
        instance.save()
        return instance


class FacilityContactSerializer(serializers.ModelSerializer):
    contact_type_name = serializers.CharField(source='contact_type.type_name', read_only=True)
    
    class Meta:
        model = FacilityContact
        fields = [
            'contact_id', 'facility', 'contact_type', 'contact_type_name',
            'contact_value', 'active_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['contact_id', 'created_at', 'updated_at']


class FacilityCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityCoordinate
        fields = [
            'coordinate_id', 'facility', 'latitude', 'longitude', 'coordinates_string',
            'collection_date', 'data_source', 'collection_method', 'active_status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['coordinate_id', 'coordinates_string', 'created_at', 'updated_at']


class FacilityServiceSerializer(serializers.ModelSerializer):
    service_category_name = serializers.CharField(source='service_category.category_name', read_only=True)
    
    class Meta:
        model = FacilityService
        fields = [
            'service_id', 'facility', 'service_category', 'service_category_name',
            'service_description', 'active_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['service_id', 'created_at', 'updated_at']


class FacilityOwnerSerializer(serializers.ModelSerializer):
    owner_type_name = serializers.CharField(source='owner_type.type_name', read_only=True)
    
    class Meta:
        model = FacilityOwner
        fields = [
            'owner_id', 'facility', 'owner_name', 'owner_type', 'owner_type_name',
            'active_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner_id', 'created_at', 'updated_at']


class FacilitySerializer(serializers.ModelSerializer):
    operational_status_name = serializers.CharField(source='operational_status.status_name', read_only=True)
    ward_name = serializers.CharField(source='ward_detail.ward_name', read_only=True)
    constituency_name = serializers.CharField(source='ward_detail.constituency.constituency_name', read_only=True)
    county_name = serializers.CharField(source='ward_detail.constituency.county.county_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    
    # Nested serializers
    contacts = FacilityContactSerializer(many=True, read_only=True, source='contacts_new')
    coordinates = FacilityCoordinateSerializer(read_only=True)
    services = FacilityServiceSerializer(many=True, read_only=True, source='services_new')
    owners = FacilityOwnerSerializer(many=True, read_only=True, source='owners_new')
    users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'id', 'name', 'facility_type', 'ownership', 'county', 'ward',
            'location', 'latitude', 'longitude', 'contact_person', 'phone', 'email',
            'is_active', 'registration_number', 'target_population', 'services_offered',
            'operating_hours', 'emergency_contact', 'operational_status', 'operational_status_name',
            'ward_detail', 'ward_name', 'constituency_name', 'county_name',
            'created_at', 'created_by', 'created_by_name',
            'updated_by', 'updated_by_name', 'contacts', 'coordinates',
            'services', 'owners', 'users'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FacilityListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing facilities without nested data"""
    operational_status_name = serializers.CharField(source='operational_status.status_name', read_only=True)
    ward_name = serializers.CharField(source='ward_detail.ward_name', read_only=True)
    constituency_name = serializers.CharField(source='ward_detail.constituency.constituency_name', read_only=True)
    county_name = serializers.CharField(source='ward_detail.constituency.county.county_name', read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'id', 'name', 'facility_type', 'ownership', 'county', 'ward',
            'location', 'latitude', 'longitude', 'contact_person', 'phone', 'email',
            'is_active', 'registration_number', 'target_population', 'services_offered',
            'operating_hours', 'emergency_contact', 'operational_status_name', 'ward_name',
            'constituency_name', 'county_name', 'created_at'
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must include email and password.")
        
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'password_confirm', 'facility']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password_hash = make_password(password)
        user.set_password(password)
        user.save()
        return user


class UserAuthMethodSerializer(serializers.ModelSerializer):
    auth_method_name = serializers.CharField(source='auth_method.method_name', read_only=True)
    
    class Meta:
        model = UserAuthMethod
        fields = ['user', 'auth_method', 'auth_method_name']


class AccessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLevel
        fields = '__all__'


class UserAccessLevelSerializer(serializers.ModelSerializer):
    access_level_name = serializers.CharField(source='access_level.level_name', read_only=True)
    
    class Meta:
        model = UserAccessLevel
        fields = ['user', 'access_level', 'access_level_name']


class ApiTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiToken
        fields = '__all__'
        read_only_fields = ['token_id', 'created_at']


class ResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetToken
        fields = '__all__'
        read_only_fields = ['reset_id', 'created_at']


class ContactClickSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    contact_value = serializers.CharField(source='contact.contact_value', read_only=True)
    
    class Meta:
        model = ContactClick
        fields = [
            'click_id', 'session', 'user', 'facility', 'facility_name', 'contact',
            'contact_value', 'clicked_at', 'helpful', 'followup_at'
        ]
        read_only_fields = ['click_id', 'clicked_at']


class FacilityGbvCategorySerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    gbv_category_name = serializers.CharField(source='gbv_category.category_name', read_only=True)
    
    class Meta:
        model = FacilityGbvCategory
        fields = ['facility', 'facility_name', 'gbv_category', 'gbv_category_name']


class DocumentSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    gbv_category_name = serializers.CharField(source='gbv_category.category_name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.type_name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'document_id', 'title', 'description', 'file_url', 'facility', 'facility_name',
            'gbv_category', 'gbv_category_name', 'document_type', 'document_type_name',
            'uploaded_by', 'uploaded_by_name', 'uploaded_at'
        ]
        read_only_fields = ['document_id', 'uploaded_at']
