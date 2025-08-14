# -*- encoding: utf-8 -*-
"""
Facility models for GVRC Admin
Integrated with enhanced features from facility_project
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils import timezone
from apps.common.models import TimeStampedModel
from decimal import Decimal


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)


class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    county_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'counties'
        verbose_name_plural = 'Counties'
    
    def __str__(self):
        return self.county_name


class Constituency(models.Model):
    constituency_id = models.AutoField(primary_key=True)
    constituency_name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='constituencies')
    
    class Meta:
        db_table = 'constituencies'
        verbose_name_plural = 'Constituencies'
    
    def __str__(self):
        return self.constituency_name


class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True)
    ward_name = models.CharField(max_length=100)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, related_name='wards')
    
    class Meta:
        db_table = 'wards'
    
    def __str__(self):
        return self.ward_name


class OperationalStatus(models.Model):
    operational_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'operational_statuses'
        verbose_name_plural = 'Operational Statuses'
    
    def __str__(self):
        return self.status_name


class ContactType(models.Model):
    contact_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'contact_types'
    
    def __str__(self):
        return self.type_name


class ServiceCategory(models.Model):
    service_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'service_categories'
        verbose_name_plural = 'Service Categories'
    
    def __str__(self):
        return self.category_name


class OwnerType(models.Model):
    owner_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'owner_types'
    
    def __str__(self):
        return self.type_name


class DocumentType(models.Model):
    document_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'document_types'
        verbose_name_plural = 'Document Types'
    
    def __str__(self):
        return self.type_name


class AuthenticationMethod(models.Model):
    auth_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'authentication_methods'
        verbose_name_plural = 'Authentication Methods'
    
    def __str__(self):
        return self.method_name


class GbvCategory(models.Model):
    gbv_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'gbv_categories'
        verbose_name_plural = 'GBV Categories'
    
    def __str__(self):
        return self.category_name


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    facility = models.ForeignKey('Facility', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    # Override AbstractUser fields
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name or self.email


class Facility(TimeStampedModel):
    """Community-based facility model"""
    FACILITY_TYPES = [
        # Health facilities
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('dispensary', 'Dispensary'),
        ('health_center', 'Health Center'),
        ('laboratory', 'Laboratory'),
        ('pharmacy', 'Pharmacy'),
        # Police and security
        ('police_station', 'Police Station'),
        ('police_post', 'Police Post'),
        ('security_office', 'Security Office'),
        # Community organizations
        ('cbo', 'Community-Based Organization (CBO)'),
        ('ngo', 'Non-Governmental Organization (NGO)'),
        ('faith_based', 'Faith-Based Organization'),
        # Support services
        ('safe_house', 'Safe House'),
        ('shelter', 'Shelter'),
        ('legal_aid', 'Legal Aid Center'),
        ('gender_desk', 'Gender Desk'),
        ('counseling_center', 'Counseling Center'),
        ('rehabilitation_center', 'Rehabilitation Center'),
        # Other community facilities
        ('community_center', 'Community Center'),
        ('youth_center', 'Youth Center'),
        ('women_center', 'Women Center'),
        ('elderly_center', 'Elderly Center'),
        ('disability_center', 'Disability Center'),
    ]
    
    OWNERSHIP_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('faith_based', 'Faith-based'),
        ('ngo', 'NGO'),
        ('community', 'Community-owned'),
        ('government', 'Government'),
    ]
    
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=30, choices=FACILITY_TYPES)
    ownership = models.CharField(max_length=20, choices=OWNERSHIP_TYPES)
    county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    location = models.CharField(max_length=200, help_text="Street address or general location description")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Latitude coordinate (e.g., -1.2921)")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Longitude coordinate (e.g., 36.8219)")
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    registration_number = models.CharField(max_length=50, unique=True)
    
    # Additional fields for community facilities
    target_population = models.CharField(max_length=200, blank=True, help_text="Primary target population served")
    services_offered = models.TextField(blank=True, help_text="Brief description of main services")
    operating_hours = models.CharField(max_length=100, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    
    # Enhanced fields from facility_project
    operational_status = models.ForeignKey(OperationalStatus, on_delete=models.PROTECT, related_name='facilities', null=True, blank=True)
    ward_detail = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name='facilities', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_facilities', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_facilities', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_facility_type_display()}"
    
    def get_coordinates(self):
        """Return coordinates as a tuple if both lat and lon are available"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    def get_location_display(self):
        """Return formatted location information"""
        location_parts = []
        if self.county:
            location_parts.append(f"County: {self.county}")
        if self.ward:
            location_parts.append(f"Ward: {self.ward}")
        if self.location:
            location_parts.append(f"Address: {self.location}")
        if self.latitude and self.longitude:
            location_parts.append(f"Coordinates: {self.latitude}, {self.longitude}")
        
        return " | ".join(location_parts) if location_parts else "Location not specified"
    
    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Facilities"


