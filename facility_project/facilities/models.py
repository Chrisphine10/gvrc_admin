from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
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


class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    operational_status = models.ForeignKey(OperationalStatus, on_delete=models.PROTECT, related_name='facilities')
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name='facilities')
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_facilities', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_facilities', null=True)
    
    class Meta:
        db_table = 'facilities'
        verbose_name_plural = 'Facilities'
    
    def __str__(self):
        return self.facility_name


class FacilityContact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.ForeignKey(ContactType, on_delete=models.PROTECT)
    contact_value = models.CharField(max_length=255)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_contacts'
        unique_together = ['facility', 'contact_type', 'contact_value']
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.contact_type.type_name}: {self.contact_value}"


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
        return f"{self.facility.facility_name} - ({self.latitude}, {self.longitude})"


class FacilityService(models.Model):
    service_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='services')
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT)
    service_description = models.TextField(blank=True, null=True)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_services'
        unique_together = ['facility', 'service_category']
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.service_category.category_name}"


class FacilityOwner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='owners')
    owner_name = models.CharField(max_length=200)
    owner_type = models.ForeignKey(OwnerType, on_delete=models.PROTECT)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'facility_owners'
    
    def __str__(self):
        return f"{self.facility.facility_name} - {self.owner_name}"


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
        return f"Click on {self.contact.contact_value} for {self.facility.facility_name}"


class FacilityGbvCategory(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    gbv_category = models.ForeignKey(GbvCategory, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'facility_gbv_categories'
        unique_together = ['facility', 'gbv_category']
        verbose_name_plural = 'Facility GBV Categories'
    def __str__(self):
        return f"{self.facility.facility_name} - {self.gbv_category.category_name}"


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