# -*- encoding: utf-8 -*-
"""
Views for facilities app
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.db import transaction
from .models import Facility, FacilityContact, FacilityService, FacilityOwner, FacilityCoordinate, FacilityGBVCategory
from .forms import (
    FacilityForm, FacilityContactForm, FacilityServiceForm, FacilityOwnerForm, 
    FacilityCoordinateForm, FacilityGBVCategoryForm, FacilityContactFormSet,
    FacilityServiceFormSet, FacilityOwnerFormSet
)
from apps.common.geography import County
from apps.common.lookups import OperationalStatus, ServiceCategory


@login_required
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
        'facilitygbvcategory_set__gbv_category'
    ).filter(active_status=True)
    
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
    
    # Get filter options
    counties = County.objects.all().order_by('county_name')
    operational_statuses = OperationalStatus.objects.all().order_by('status_name')
    service_categories = ServiceCategory.objects.all().order_by('category_name')
    
    context = {
        'facilities': facilities,
        'search_query': search_query,
        'selected_county': county_id,
        'selected_status': status_id,
        'operational_facilities_count': operational_facilities_count,
        'counties_count': counties_count,
        'wards_count': wards_count,
        'counties': counties,
        'operational_statuses': operational_statuses,
        'service_categories': service_categories,
    }
    
    return render(request, 'facilities/facility_list.html', context)


@login_required
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
        active_status=True
    )
    
    # Get related data efficiently
    contacts = facility.facilitycontact_set.filter(active_status=True)
    services = facility.facilityservice_set.filter(active_status=True)
    owners = facility.facilityowner_set.filter(active_status=True)
    coordinates = facility.facilitycoordinate_set.filter(active_status=True).first()
    
    context = {
        'facility': facility,
        'contacts': contacts,
        'services': services,
        'owners': owners,
        'coordinates': coordinates,
    }
    
    return render(request, 'facilities/facility_detail.html', context)


@login_required
def facility_map(request):
    """Show facilities on a map with coordinates"""
    facilities = Facility.objects.filter(
        active_status=True
    ).select_related(
        'ward__constituency__county'
    ).prefetch_related(
        'facilitycoordinate_set'
    )
    
    # Filter facilities with coordinates
    facilities_with_coords = []
    for facility in facilities:
        coords = facility.facilitycoordinate_set.filter(active_status=True).first()
        if coords and coords.latitude and coords.longitude:
            facilities_with_coords.append({
                'facility': facility,
                'coordinates': coords,
            })
    
    context = {
        'facilities_with_coords': facilities_with_coords,
        'total_facilities': facilities.count(),
        'facilities_with_coords_count': len(facilities_with_coords),
    }
    
    return render(request, 'facilities/facility_map.html', context)


@login_required
def facility_create(request):
    """Create a new facility with all related data"""
    if request.method == 'POST':
        facility_form = FacilityForm(request.POST)
        coordinate_form = FacilityCoordinateForm(request.POST)
        gbv_form = FacilityGBVCategoryForm(request.POST)
        contact_formset = FacilityContactFormSet(request.POST, prefix='contacts')
        service_formset = FacilityServiceFormSet(request.POST, prefix='services')
        owner_formset = FacilityOwnerFormSet(request.POST, prefix='owners')
        
        if (facility_form.is_valid() and coordinate_form.is_valid() and 
            gbv_form.is_valid() and contact_formset.is_valid() and 
            service_formset.is_valid() and owner_formset.is_valid()):
            
            try:
                with transaction.atomic():
                    # Create facility
                    facility = facility_form.save(commit=False)
                    if request.user.is_authenticated:
                        facility.created_by = request.user.id
                    facility.save()
                    
                    # Save coordinates if provided
                    if coordinate_form.cleaned_data.get('latitude') and coordinate_form.cleaned_data.get('longitude'):
                        coordinate = coordinate_form.save(commit=False)
                        coordinate.facility = facility
                        if request.user.is_authenticated:
                            coordinate.created_by = request.user.id
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
                                contact.created_by = request.user.id
                            contact.save()
                    
                    # Save services
                    for service_form in service_formset:
                        if service_form.cleaned_data and not service_form.cleaned_data.get('DELETE', False):
                            service = service_form.save(commit=False)
                            service.facility = facility
                            if request.user.is_authenticated:
                                service.created_by = request.user.id
                            service.save()
                    
                    # Save owners
                    for owner_form in owner_formset:
                        if owner_form.cleaned_data and not owner_form.cleaned_data.get('DELETE', False):
                            owner = owner_form.save(commit=False)
                            owner.facility = facility
                            if request.user.is_authenticated:
                                owner.created_by = request.user.id
                            owner.save()
                    
                    messages.success(request, f'Facility "{facility.facility_name}" created successfully!')
                    return redirect('facilities:facility_detail', facility_id=facility.facility_id)
                    
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
    
    context = {
        'facility_form': facility_form,
        'coordinate_form': coordinate_form,
        'gbv_form': gbv_form,
        'contact_formset': contact_formset,
        'service_formset': service_formset,
        'owner_formset': owner_formset,
        'form_action': 'Create',
        'page_title': 'Create New Facility',
    }
    
    return render(request, 'facilities/facility_form.html', context)


@login_required
def facility_update(request, facility_id):
    """Update an existing facility with all related data"""
    facility = get_object_or_404(Facility, facility_id=facility_id, active_status=True)
    
    # Get existing related objects
    existing_coordinate = facility.facilitycoordinate_set.filter(active_status=True).first()
    existing_contacts = facility.facilitycontact_set.filter(active_status=True)
    existing_services = facility.facilityservice_set.filter(active_status=True)
    existing_owners = facility.facilityowner_set.filter(active_status=True)
    
    if request.method == 'POST':
        facility_form = FacilityForm(request.POST, instance=facility)
        coordinate_form = FacilityCoordinateForm(request.POST, instance=existing_coordinate)
        gbv_form = FacilityGBVCategoryForm(request.POST, facility=facility)
        contact_formset = FacilityContactFormSet(request.POST, prefix='contacts')
        service_formset = FacilityServiceFormSet(request.POST, prefix='services')
        owner_formset = FacilityOwnerFormSet(request.POST, prefix='owners')
        
        if (facility_form.is_valid() and coordinate_form.is_valid() and 
            gbv_form.is_valid() and contact_formset.is_valid() and 
            service_formset.is_valid() and owner_formset.is_valid()):
            
            try:
                with transaction.atomic():
                    # Update facility
                    facility = facility_form.save(commit=False)
                    if request.user.is_authenticated:
                        facility.updated_by = request.user.id
                    facility.save()
                    
                    # Update or create coordinates
                    if coordinate_form.cleaned_data.get('latitude') and coordinate_form.cleaned_data.get('longitude'):
                        if existing_coordinate:
                            coordinate = coordinate_form.save(commit=False)
                            if request.user.is_authenticated:
                                coordinate.updated_by = request.user.id
                            coordinate.save()
                        else:
                            coordinate = coordinate_form.save(commit=False)
                            coordinate.facility = facility
                            if request.user.is_authenticated:
                                coordinate.created_by = request.user.id
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
                    existing_contacts.update(active_status=False)
                    existing_services.update(active_status=False)
                    existing_owners.update(active_status=False)
                    
                    # Save new contacts
                    for contact_form in contact_formset:
                        if contact_form.cleaned_data and not contact_form.cleaned_data.get('DELETE', False):
                            contact = contact_form.save(commit=False)
                            contact.facility = facility
                            if request.user.is_authenticated:
                                contact.created_by = request.user.id
                            contact.save()
                    
                    # Save new services
                    for service_form in service_formset:
                        if service_form.cleaned_data and not service_form.cleaned_data.get('DELETE', False):
                            service = service_form.save(commit=False)
                            service.facility = facility
                            if request.user.is_authenticated:
                                service.created_by = request.user.id
                            service.save()
                    
                    # Save new owners
                    for owner_form in owner_formset:
                        if owner_form.cleaned_data and not owner_form.cleaned_data.get('DELETE', False):
                            owner = owner_form.save(commit=False)
                            owner.facility = facility
                            if request.user.is_authenticated:
                                owner.created_by = request.user.id
                            owner.save()
                    
                    messages.success(request, f'Facility "{facility.facility_name}" updated successfully!')
                    return redirect('facilities:facility_detail', facility_id=facility.facility_id)
                    
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
            {'contact_type': contact.contact_type, 'contact_value': contact.contact_value}
            for contact in existing_contacts
        ]
        service_initial = [
            {'service_category': service.service_category, 'service_description': service.service_description}
            for service in existing_services
        ]
        owner_initial = [
            {'owner_name': owner.owner_name, 'owner_type': owner.owner_type}
            for owner in existing_owners
        ]
        
        contact_formset = FacilityContactFormSet(prefix='contacts', initial=contact_initial)
        service_formset = FacilityServiceFormSet(prefix='services', initial=service_initial)
        owner_formset = FacilityOwnerFormSet(prefix='owners', initial=owner_initial)
    
    context = {
        'facility': facility,
        'facility_form': facility_form,
        'coordinate_form': coordinate_form,
        'gbv_form': gbv_form,
        'contact_formset': contact_formset,
        'service_formset': service_formset,
        'owner_formset': owner_formset,
        'form_action': 'Update',
        'page_title': f'Edit {facility.facility_name}',
    }
    
    return render(request, 'facilities/facility_form.html', context)