class Facility_Services(TimeStampedModel):
    """Services offered by facilities"""
    SERVICE_CATEGORIES = [
        # Health services
        ('curative', 'Curative Services'),
        ('preventive', 'Preventive Services'),
        ('diagnostic', 'Diagnostic Services'),
        ('rehabilitative', 'Rehabilitative Services'),
        ('support', 'Support Services'),
        # Security and legal services
        ('security', 'Security Services'),
        ('legal', 'Legal Services'),
        ('counseling', 'Counseling Services'),
        ('protection', 'Protection Services'),
        # Community services
        ('education', 'Education Services'),
        ('training', 'Training Services'),
        ('advocacy', 'Advocacy Services'),
        ('emergency', 'Emergency Services'),
        ('referral', 'Referral Services'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.facility.name} - {self.service_name}"
    
    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Facility Services"


class Facility_HumanResources(TimeStampedModel):
    """Human resources at facilities"""
    STAFF_CATEGORIES = [
        # Health staff
        ('medical', 'Medical Staff'),
        ('nursing', 'Nursing Staff'),
        ('pharmacy', 'Pharmacy Staff'),
        ('laboratory', 'Laboratory Staff'),
        # Security staff
        ('police', 'Police Officers'),
        ('security', 'Security Personnel'),
        # Legal and support staff
        ('legal', 'Legal Staff'),
        ('counselor', 'Counselors'),
        ('social_worker', 'Social Workers'),
        ('psychologist', 'Psychologists'),
        # Administrative staff
        ('administrative', 'Administrative Staff'),
        ('support', 'Support Staff'),
        ('volunteer', 'Volunteers'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='staff')
    staff_category = models.CharField(max_length=20, choices=STAFF_CATEGORIES)
    position = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.facility.name} - {self.full_name} ({self.position})"
    
    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Facility Human Resources"


class Facility_Infrastructure(TimeStampedModel):
    """Infrastructure and operational equipment for community facilities"""
    EQUIPMENT_CATEGORIES = [
        # Emergency and medical vehicles
        ('ambulance', 'Ambulance'),
        ('emergency_vehicle', 'Emergency Vehicle'),
        ('medical_transport', 'Medical Transport Vehicle'),
        ('police_vehicle', 'Police Vehicle'),
        ('security_vehicle', 'Security Vehicle'),
        # Medical equipment
        ('medical_equipment', 'Medical Equipment'),
        ('diagnostic_equipment', 'Diagnostic Equipment'),
        ('emergency_equipment', 'Emergency Equipment'),
        ('first_aid_equipment', 'First Aid Equipment'),
        # Communication equipment
        ('communication_equipment', 'Communication Equipment'),
        ('radio_equipment', 'Radio Equipment'),
        ('emergency_communication', 'Emergency Communication'),
        # Security equipment
        ('security_equipment', 'Security Equipment'),
        ('surveillance_equipment', 'Surveillance Equipment'),
        ('safety_equipment', 'Safety Equipment'),
        # IT and office equipment
        ('it_equipment', 'IT Equipment'),
        ('office_equipment', 'Office Equipment'),
        ('data_management', 'Data Management Equipment'),
        # Utilities and infrastructure
        ('power_equipment', 'Power Equipment'),
        ('water_equipment', 'Water Equipment'),
        ('generator', 'Generator'),
        ('backup_systems', 'Backup Systems'),
        # Other operational equipment
        ('furniture', 'Furniture'),
        ('storage_equipment', 'Storage Equipment'),
        ('maintenance_equipment', 'Maintenance Equipment'),
    ]
    
    EQUIPMENT_CONDITIONS = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('non_functional', 'Non-Functional'),
        ('under_maintenance', 'Under Maintenance'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='infrastructure')
    equipment_name = models.CharField(max_length=200, help_text="Name of the equipment or vehicle (e.g., Ambulance, Emergency Radio)")
    category = models.CharField(max_length=30, choices=EQUIPMENT_CATEGORIES)
    quantity = models.PositiveIntegerField(default=1, help_text="Number of units available")
    condition = models.CharField(max_length=20, choices=EQUIPMENT_CONDITIONS, default='good')
    registration_number = models.CharField(max_length=50, blank=True, help_text="Vehicle registration number if applicable")
    model_year = models.PositiveIntegerField(null=True, blank=True, help_text="Year of manufacture")
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True, help_text="Insurance expiry date for vehicles")
    fuel_type = models.CharField(max_length=20, blank=True, help_text="Fuel type for vehicles (e.g., Petrol, Diesel, Electric)")
    capacity = models.CharField(max_length=50, blank=True, help_text="Capacity or specifications (e.g., 4 passengers, 1000W)")
    is_operational = models.BooleanField(default=True, help_text="Whether the equipment is currently operational")
    notes = models.TextField(blank=True, help_text="Additional notes about the equipment")
    
    def __str__(self):
        return f"{self.facility.name} - {self.equipment_name}"
    
    def is_vehicle(self):
        """Check if this is a vehicle type equipment"""
        vehicle_categories = ['ambulance', 'emergency_vehicle', 'medical_transport', 'police_vehicle', 'security_vehicle']
        return self.category in vehicle_categories
    
    def needs_maintenance(self):
        """Check if equipment needs maintenance based on last maintenance date"""
        if self.last_maintenance:
            from datetime import date, timedelta
            # Suggest maintenance every 6 months for vehicles, 12 months for other equipment
            maintenance_interval = timedelta(days=180 if self.is_vehicle() else 365)
            return date.today() - self.last_maintenance > maintenance_interval
        return False
    
    def get_operational_status(self):
        """Get operational status with color coding"""
        if not self.is_operational:
            return "Non-Operational"
        elif self.condition == 'poor' or self.condition == 'non_functional':
            return "Needs Attention"
        elif self.needs_maintenance():
            return "Needs Maintenance"
        else:
            return "Operational"
    
    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Facility Infrastructure"


