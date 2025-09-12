# -*- encoding: utf-8 -*-
"""
Views for facilities app
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.db import transaction
from django.conf import settings
from django.core.paginator import Paginator
from apps.authentication.permissions import (
    permission_required, role_required, any_role_required,
    staff_required, superuser_required
)
from .models import Facility, FacilityContact, FacilityService, FacilityOwner, FacilityCoordinate, FacilityGBVCategory, FacilityInfrastructure
from .forms import (
    FacilityForm, FacilityContactForm, FacilityServiceForm, FacilityOwnerForm, 
    FacilityCoordinateForm, FacilityGBVCategoryForm, FacilityContactFormSet,
    FacilityServiceFormSet, FacilityOwnerFormSet, FacilityInfrastructureFormSet
)
from apps.geography.models import County
from apps.lookups.models import OperationalStatus, ServiceCategory


# @permission_required('view_facilities')  # Temporarily disabled for testing
def facility_list(request):
    """List all facilities with comprehensive data"""
    # Get base queryset with all related data
    facilities = Facility.objects.select_related(
        'ward__constituency__county', 
        'operational_status'
    ).prefetch_related(
        'facilityservice_set__service_category',
        'facilitycontact_set__contact_type',
        'facilityowner_set__owner_type',
        'facilitygbvcategory_set__gbv_category',
        'facilitycoordinate_set'
    ).filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        facilities = facilities.filter(
            Q(facility_name__icontains=search_query) |
            Q(registration_number__icontains=search_query) |
            Q(ward__ward_name__icontains=search_query) |
            Q(ward__constituency__constituency_name__icontains=search_query) |
            Q(ward__constituency__county__county_name__icontains=search_query)
        )
    
    # Filter by county
    county_id = request.GET.get('county')
    if county_id:
        facilities = facilities.filter(ward__constituency__county_id=county_id)
    
    # Filter by operational status
    status_id = request.GET.get('status')
    if status_id:
        facilities = facilities.filter(operational_status_id=status_id)
    
    # Get statistics
    operational_facilities_count = facilities.filter(operational_status__status_name='Operational').count()
    counties_count = County.objects.count()
    wards_count = facilities.values('ward').distinct().count()
    
    # Add pagination
    paginator = Paginator(facilities, 50)  # Show 50 facilities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    counties = County.objects.all().order_by('county_name')
    operational_statuses = OperationalStatus.objects.all().order_by('status_name')
    service_categories = ServiceCategory.objects.all().order_by('category_name')
    
    context = {
        'facilities': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_county': county_id,
        'selected_status': status_id,
        'operational_facilities_count': operational_facilities_count,
        'counties_count': counties_count,
        'wards_count': wards_count,
        'counties': counties,
        'operational_statuses': operational_statuses,
        'service_categories': service_categories,
        'segment': 'facilities',
    }
    
    return render(request, 'facilities/facility_list.html', context)


@permission_required('view_facilities')
def facility_detail(request, facility_id):
    """Show facility details with all related data"""
    facility = get_object_or_404(
        Facility.objects.select_related(
            'ward__constituency__county', 
            'operational_status'
        ).prefetch_related(
            'facilityservice_set__service_category',
            'facilitycontact_set__contact_type',
            'facilityowner_set__owner_type',
            'facilitygbvcategory_set__gbv_category',
            'facilitycoordinate_set'
        ), 
        facility_id=facility_id, 
        is_active=True
    )
    
    # Get related data efficiently
    contacts = facility.facilitycontact_set.filter(is_active=True)
    services = facility.facilityservice_set.filter(is_active=True)
    owners = facility.facilityowner_set.all()
    infrastructure = facility.facilityinfrastructure_set.filter(is_active=True)
    coordinates = facility.facilitycoordinate_set.first()
    
    context = {
        'facility': facility,
        'contacts': contacts,
        'services': services,
        'owners': owners,
        'infrastructure': infrastructure,
        'coordinates': coordinates,
        'segment': 'facilities',
    }
    
    return render(request, 'facilities/facility_detail.html', context)


@permission_required('view_facilities')
def facility_map(request):
    """Show facilities on a map with coordinates"""
    facilities = Facility.objects.filter(
        is_active=True
    ).select_related(
        'ward__constituency__county',
        'operational_status'
    ).prefetch_related(
        'facilitycoordinate_set'
    )
    
    # Filter facilities with coordinates and serialize for JavaScript
    facilities_with_coords = []
    for facility in facilities:
        coords = facility.facilitycoordinate_set.filter(is_active=True).first()
        if coords and coords.latitude and coords.longitude:
            facilities_with_coords.append({
                'facility': {
                    'facility_id': facility.facility_id,
                    'facility_name': facility.facility_name,
                    'registration_number': facility.registration_number,
                    'ward': {
                        'ward_name': facility.ward.ward_name,
                        'constituency': {
                            'county': {
                                'county_name': facility.ward.constituency.county.county_name
                            }
                        }
                    },
                    'operational_status': {
                        'status_name': facility.operational_status.status_name
                    }
                },
                'coordinates': {
                    'latitude': float(coords.latitude),
                    'longitude': float(coords.longitude)
                }
            })
    
    import json
    
    context = {
        'facilities_with_coords': facilities_with_coords,
        'facilities_with_coords_json': json.dumps(facilities_with_coords),
        'total_facilities': facilities.count(),
        'facilities_with_coords_count': len(facilities_with_coords),
        'segment': 'facility_map',
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    
    return render(request, 'facilities/facility_map.html', context)


@permission_required('add_facilities')
def facility_create(request):
    """Create a new facility with all related data"""
    if request.method == 'POST':
        facility_form = FacilityForm(request.POST)
        coordinate_form = FacilityCoordinateForm(request.POST)
        gbv_form = FacilityGBVCategoryForm(request.POST)
        contact_formset = FacilityContactFormSet(request.POST, prefix='contacts')
        service_formset = FacilityServiceFormSet(request.POST, prefix='services')
        owner_formset = FacilityOwnerFormSet(request.POST, prefix='owners')
        infrastructure_formset = FacilityInfrastructureFormSet(request.POST, prefix='infrastructure')
        
        if (facility_form.is_valid() and coordinate_form.is_valid() and 
            gbv_form.is_valid() and contact_formset.is_valid() and 
            service_formset.is_valid() and owner_formset.is_valid() and
            infrastructure_formset.is_valid()):
            
            try:
                with transaction.atomic():
                    # Create facility
                    facility = facility_form.save(commit=False)
                    
                    # Set ward based on geography selection
                    if facility_form.cleaned_data.get('ward'):
                        facility.ward = facility_form.cleaned_data['ward']
                    elif (facility_form.cleaned_data.get('county') and 
                          facility_form.cleaned_data.get('constituency')):
                        # If ward is not selected but county and constituency are, 
                        # we need to find or create the appropriate ward
                        # For now, we'll require ward selection
                        messages.error(request, 'Please select a ward for the facility.')
                        raise ValueError('Ward selection required')
                    
                    if request.user.is_authenticated:
                        facility.created_by = request.user.user_id
                    facility.save()
                    
                    # Save coordinates if provided
                    if coordinate_form.cleaned_data.get('latitude') and coordinate_form.cleaned_data.get('longitude'):
                        coordinate = coordinate_form.save(commit=False)
                        coordinate.facility = facility
                        if request.user.is_authenticated:
                            coordinate.created_by = request.user.user_id
                        coordinate.save()
                    
                    # Save GBV categories
                    gbv_categories = gbv_form.cleaned_data.get('gbv_categories', [])
                    for category in gbv_categories:
                        FacilityGBVCategory.objects.create(
                            facility=facility,
                            gbv_category=category
                        )
                    
                    # Save contacts
                    for contact_form in contact_formset:
                        if contact_form.cleaned_data and not contact_form.cleaned_data.get('DELETE', False):
                            contact = contact_form.save(commit=False)
                            contact.facility = facility
                            if request.user.is_authenticated:
                                contact.created_by = request.user.user_id
                            contact.save()
                    
                    # Save services
                    for service_form in service_formset:
                        if service_form.cleaned_data and not service_form.cleaned_data.get('DELETE', False):
                            service = service_form.save(commit=False)
                            service.facility = facility
                            if request.user.is_authenticated:
                                service.created_by = request.user.user_id
                            service.save()
                    
                    # Save owners
                    for owner_form in owner_formset:
                        if owner_form.cleaned_data and not owner_form.cleaned_data.get('DELETE', False):
                            owner = owner_form.save(commit=False)
                            owner.facility = facility
                            if request.user.is_authenticated:
                                owner.created_by = request.user.user_id
                            owner.save()
                    
                    # Save infrastructure
                    for infrastructure_form in infrastructure_formset:
                        if (infrastructure_form.cleaned_data and 
                            not infrastructure_form.cleaned_data.get('DELETE', False)):
                            try:
                                infrastructure = infrastructure_form.save(commit=False)
                                infrastructure.facility = facility
                                if request.user.is_authenticated:
                                    infrastructure.created_by = request.user.user_id
                                infrastructure.save()
                            except Exception as e:
                                # Log error but don't fail the entire operation
                                print(f"Error saving infrastructure: {e}")
                                continue
                    
                    messages.success(request, f'Facility "{facility.facility_name}" created successfully!')
                    return redirect('facilities:facility_list')
                    
            except Exception as e:
                messages.error(request, f'Error creating facility: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        facility_form = FacilityForm()
        coordinate_form = FacilityCoordinateForm()
        gbv_form = FacilityGBVCategoryForm()
        contact_formset = FacilityContactFormSet(prefix='contacts')
        service_formset = FacilityServiceFormSet(prefix='services')
        owner_formset = FacilityOwnerFormSet(prefix='owners')
        infrastructure_formset = FacilityInfrastructureFormSet(prefix='infrastructure')
    
    context = {
        'facility_form': facility_form,
        'coordinate_form': coordinate_form,
        'gbv_form': gbv_form,
        'contact_formset': contact_formset,
        'service_formset': service_formset,
        'owner_formset': owner_formset,
        'infrastructure_formset': infrastructure_formset,
        'form_action': 'Create',
        'page_title': 'Create New Facility',
        'segment': 'facilities',
        'google_places_api_key': settings.GOOGLE_PLACES_API_KEY,
    }
    
    return render(request, 'facilities/facility_form.html', context)


@permission_required('change_facilities')
def facility_update(request, facility_id):
    """Update an existing facility with all related data"""
    facility = get_object_or_404(Facility, facility_id=facility_id, is_active=True)
    
    # Get existing related objects
    existing_coordinate = facility.facilitycoordinate_set.first()
    existing_contacts = facility.facilitycontact_set.filter(is_active=True)
    existing_services = facility.facilityservice_set.filter(is_active=True)
    existing_owners = facility.facilityowner_set.all()
    existing_infrastructure = facility.facilityinfrastructure_set.filter(is_active=True)
    
    if request.method == 'POST':
        facility_form = FacilityForm(request.POST, instance=facility)
        coordinate_form = FacilityCoordinateForm(request.POST, instance=existing_coordinate)
        gbv_form = FacilityGBVCategoryForm(request.POST, facility=facility)
        contact_formset = FacilityContactFormSet(request.POST, prefix='contacts')
        service_formset = FacilityServiceFormSet(request.POST, prefix='services')
        owner_formset = FacilityOwnerFormSet(request.POST, prefix='owners')
        infrastructure_formset = FacilityInfrastructureFormSet(request.POST, prefix='infrastructure')
        
        if (facility_form.is_valid() and coordinate_form.is_valid() and 
            gbv_form.is_valid() and contact_formset.is_valid() and 
            service_formset.is_valid() and owner_formset.is_valid() and
            infrastructure_formset.is_valid()):
            
            try:
                with transaction.atomic():
                    # Update facility
                    facility = facility_form.save(commit=False)
                    
                    # Set ward based on geography selection
                    if facility_form.cleaned_data.get('ward'):
                        facility.ward = facility_form.cleaned_data['ward']
                    elif (facility_form.cleaned_data.get('county') and 
                          facility_form.cleaned_data.get('constituency')):
                        # If ward is not selected but county and constituency are, 
                        # we need to find or create the appropriate ward
                        # For now, we'll require ward selection
                        messages.error(request, 'Please select a ward for the facility.')
                        raise ValueError('Ward selection required')
                    
                    if request.user.is_authenticated:
                        facility.updated_by = request.user.user_id
                    facility.save()
                    
                    # Update or create coordinates
                    if coordinate_form.cleaned_data.get('latitude') and coordinate_form.cleaned_data.get('longitude'):
                        if existing_coordinate:
                            coordinate = coordinate_form.save(commit=False)
                            if request.user.is_authenticated:
                                coordinate.updated_by = request.user.user_id
                            coordinate.save()
                        else:
                            coordinate = coordinate_form.save(commit=False)
                            coordinate.facility = facility
                            if request.user.is_authenticated:
                                coordinate.created_by = request.user.user_id
                            coordinate.save()
                    
                    # Update GBV categories
                    # Remove existing categories
                    facility.facilitygbvcategory_set.all().delete()
                    # Add new categories
                    gbv_categories = gbv_form.cleaned_data.get('gbv_categories', [])
                    for category in gbv_categories:
                        FacilityGBVCategory.objects.create(
                            facility=facility,
                            gbv_category=category
                        )
                    
                    # Mark existing related objects as inactive (soft delete)
                    existing_contacts.update(is_active=False)
                    existing_services.update(is_active=False)
                    # Delete existing owners (they don't have is_active field)
                    existing_owners.delete()
                    existing_infrastructure.update(is_active=False)
                    
                    # Save new contacts
                    for contact_form in contact_formset:
                        if contact_form.cleaned_data and not contact_form.cleaned_data.get('DELETE', False):
                            contact = contact_form.save(commit=False)
                            contact.facility = facility
                            if request.user.is_authenticated:
                                contact.created_by = request.user.user_id
                            contact.save()
                    
                    # Save new services
                    for service_form in service_formset:
                        if service_form.cleaned_data and not service_form.cleaned_data.get('DELETE', False):
                            service = service_form.save(commit=False)
                            service.facility = facility
                            if request.user.is_authenticated:
                                service.created_by = request.user.user_id
                            service.save()
                    
                    # Save new owners
                    for owner_form in owner_formset:
                        if owner_form.cleaned_data and not owner_form.cleaned_data.get('DELETE', False):
                            owner = owner_form.save(commit=False)
                            owner.facility = facility
                            if request.user.is_authenticated:
                                owner.created_by = request.user.user_id
                            owner.save()
                    
                    # Save new infrastructure
                    for infrastructure_form in infrastructure_formset:
                        if (infrastructure_form.cleaned_data and 
                            not infrastructure_form.cleaned_data.get('DELETE', False)):
                            try:
                                infrastructure = infrastructure_form.save(commit=False)
                                infrastructure.facility = facility
                                if request.user.is_authenticated:
                                    infrastructure.created_by = request.user.user_id
                                infrastructure.save()
                            except Exception as e:
                                # Log error but don't fail the entire operation
                                print(f"Error saving infrastructure: {e}")
                                continue
                    
                    messages.success(request, f'Facility "{facility.facility_name}" updated successfully!')
                    return redirect('facilities:facility_list')
                    
            except Exception as e:
                messages.error(request, f'Error updating facility: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        facility_form = FacilityForm(instance=facility)
        coordinate_form = FacilityCoordinateForm(instance=existing_coordinate)
        gbv_form = FacilityGBVCategoryForm(facility=facility)
        
        # Populate formsets with existing data
        contact_initial = [
            {'contact_type': contact.contact_type, 'contact_value': contact.contact_value, 
             'contact_person_name': contact.contact_person_name, 'is_primary': contact.is_primary}
            for contact in existing_contacts
        ]
        service_initial = [
            {'service_category': service.service_category, 'service_name': service.service_name,
             'service_description': service.service_description, 'is_free': service.is_free,
             'cost_range': service.cost_range, 'currency': service.currency,
             'availability_hours': service.availability_hours, 'availability_days': service.availability_days,
             'appointment_required': service.appointment_required}
            for service in existing_services
        ]
        owner_initial = [
            {'owner_name': owner.owner_name, 'owner_type': owner.owner_type}
            for owner in existing_owners
        ]
        infrastructure_initial = [
            {'infrastructure_type': infra.infrastructure_type, 'condition_status': infra.condition_status,
             'description': infra.description, 'capacity': infra.capacity,
             'current_utilization': infra.current_utilization, 'is_available': infra.is_available}
            for infra in existing_infrastructure
        ] if existing_infrastructure.exists() else []
        
        contact_formset = FacilityContactFormSet(prefix='contacts', initial=contact_initial)
        service_formset = FacilityServiceFormSet(prefix='services', initial=service_initial)
        owner_formset = FacilityOwnerFormSet(prefix='owners', initial=owner_initial)
        infrastructure_formset = FacilityInfrastructureFormSet(prefix='infrastructure', initial=infrastructure_initial)
    
    context = {
        'facility': facility,
        'facility_form': facility_form,
        'coordinate_form': coordinate_form,
        'gbv_form': gbv_form,
        'contact_formset': contact_formset,
        'service_formset': service_formset,
        'owner_formset': owner_formset,
        'infrastructure_formset': infrastructure_formset,
        'form_action': 'Update',
        'page_title': f'Edit {facility.facility_name}',
        'segment': 'facilities',
        'google_places_api_key': settings.GOOGLE_PLACES_API_KEY,
    }
    
    return render(request, 'facilities/facility_form.html', context)
