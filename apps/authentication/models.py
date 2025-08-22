# -*- encoding: utf-8 -*-
"""
Authentication and user management models
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password


class UserManager(BaseUserManager):
    """Custom user manager for our User model"""
    
    def create_user(self, email, full_name, phone_number, password=None, **extra_fields):
        """Create and return a regular user"""
        if not email:
            raise ValueError('The Email field must be set')
        if not full_name:
            raise ValueError('The Full Name field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            username=email,  # Set username to email for compatibility
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, phone_number, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, full_name, phone_number, password, **extra_fields)
    
    def get_by_natural_key(self, username):
        """Allow login with email as username"""
        return self.get(email=username)


class UserRole(models.Model):
    """Available user roles"""
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True, null=False)
    description = models.CharField(max_length=255, blank=True)
    is_system_role = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    
    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = 'user_roles'


class Permission(models.Model):
    """Available permissions"""
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=100, unique=True, null=False)
    resource_name = models.CharField(max_length=50, null=False)
    action_name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.action_name} {self.resource_name}"
    
    class Meta:
        db_table = 'permissions'


class RolePermission(models.Model):
    """Many-to-many relationship between roles and permissions"""
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, db_column='role_id', null=False)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='permission_id', null=False)
    granted_at = models.DateTimeField(default=timezone.now, null=False)
    granted_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='role_permissions_granted', db_column='granted_by', null=False)
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'permission')


class User(AbstractBaseUser, PermissionsMixin):
    """User model for system access"""
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    # password_hash field removed - Django's AbstractBaseUser provides 'password' field
    is_active = models.BooleanField(default=True, null=False)
    verified = models.BooleanField(default=False, null=False)
    password_reset_token = models.CharField(max_length=255, blank=True)
    password_changed_at = models.DateTimeField(default=timezone.now, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    # Django admin required fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    
    # Django authentication required fields
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    def get_full_name(self):
        """Return the full name of the user"""
        return self.full_name
    
    def get_short_name(self):
        """Return the short name of the user"""
        return self.full_name.split()[0] if self.full_name else ""
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']
    
    class Meta:
        db_table = 'users'


class UserRoleAssignment(models.Model):
    """Many-to-many relationship between users and roles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', null=False)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, db_column='role_id', null=False)
    assigned_at = models.DateTimeField(default=timezone.now, null=False)
    assigned_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='role_assignments_granted', db_column='assigned_by', null=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'user_role_assignments'
        unique_together = ('user', 'role')


class UserProfile(models.Model):
    """Extended user profile information"""
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id', unique=True, null=False)
    avatar_url = models.CharField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    notification_preferences = models.JSONField(default=dict, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.full_name}"
    
    class Meta:
        db_table = 'user_profiles'


class UserSession(models.Model):
    """User session tracking"""
    session_id = models.CharField(max_length=128, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', null=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    session_data = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    last_activity_at = models.DateTimeField(default=timezone.now, null=False)
    expires_at = models.DateTimeField(null=False)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.session_id}"
    
    class Meta:
        db_table = 'user_sessions'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_active']),
            models.Index(fields=['expires_at']),
        ]





class ApiToken(models.Model):
    """API token management"""
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', null=False)
    token_name = models.CharField(max_length=100, null=False)
    token_hash = models.CharField(max_length=255, unique=True, null=False)
    last_used_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    expires_at = models.DateTimeField(null=False)
    
    def __str__(self):
        return f"Token {self.token_name} for {self.user.full_name}"
    
    class Meta:
        db_table = 'api_tokens'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_active']),
            models.Index(fields=['expires_at']),
        ]


class CustomToken(models.Model):
    """Custom API token model for our custom User model"""
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name='custom_auth_token', on_delete=models.CASCADE, db_column='user_id', null=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            import secrets
            self.key = secrets.token_hex(20)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Token for {self.user.full_name}"
    
    class Meta:
        db_table = 'custom_tokens'
