# Create your models here.
from django.db import models


# ================================
# Users
# ================================
class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # facility = models.ForeignKey('Facility', on_delete=models.SET_NULL, null=True, blank=True)  # Commented as per requirement

    def __str__(self):
        return self.full_name


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ward = models.ForeignKey("Ward", on_delete=models.CASCADE)
    captured_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.full_name} - {self.ward.ward_name}"


# ================================
# Authentication
# ================================
class AuthenticationMethod(models.Model):
    method_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.method_name


class UserAuthMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth = models.ForeignKey(AuthenticationMethod, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "auth")


class AccessLevel(models.Model):
    level_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.level_name


class UserAccessLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "access")


# ================================
# Sessions & Tokens
# ================================
class UserSession(models.Model):
    session_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Session {self.session_id} - {self.user.full_name}"


class APIToken(models.Model):
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class ResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)


# ================================
# Click Tracking
# ================================
class ContactClick(models.Model):
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # facility = models.ForeignKey('Facility', on_delete=models.CASCADE)  # Commented as per requirement
    contact = models.ForeignKey("FacilityContact", on_delete=models.CASCADE)
    clicked_at = models.DateTimeField()
    helpful = models.BooleanField(default=False)
    followup_at = models.DateTimeField(blank=True, null=True)
