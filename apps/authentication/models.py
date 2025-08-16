# -*- encoding: utf-8 -*-
"""
Authentication and user management models
"""

from django.db import models
from apps.common.models import TimeStampedModel
from apps.facilities.models import Facility
from apps.common.geography import Ward


class User(TimeStampedModel):
    """User model for system access"""
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True, db_column='facility_id')
    
    # Django admin required fields
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into the admin site.")
    is_superuser = models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.")
    username = models.CharField(max_length=150, unique=True, null=True, blank=True, help_text="Username for admin access")
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    class Meta:
        db_table = 'users'


class UserLocation(TimeStampedModel):
    """User location tracking"""
    location_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    ward = models.ForeignKey('common.Ward', on_delete=models.CASCADE, db_column='ward_id', null=True, blank=True)
    captured_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.full_name} - {self.ward.ward_name} at {self.captured_at}"
    
    class Meta:
        db_table = 'user_locations'


class AuthenticationMethod(models.Model):
    """Available authentication methods"""
    auth_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.method_name
    
    class Meta:
        db_table = 'authentication_methods'


class UserAuthMethod(models.Model):
    """Many-to-many relationship between users and authentication methods"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    auth_method = models.ForeignKey(AuthenticationMethod, on_delete=models.CASCADE, db_column='auth_id')
    
    class Meta:
        db_table = 'user_auth_methods'
        unique_together = ('user', 'auth_method')


class AccessLevel(models.Model):
    """Available access levels"""
    access_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.level_name
    
    class Meta:
        db_table = 'access_levels'


class UserAccessLevel(models.Model):
    """Many-to-many relationship between users and access levels"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, db_column='access_id')
    
    class Meta:
        db_table = 'user_access_levels'
        unique_together = ('user', 'access_level')


class UserSession(models.Model):
    """User session tracking"""
    session_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.full_name} - {self.session_id}"
    
    class Meta:
        db_table = 'user_sessions'


class ApiToken(models.Model):
    """API token management"""
    token_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, db_column='session_id')
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Token for {self.session.user.full_name}"
    
    class Meta:
        db_table = 'api_tokens'


class ResetToken(models.Model):
    """Password reset token management"""
    reset_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reset token for {self.user.full_name}"
    
    class Meta:
        db_table = 'reset_tokens'


class ContactClick(models.Model):
    """Contact click tracking"""
    click_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, db_column='session_id', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    facility = models.ForeignKey('facilities.Facility', on_delete=models.CASCADE, db_column='facility_id', null=True, blank=True)
    contact = models.ForeignKey('facilities.FacilityContact', on_delete=models.CASCADE, db_column='contact_id', null=True, blank=True)
    clicked_at = models.DateTimeField()
    helpful = models.BooleanField(null=True, blank=True)
    followup_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name} clicked {self.contact.contact_type.type_name} at {self.facility.facility_name}"
    
    class Meta:
        db_table = 'contact_clicks'


class CustomToken(models.Model):
    """
    Custom API token model for our custom User model
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name='auth_token', on_delete=models.CASCADE, db_column='user_id')
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            import secrets
            self.key = secrets.token_hex(20)  # 40 character hex token
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Token for {self.user.full_name}"
    
    class Meta:
        db_table = 'custom_tokens'
