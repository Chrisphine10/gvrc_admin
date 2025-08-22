# -*- encoding: utf-8 -*-
"""
Forms for facilities app
"""

from django import forms
from .models import Facility, FacilityContact, FacilityService, FacilityOwner, FacilityCoordinate, FacilityGBVCategory, FacilityInfrastructure
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import OperationalStatus, ContactType, ServiceCategory, OwnerType, GBVCategory


class FacilityForm(forms.ModelForm):
    """Form for creating and updating facilities"""
    
    class Meta:
        model = Facility
        fields = ['facility_name', 'facility_code', 'registration_number', 'operational_status', 'ward', 
                 'address_line_1', 'address_line_2', 'description', 'website_url']
        widgets = {
            'facility_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter facility name'
            }),
            'facility_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter facility code (optional)'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter registration number'
            }),
            'operational_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ward': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address_line_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address line 1'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address line 2 (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter facility description'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter website URL (optional)'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facility_name'].help_text = 'Full name of the facility'
        self.fields['facility_code'].help_text = 'Optional unique facility code'
        self.fields['registration_number'].help_text = 'Unique registration number'
        self.fields['operational_status'].help_text = 'Current operational status'
        self.fields['ward'].help_text = 'Administrative ward where facility is located'
        self.fields['address_line_1'].help_text = 'Primary address of the facility'
        self.fields['address_line_2'].help_text = 'Additional address information (optional)'
        self.fields['description'].help_text = 'Detailed description of the facility'
        self.fields['website_url'].help_text = 'Official website URL (optional)'
        
        # Make required fields required
        required_fields = ['facility_name', 'registration_number', 'operational_status', 'ward']
        for field_name, field in self.fields.items():
            field.required = field_name in required_fields
            
        # Set empty label for select fields
        self.fields['operational_status'].empty_label = "Select operational status"
        self.fields['ward'].empty_label = "Select ward"


class FacilityContactForm(forms.ModelForm):
    """Form for facility contact information"""
    
    class Meta:
        model = FacilityContact
        fields = ['contact_type', 'contact_value', 'contact_person_name', 'is_primary']
        widgets = {
            'contact_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'contact_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact information'
            }),
            'contact_person_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact person name (optional)'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_type'].empty_label = "Select contact type"
        self.fields['contact_value'].help_text = 'Phone number, email, website, etc.'
        self.fields['contact_person_name'].help_text = 'Name of the contact person (optional)'
        self.fields['is_primary'].help_text = 'Mark as primary contact for this facility'
        
        # Set required fields
        required_fields = ['contact_type', 'contact_value']
        for field_name, field in self.fields.items():
            field.required = field_name in required_fields


class FacilityServiceForm(forms.ModelForm):
    """Form for facility services"""
    
    class Meta:
        model = FacilityService
        fields = ['service_category', 'service_name', 'service_description', 'is_free', 'cost_range', 
                 'currency', 'availability_hours', 'availability_days', 'appointment_required']
        widgets = {
            'service_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'service_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service name'
            }),
            'service_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the service offered'
            }),
            'is_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'cost_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1000-5000 KES'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'availability_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 8:00 AM - 5:00 PM'
            }),
            'availability_days': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Monday-Friday'
            }),
            'appointment_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_category'].empty_label = "Select service category"
        self.fields['service_name'].help_text = 'Name of the service offered'
        self.fields['service_description'].help_text = 'Detailed description of the service'
        self.fields['is_free'].help_text = 'Check if the service is free of charge'
        self.fields['cost_range'].help_text = 'Cost range if not free (optional)'
        self.fields['currency'].help_text = 'Currency for cost (default: KES)'
        self.fields['availability_hours'].help_text = 'Operating hours for this service'
        self.fields['availability_days'].help_text = 'Days when this service is available'
        self.fields['appointment_required'].help_text = 'Check if appointments are required'
        
        # Set required fields
        required_fields = ['service_category', 'service_name']
        for field_name, field in self.fields.items():
            field.required = field_name in required_fields
            
        # Set currency choices
        self.fields['currency'].choices = [
            ('KES', 'Kenyan Shilling (KES)'),
            ('USD', 'US Dollar (USD)'),
            ('EUR', 'Euro (EUR)'),
        ]


