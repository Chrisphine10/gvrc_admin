# -*- encoding: utf-8 -*-
"""
Forms for facilities app
"""

from django import forms
from .models import Facility, FacilityContact, FacilityService, FacilityOwner, FacilityCoordinate, FacilityGBVCategory
from apps.common.geography import County, Constituency, Ward
from apps.common.lookups import OperationalStatus, ContactType, ServiceCategory, OwnerType, GBVCategory


class FacilityForm(forms.ModelForm):
    """Form for creating and updating facilities"""
    
    class Meta:
        model = Facility
        fields = ['facility_name', 'registration_number', 'operational_status', 'ward']
        widgets = {
            'facility_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter facility name'
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
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facility_name'].help_text = 'Full name of the facility'
        self.fields['registration_number'].help_text = 'Unique registration number'
        self.fields['operational_status'].help_text = 'Current operational status'
        self.fields['ward'].help_text = 'Administrative ward where facility is located'
        
        # Make all fields required
        for field_name, field in self.fields.items():
            field.required = True
            
        # Set empty label for select fields
        self.fields['operational_status'].empty_label = "Select operational status"
        self.fields['ward'].empty_label = "Select ward"


class FacilityContactForm(forms.ModelForm):
    """Form for facility contact information"""
    
    class Meta:
        model = FacilityContact
        fields = ['contact_type', 'contact_value']
        widgets = {
            'contact_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'contact_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact information'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_type'].empty_label = "Select contact type"
        self.fields['contact_value'].help_text = 'Phone number, email, website, etc.'


class FacilityServiceForm(forms.ModelForm):
    """Form for facility services"""
    
    class Meta:
        model = FacilityService
        fields = ['service_category', 'service_description']
        widgets = {
            'service_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'service_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the service offered'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_category'].empty_label = "Select service category"
        self.fields['service_description'].required = False


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
    extra=1, 
    min_num=1,  # Ensure at least one form
    max_num=5,
    can_delete=True,
    validate_min=True  # Validate minimum number of forms
)

FacilityServiceFormSet = formset_factory(
    FacilityServiceForm, 
    extra=1, 
    min_num=1,  # Ensure at least one form
    max_num=10,
    can_delete=True,
    validate_min=True  # Validate minimum number of forms
)

FacilityOwnerFormSet = formset_factory(
    FacilityOwnerForm, 
    extra=1, 
    min_num=1,  # Ensure at least one form
    max_num=3,
    can_delete=True,
    validate_min=True  # Validate minimum number of forms
)
