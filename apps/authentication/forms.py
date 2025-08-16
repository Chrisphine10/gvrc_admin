# -*- encoding: utf-8 -*-
"""
Authentication forms for custom User model
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, ResetToken
import hashlib
import secrets
from django.utils import timezone
from datetime import timedelta


class LoginForm(forms.Form):
    """Custom login form for email-based authentication"""
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email, is_active=True)
                # For now, we'll use simple password hashing - in production, use proper password hashing
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                if user.password_hash != password_hash:
                    raise ValidationError("Invalid email or password.")
                self.user = user
            except User.DoesNotExist:
                raise ValidationError("Invalid email or password.")
        
        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)


class SignUpForm(forms.ModelForm):
    """Custom registration form for the User model"""
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number')
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    "placeholder": "Full Name",
                    "class": "form-control"
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "form-control"
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    "placeholder": "Phone Number",
                    "class": "form-control"
                }
            ),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone_number
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password - in production, use Django's built-in password hashing
        password = self.cleaned_data["password1"]
        user.password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if commit:
            user.save()
        return user


class PasswordResetRequestForm(forms.Form):
    """Form to request password reset"""
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
            self.user = user
        except User.DoesNotExist:
            raise ValidationError("No user found with this email address.")
        return email
    
    def get_user(self):
        return getattr(self, 'user', None)
    
    def create_reset_token(self):
        """Create a password reset token"""
        user = self.get_user()
        if user:
            # Deactivate any existing tokens
            ResetToken.objects.filter(user=user, used=False).update(used=True)
            
            # Create new token
            token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            
            reset_token = ResetToken.objects.create(
                user=user,
                token_hash=token_hash,
                created_at=timezone.now(),
                expires_at=timezone.now() + timedelta(hours=24),
                used=False
            )
            
            return token, reset_token
        return None, None


class PasswordResetConfirmForm(forms.Form):
    """Form to confirm password reset"""
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm New Password",
                "class": "form-control"
            }
        ))
    
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', None)
        super().__init__(*args, **kwargs)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def clean(self):
        cleaned_data = super().clean()
        if self.token:
            token_hash = hashlib.sha256(self.token.encode()).hexdigest()
            try:
                reset_token = ResetToken.objects.get(
                    token_hash=token_hash,
                    used=False,
                    expires_at__gt=timezone.now()
                )
                self.reset_token = reset_token
            except ResetToken.DoesNotExist:
                raise ValidationError("Invalid or expired reset token.")
        else:
            raise ValidationError("No reset token provided.")
        
        return cleaned_data
    
    def save(self):
        """Save the new password and mark token as used"""
        if hasattr(self, 'reset_token'):
            user = self.reset_token.user
            password = self.cleaned_data['password1']
            user.password_hash = hashlib.sha256(password.encode()).hexdigest()
            user.save()
            
            # Mark token as used
            self.reset_token.used = True
            self.reset_token.save()
            
            return user
        return None