class FacilityOwnerForm(forms.ModelForm):
    """Form for facility ownership"""
    
    class Meta:
        model = FacilityOwner
        fields = ['owner_name', 'owner_type']
        widgets = {
            'owner_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter owner name'
            }),
            'owner_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner_type'].empty_label = "Select owner type"


class FacilityCoordinateForm(forms.ModelForm):
    """Form for facility GPS coordinates"""
    
    class Meta:
        model = FacilityCoordinate
        fields = ['latitude', 'longitude', 'data_source', 'collection_method', 'collection_date']
        widgets = {
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'e.g., -1.286389'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'e.g., 36.817223'
            }),
            'data_source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., GPS device, Google Maps'
            }),
            'collection_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Field survey, Satellite imagery'
            }),
            'collection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].help_text = 'Latitude in decimal degrees'
        self.fields['longitude'].help_text = 'Longitude in decimal degrees'
        self.fields['data_source'].required = False
        self.fields['collection_method'].required = False
        self.fields['collection_date'].required = False


class FacilityInfrastructureForm(forms.ModelForm):
    """Form for facility infrastructure"""
    
    class Meta:
        model = FacilityInfrastructure
        fields = ['infrastructure_type', 'condition_status', 'description', 'capacity', 
                 'current_utilization', 'is_available']
        widgets = {
            'infrastructure_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'condition_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the infrastructure'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 50 people'
            }),
            'current_utilization': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30 people'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['infrastructure_type'].empty_label = "Select infrastructure type"
        self.fields['condition_status'].empty_label = "Select condition status"
        self.fields['description'].help_text = 'Detailed description of the infrastructure'
        self.fields['capacity'].help_text = 'Maximum capacity (optional)'
        self.fields['current_utilization'].help_text = 'Current utilization (optional)'
        self.fields['is_available'].help_text = 'Check if infrastructure is currently available'
        
        # Set required fields
        required_fields = ['infrastructure_type', 'condition_status']
        for field_name, field in self.fields.items():
            field.required = field_name in required_fields


class FacilityGBVCategoryForm(forms.Form):
    """Form for selecting GBV categories"""
    
    gbv_categories = forms.ModelMultipleChoiceField(
        queryset=GBVCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        help_text='Select the GBV categories this facility specializes in'
    )
    
    def __init__(self, *args, **kwargs):
        facility = kwargs.pop('facility', None)
        super().__init__(*args, **kwargs)
        
        if facility:
            # Pre-select existing categories
            existing_categories = facility.facilitygbvcategory_set.values_list('gbv_category', flat=True)
            self.fields['gbv_categories'].initial = existing_categories


# Formsets for handling multiple related objects
from django.forms import formset_factory, modelformset_factory

FacilityContactFormSet = formset_factory(
    FacilityContactForm, 
    extra=0,  # Start with exactly 1 form (from min_num)
    min_num=1,  # Ensure at least one form
    max_num=5,
    can_delete=True,
    validate_min=True  # Validate minimum number of forms
)

FacilityServiceFormSet = formset_factory(
    FacilityServiceForm, 
    extra=0,  # Start with exactly 1 form (from min_num)
    min_num=1,  # Ensure at least one form
    max_num=10,
    can_delete=True,
    validate_min=True  # Validate minimum number of forms
)

FacilityOwnerFormSet = formset_factory(
    FacilityOwnerForm, 
    extra=0,  # Start with exactly 1 form (from min_num)
    min_num=1,  # Ensure at least one form
    max_num=3,
    can_delete=True,
    validate_min=True  # Validate minimum number of forms
)

FacilityInfrastructureFormSet = formset_factory(
    FacilityInfrastructureForm, 
    extra=0,  # Start with exactly 0 forms (from min_num)
    min_num=0,  # Infrastructure is optional
    max_num=10,
    can_delete=True,
    validate_min=False  # Don't validate minimum since infrastructure is optional
)