class FacilityContact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='contacts_new')
    contact_type = models.ForeignKey(ContactType, on_delete=models.PROTECT)
    contact_value = models.CharField(max_length=255)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_contacts'
        unique_together = ['facility', 'contact_type', 'contact_value']
    
    def __str__(self):
        return f"{self.facility.name} - {self.contact_type.type_name}: {self.contact_value}"


class FacilityCoordinate(models.Model):
    coordinate_id = models.AutoField(primary_key=True)
    facility = models.OneToOneField(Facility, on_delete=models.CASCADE, related_name='coordinates')
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    coordinates_string = models.CharField(max_length=100, blank=True, null=True)
    collection_date = models.DateField(auto_now_add=True)
    data_source = models.CharField(max_length=100, blank=True, null=True)
    collection_method = models.CharField(max_length=100, blank=True, null=True)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_coordinates'
    
    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.coordinates_string = f"{self.latitude},{self.longitude}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.facility.name} - ({self.latitude}, {self.longitude})"


class FacilityService(models.Model):
    service_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='services_new')
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT)
    service_description = models.TextField(blank=True, null=True)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_services'
        unique_together = ['facility', 'service_category']
    
    def __str__(self):
        return f"{self.facility.name} - {self.service_category.category_name}"


class FacilityOwner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='owners_new')
    owner_name = models.CharField(max_length=200)
    owner_type = models.ForeignKey(OwnerType, on_delete=models.PROTECT)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_owners'
    
    def __str__(self):
        return f"{self.facility.name} - {self.owner_name}"


class UserLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    captured_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_locations'
    
    def __str__(self):
        return f"{self.user.full_name} - {self.ward.ward_name}"


class UserSession(models.Model):
    session_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'user_sessions'
    
    def __str__(self):
        return f"{self.user.full_name} - {self.session_id[:8]}..."


class UserAuthMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_method = models.ForeignKey(AuthenticationMethod, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_auth_methods'
        unique_together = ['user', 'auth_method']
        verbose_name_plural = 'User Authentication Methods'
    def __str__(self):
        return f"{self.user.full_name} - {self.auth_method.method_name}"


class AccessLevel(models.Model):
    access_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'access_levels'
        verbose_name_plural = 'Access Levels'
    def __str__(self):
        return self.level_name


class UserAccessLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_access_levels'
        unique_together = ['user', 'access_level']
        verbose_name_plural = 'User Access Levels'
    def __str__(self):
        return f"{self.user.full_name} - {self.access_level.level_name}"


class ApiToken(models.Model):
    token_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='api_tokens')
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'api_tokens'
        verbose_name_plural = 'API Tokens'
    def __str__(self):
        return f"Token for {self.session.user.full_name}"


class ResetToken(models.Model):
    reset_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reset_tokens'
        verbose_name_plural = 'Reset Tokens'
    def __str__(self):
        return f"Reset token for {self.user.full_name}"


class ContactClick(models.Model):
    click_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='contact_clicks', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_clicks', null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='contact_clicks')
    contact = models.ForeignKey(FacilityContact, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    helpful = models.BooleanField(default=False)
    followup_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'contact_clicks'
        verbose_name_plural = 'Contact Clicks'
    def __str__(self):
        return f"Click on {self.contact.contact_value} for {self.facility.name}"


class FacilityGbvCategory(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    gbv_category = models.ForeignKey(GbvCategory, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'facility_gbv_categories'
        unique_together = ['facility', 'gbv_category']
        verbose_name_plural = 'Facility GBV Categories'
    def __str__(self):
        return f"{self.facility.name} - {self.gbv_category.category_name}"


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file_url = models.URLField(max_length=500)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='documents')
    gbv_category = models.ForeignKey(GbvCategory, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'documents'
        verbose_name_plural = 'Documents'
    def __str__(self):
        return self.title
