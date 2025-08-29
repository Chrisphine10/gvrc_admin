# -*- encoding: utf-8 -*-
"""
Views for common app
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import (
    OperationalStatus, ContactType, ServiceCategory, OwnerType, 
    GBVCategory, InfrastructureType, ConditionStatus, DocumentType
)
from apps.facilities.models import Facility


@login_required
def geography_overview(request):
    """Show geographical overview with comprehensive statistics"""
    counties = County.objects.annotate(
        constituency_count=Count('constituency'),
        ward_count=Count('constituency__ward')
    ).values('county_id', 'county_name', 'county_code', 'constituency_count', 'ward_count').order_by('county_name')
    
    # Get total counts
    total_constituencies = Constituency.objects.count()
    total_wards = Ward.objects.count()
    total_facilities = Facility.objects.filter(is_active=True).count()
    
    context = {
        'counties': counties,
        'total_constituencies': total_constituencies,
        'total_wards': total_wards,
        'total_facilities': total_facilities,
        'segment': 'geography',
    }
    
    return render(request, 'common/geography_overview.html', context)


@login_required
def county_detail(request, county_id):
    """Show county details with constituency and ward information"""
    county = get_object_or_404(County, county_id=county_id)
    constituencies = county.constituency_set.annotate(
        ward_count=Count('ward')
    ).order_by('constituency_name')
    
    # Get facility count for this county
    facility_count = Facility.objects.filter(
        ward__constituency__county=county,
        is_active=True
    ).count()
    
    context = {
        'county': county,
        'constituencies': constituencies,
        'facility_count': facility_count,
    }
    
    return render(request, 'common/county_detail.html', context)


@login_required
def constituency_detail(request, constituency_id):
    """Show constituency details with ward information"""
    constituency = get_object_or_404(Constituency, constituency_id=constituency_id)
    wards = constituency.ward_set.all().order_by('ward_name')
    
    # Get facility count for this constituency
    facility_count = Facility.objects.filter(
        ward__constituency=constituency,
        is_active=True
    ).count()
    
    context = {
        'constituency': constituency,
        'wards': wards,
        'facility_count': facility_count,
    }
    
    return render(request, 'common/constituency_detail.html', context)


@login_required
def ward_detail(request, ward_id):
    """Show ward details with facility information"""
    ward = get_object_or_404(Ward, ward_id=ward_id)
    facilities = ward.facility_set.filter(is_active=True).select_related(
        'operational_status'
    ).prefetch_related(
        'facilityservice_set__service_category'
    )
    
    context = {
        'ward': ward,
        'facilities': facilities,
        'facility_count': facilities.count(),
    }
    
    return render(request, 'common/ward_detail.html', context)


@login_required
def lookup_tables(request):
    """Show all lookup tables with counts"""
    context = {
        'operational_statuses': OperationalStatus.objects.all().order_by('sort_order', 'status_name'),
        'contact_types': ContactType.objects.all().order_by('type_name'),
        'service_categories': ServiceCategory.objects.all().order_by('category_name'),
        'owner_types': OwnerType.objects.all().order_by('type_name'),
        'gbv_categories': GBVCategory.objects.all().order_by('category_name'),
        'infrastructure_types': InfrastructureType.objects.all().order_by('type_name'),
        'condition_statuses': ConditionStatus.objects.all().order_by('status_name'),
        'document_types': DocumentType.objects.all().order_by('type_name'),
        'segment': 'lookups',
    }
    
    return render(request, 'common/lookup_tables.html', context)


# CRUD Views for Operational Status
@login_required
@require_http_methods(["POST"])
def add_operational_status(request):
    """Add new operational status"""
    try:
        status_name = request.POST.get('status_name')
        description = request.POST.get('description', '')
        sort_order = request.POST.get('sort_order', 0)
        
        if not status_name:
            messages.error(request, 'Status name is required')
            return redirect('common:lookup_tables')
        
        OperationalStatus.objects.create(
            status_name=status_name,
            description=description,
            sort_order=sort_order
        )
        messages.success(request, f'Operational status "{status_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding operational status: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_operational_status(request, status_id):
    """Edit operational status"""
    try:
        status = get_object_or_404(OperationalStatus, operational_status_id=status_id)
        status.status_name = request.POST.get('status_name')
        status.description = request.POST.get('description', '')
        status.sort_order = request.POST.get('sort_order', 0)
        status.save()
        messages.success(request, f'Operational status "{status.status_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating operational status: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_operational_status(request, status_id):
    """Delete operational status"""
    try:
        status = get_object_or_404(OperationalStatus, operational_status_id=status_id)
        status_name = status.status_name
        status.delete()
        messages.success(request, f'Operational status "{status_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting operational status: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for Contact Type
@login_required
@require_http_methods(["POST"])
def add_contact_type(request):
    """Add new contact type"""
    try:
        type_name = request.POST.get('type_name')
        validation_regex = request.POST.get('validation_regex', '')
        
        if not type_name:
            messages.error(request, 'Type name is required')
            return redirect('common:lookup_tables')
        
        ContactType.objects.create(
            type_name=type_name,
            validation_regex=validation_regex
        )
        messages.success(request, f'Contact type "{type_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding contact type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_contact_type(request, type_id):
    """Edit contact type"""
    try:
        contact_type = get_object_or_404(ContactType, contact_type_id=type_id)
        contact_type.type_name = request.POST.get('type_name')
        contact_type.validation_regex = request.POST.get('validation_regex', '')
        contact_type.save()
        messages.success(request, f'Contact type "{contact_type.type_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating contact type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_contact_type(request, type_id):
    """Delete contact type"""
    try:
        contact_type = get_object_or_404(ContactType, contact_type_id=type_id)
        type_name = contact_type.type_name
        contact_type.delete()
        messages.success(request, f'Contact type "{type_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting contact type: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for Service Category
@login_required
@require_http_methods(["POST"])
def add_service_category(request):
    """Add new service category"""
    try:
        category_name = request.POST.get('category_name')
        description = request.POST.get('description', '')
        icon_url = request.POST.get('icon_url', '')
        
        if not category_name:
            messages.error(request, 'Category name is required')
            return redirect('common:lookup_tables')
        
        ServiceCategory.objects.create(
            category_name=category_name,
            description=description,
            icon_url=icon_url
        )
        messages.success(request, f'Service category "{category_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding service category: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_service_category(request, category_id):
    """Edit service category"""
    try:
        category = get_object_or_404(ServiceCategory, service_category_id=category_id)
        category.category_name = request.POST.get('category_name')
        category.description = request.POST.get('description', '')
        category.icon_url = request.POST.get('icon_url', '')
        category.save()
        messages.success(request, f'Service category "{category.category_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating service category: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_service_category(request, category_id):
    """Delete service category"""
    try:
        category = get_object_or_404(ServiceCategory, service_category_id=category_id)
        category_name = category.category_name
        category.delete()
        messages.success(request, f'Service category "{category_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting service category: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for Owner Type
@login_required
@require_http_methods(["POST"])
def add_owner_type(request):
    """Add new owner type"""
    try:
        type_name = request.POST.get('type_name')
        description = request.POST.get('description', '')
        
        if not type_name:
            messages.error(request, 'Type name is required')
            return redirect('common:lookup_tables')
        
        OwnerType.objects.create(
            type_name=type_name,
            description=description
        )
        messages.success(request, f'Owner type "{type_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding owner type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_owner_type(request, type_id):
    """Edit owner type"""
    try:
        owner_type = get_object_or_404(OwnerType, owner_type_id=type_id)
        owner_type.type_name = request.POST.get('type_name')
        owner_type.description = request.POST.get('description', '')
        owner_type.save()
        messages.success(request, f'Owner type "{owner_type.type_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating owner type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_owner_type(request, type_id):
    """Delete owner type"""
    try:
        owner_type = get_object_or_404(OwnerType, owner_type_id=type_id)
        type_name = owner_type.type_name
        owner_type.delete()
        messages.success(request, f'Owner type "{type_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting owner type: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for GBV Category
@login_required
@require_http_methods(["POST"])
def add_gbv_category(request):
    """Add new GBV category"""
    try:
        category_name = request.POST.get('category_name')
        description = request.POST.get('description', '')
        icon_url = request.POST.get('icon_url', '')
        
        if not category_name:
            messages.error(request, 'Category name is required')
            return redirect('common:lookup_tables')
        
        GBVCategory.objects.create(
            category_name=category_name,
            description=description,
            icon_url=icon_url
        )
        messages.success(request, f'GBV category "{category_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding GBV category: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_gbv_category(request, category_id):
    """Edit GBV category"""
    try:
        category = get_object_or_404(GBVCategory, gbv_category_id=category_id)
        category.category_name = request.POST.get('category_name')
        category.description = request.POST.get('description', '')
        category.icon_url = request.POST.get('icon_url', '')
        category.save()
        messages.success(request, f'GBV category "{category.category_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating GBV category: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_gbv_category(request, category_id):
    """Delete GBV category"""
    try:
        category = get_object_or_404(GBVCategory, gbv_category_id=category_id)
        category_name = category.category_name
        category.delete()
        messages.success(request, f'GBV category "{category_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting GBV category: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for Infrastructure Type
@login_required
@require_http_methods(["POST"])
def add_infrastructure_type(request):
    """Add new infrastructure type"""
    try:
        type_name = request.POST.get('type_name')
        description = request.POST.get('description', '')
        
        if not type_name:
            messages.error(request, 'Type name is required')
            return redirect('common:lookup_tables')
        
        InfrastructureType.objects.create(
            type_name=type_name,
            description=description
        )
        messages.success(request, f'Infrastructure type "{type_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding infrastructure type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_infrastructure_type(request, type_id):
    """Edit infrastructure type"""
    try:
        infra_type = get_object_or_404(InfrastructureType, infrastructure_type_id=type_id)
        infra_type.type_name = request.POST.get('type_name')
        infra_type.description = request.POST.get('description', '')
        infra_type.save()
        messages.success(request, f'Infrastructure type "{infra_type.type_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating infrastructure type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_infrastructure_type(request, type_id):
    """Delete infrastructure type"""
    try:
        infra_type = get_object_or_404(InfrastructureType, infrastructure_type_id=type_id)
        type_name = infra_type.type_name
        infra_type.delete()
        messages.success(request, f'Infrastructure type "{type_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting infrastructure type: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for Condition Status
@login_required
@require_http_methods(["POST"])
def add_condition_status(request):
    """Add new condition status"""
    try:
        status_name = request.POST.get('status_name')
        description = request.POST.get('description', '')
        
        if not status_name:
            messages.error(request, 'Status name is required')
            return redirect('common:lookup_tables')
        
        ConditionStatus.objects.create(
            status_name=status_name,
            description=description
        )
        messages.success(request, f'Condition status "{status_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding condition status: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_condition_status(request, status_id):
    """Edit condition status"""
    try:
        status = get_object_or_404(ConditionStatus, condition_status_id=status_id)
        status.status_name = request.POST.get('status_name')
        status.description = request.POST.get('description', '')
        status.save()
        messages.success(request, f'Condition status "{status.status_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating condition status: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_condition_status(request, status_id):
    """Delete condition status"""
    try:
        status = get_object_or_404(ConditionStatus, condition_status_id=status_id)
        status_name = status.status_name
        status.delete()
        messages.success(request, f'Condition status "{status_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting condition status: {str(e)}')
    
    return redirect('common:lookup_tables')


# CRUD Views for Document Type
@login_required
@require_http_methods(["POST"])
def add_document_type(request):
    """Add new document type"""
    try:
        type_name = request.POST.get('type_name')
        allowed_extensions = request.POST.get('allowed_extensions', '')
        max_file_size_mb = request.POST.get('max_file_size_mb', 10)
        description = request.POST.get('description', '')
        
        if not type_name:
            messages.error(request, 'Type name is required')
            return redirect('common:lookup_tables')
        
        DocumentType.objects.create(
            type_name=type_name,
            allowed_extensions=allowed_extensions,
            max_file_size_mb=max_file_size_mb,
            description=description
        )
        messages.success(request, f'Document type "{type_name}" added successfully')
    except Exception as e:
        messages.error(request, f'Error adding document type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def edit_document_type(request, type_id):
    """Edit document type"""
    try:
        doc_type = get_object_or_404(DocumentType, document_type_id=type_id)
        doc_type.type_name = request.POST.get('type_name')
        doc_type.allowed_extensions = request.POST.get('allowed_extensions', '')
        doc_type.max_file_size_mb = request.POST.get('max_file_size_mb', 10)
        doc_type.description = request.POST.get('description', '')
        doc_type.save()
        messages.success(request, f'Document type "{doc_type.type_name}" updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating document type: {str(e)}')
    
    return redirect('common:lookup_tables')


@login_required
@require_http_methods(["POST"])
def delete_document_type(request, type_id):
    """Delete document type"""
    try:
        doc_type = get_object_or_404(DocumentType, document_type_id=type_id)
        type_name = doc_type.type_name
        doc_type.delete()
        messages.success(request, f'Document type "{type_name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting document type: {str(e)}')
    
    return redirect('common:lookup_tables')



