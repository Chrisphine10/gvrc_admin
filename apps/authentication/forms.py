# -*- encoding: utf-8 -*-
"""
Authentication forms for custom User model
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, UserProfile
from django.utils import timezone
from datetime import timedelta
import logging

# Set up logger for forms
logger = logging.getLogger(__name__)


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
                # Log authentication attempt
                logger.debug(f"Attempting authentication for email: {email}")
                
                # Use Django's authenticate function with our custom backend
                user = authenticate(email=email, password=password)
                
                if user is None:
                    logger.warning(f"Authentication failed for email: {email} - Invalid credentials")
                    raise ValidationError("Invalid email or password.")
                
                # Check if user is active
                if not user.is_active:
                    logger.warning(f"Authentication failed for email: {email} - Account inactive")
                    raise ValidationError("Your account has been deactivated. Please contact an administrator.")
                
                # Check if user is staff (for admin access)
                if not user.is_staff:
                    logger.info(f"Non-staff user authenticated: {email}")
                
                logger.info(f"Authentication successful for email: {email}")
                self.user = user
                
            except ValidationError:
                # Re-raise validation errors
                raise
            except Exception as e:
                logger.error(f"Unexpected error during authentication for {email}: {str(e)}")
                raise ValidationError("An error occurred during authentication. Please try again.")
        
        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)


class SignUpForm(UserCreationForm):
    """Custom registration form for the User model"""
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    
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
        # Set username to email for compatibility
        user.username = user.email
        
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
        """Create a password reset token - placeholder for future implementation"""
        user = self.get_user()
        if user:
            # TODO: Implement password reset token functionality with new schema
            # For now, return a placeholder
            return None, None
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
            # TODO: Implement token validation with new schema
            # For now, just pass validation
            pass
        else:
            raise ValidationError("No reset token provided.")
        
        return cleaned_data
    
    def save(self):
        """Save the new password - placeholder for future implementation"""
        # TODO: Implement password reset functionality with new schema
        return None


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile information"""
    
    # User model fields
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Full Name",
                "class": "form-control"
            }
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        )
    )
    
    # UserProfile model fields
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us about yourself...",
                "class": "form-control",
                "rows": 3
            }
        )
    )
    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Department",
                "class": "form-control"
            }
        )
    )
    job_title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Job Title",
                "class": "form-control"
            }
        )
    )
    avatar_url = forms.URLField(
        max_length=500,
        required=False,
        widget=forms.URLInput(
            attrs={
                "placeholder": "Avatar URL (optional)",
                "class": "form-control"
            }
        )
    )
    
    class Meta:
        model = User
        fields = ['full_name', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize profile fields if they exist
        if self.instance and hasattr(self.instance, 'userprofile'):
            try:
                profile = self.instance.userprofile
                self.fields['bio'].initial = profile.bio
                self.fields['department'].initial = profile.department
                self.fields['job_title'].initial = profile.job_title
                self.fields['avatar_url'].initial = profile.avatar_url
            except UserProfile.DoesNotExist:
                # Profile doesn't exist yet, will be created on save
                pass
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Check if phone number is already taken by another user
            existing_user = User.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise ValidationError("This phone number is already in use by another user.")
        return phone_number
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Save or update UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bio = self.cleaned_data.get('bio', '')
            profile.department = self.cleaned_data.get('department', '')
            profile.job_title = self.cleaned_data.get('job_title', '')
            profile.avatar_url = self.cleaned_data.get('avatar_url', '')
            profile.save()
        
        return user


class PasswordChangeForm(forms.Form):
    """Form for changing user password"""
    
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Current Password",
                "class": "form-control"
            }
        )
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control"
            }
        )
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm New Password",
                "class": "form-control"
            }
        )
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError("Your current password is incorrect.")
        return current_password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        return password2
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            # Basic password validation
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if password.isdigit():
                raise ValidationError("Password cannot be entirely numeric.")
        return password
    
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user