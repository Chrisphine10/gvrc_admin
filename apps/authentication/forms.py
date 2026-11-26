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
        # Never say whether the address has an account: that told anyone which
        # emails belong to Hodi staff. The view answers the same either way.
        email = self.cleaned_data.get('email')
        self.user = User.objects.filter(email__iexact=email, is_active=True).first()
        return email

    def get_user(self):
        return getattr(self, 'user', None)

    def create_reset_token(self):
        """A signed, single-use token "<uidb64>.<token>" for the URL.

        Django's token generator hashes the user's current password and last
        login into the token, so it stops working once the password changes,
        and expires after PASSWORD_RESET_TIMEOUT (3 days by default).
        """
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        user = self.get_user()
        if not user:
            return None, None
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        return f"{uidb64}.{default_token_generator.make_token(user)}", True


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
        self.user = self.user_for_token(self.token)
        super().__init__(*args, **kwargs)

    @staticmethod
    def user_for_token(token):
        """The user a "<uidb64>.<token>" string is valid for, else None."""
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        if not token or '.' not in token:
            return None
        uidb64, _, raw = token.partition('.')
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)), is_active=True)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return None
        return user if default_token_generator.check_token(user, raw) else None

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        if not self.user:
            raise ValidationError("This reset link is invalid or has expired. Please request a new one.")
        password = cleaned_data.get("password1")
        if password:
            from django.contrib.auth.password_validation import validate_password
            try:
                validate_password(password, self.user)
            except ValidationError as exc:
                self.add_error("password1", exc)
        return cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save(update_fields=["password"])
        return self.user


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


class StaffUserCreateForm(forms.ModelForm):
    """Administrators add staff here. No password: the new person gets a
    one-time "set your password" link by email and SMS, so nobody else ever
    knows it."""

    role = forms.ModelChoiceField(
        queryset=None, required=False, empty_label="No role yet",
        help_text="What this person can see and do. You can change it later.",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "phone_number", "is_staff")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "0712345678"}),
        }
        help_texts = {
            "email": "The sign-in name. The set-password link is emailed here.",
            "phone_number": "A Kenyan mobile number: the set-password link and chat alerts are sent here by SMS.",
            "is_staff": "Staff can be assigned help chats.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import UserRole
        self.fields["role"].queryset = UserRole.objects.order_by("role_name")
        self.fields["is_staff"].initial = True

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self):
        from apps.sms.services import is_sendable_phone, normalize_phone
        phone = (self.cleaned_data.get("phone_number") or "").strip()
        if not is_sendable_phone(phone):
            raise ValidationError("Enter a Kenyan mobile number, e.g. 0712345678.")
        phone = "+" + normalize_phone(phone)
        if User.objects.filter(phone_number__in=[phone, phone[1:], "0" + phone[4:]]).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone

    def save(self, commit=True):
        d = self.cleaned_data
        return User.objects.create_user(
            email=d["email"], full_name=d["full_name"].strip(), phone_number=d["phone_number"],
            password=None, is_staff=d.get("is_staff", False),
        )
