# -*- encoding: utf-8 -*-
"""
Views for common app
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .geography import County, Constituency, Ward
from .lookups import OperationalStatus, ContactType, ServiceCategory, OwnerType, GBVCategory, DocumentType
from .documents import Document
from apps.facilities.models import Facility


@login_required
def geography_overview(request):
    """Show geographical overview with comprehensive statistics"""
    counties = County.objects.annotate(
        constituency_count=Count('constituency'),
        ward_count=Count('constituency__ward')
    ).order_by('county_name')
    
    # Get total counts
    total_constituencies = Constituency.objects.count()
    total_wards = Ward.objects.count()
    total_facilities = Facility.objects.filter(active_status=True).count()
    
    context = {
        'counties': counties,
        'total_constituencies': total_constituencies,
        'total_wards': total_wards,
        'total_facilities': total_facilities,
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
        active_status=True
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
        active_status=True
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
    facilities = ward.facility_set.filter(active_status=True).select_related(
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
        'operational_statuses': OperationalStatus.objects.all(),
        'contact_types': ContactType.objects.all(),
        'service_categories': ServiceCategory.objects.all(),
        'owner_types': OwnerType.objects.all(),
        'gbv_categories': GBVCategory.objects.all(),
        'document_types': DocumentType.objects.all(),
    }
    
    return render(request, 'common/lookup_tables.html', context)


@login_required
def document_list(request):
    """List all documents with comprehensive data"""
    documents = Document.objects.select_related(
        'facility', 'gbv_category', 'document_type', 'uploaded_by'
    ).order_by('-uploaded_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(facility__facility_name__icontains=search_query)
        )
    
    # Filter by document type
    doc_type_id = request.GET.get('doc_type')
    if doc_type_id:
        documents = documents.filter(document_type_id=doc_type_id)
    
    # Filter by GBV category
    gbv_category_id = request.GET.get('gbv_category')
    if gbv_category_id:
        documents = documents.filter(gbv_category_id=gbv_category_id)
    
    # Get filter options
    document_types = DocumentType.objects.all().order_by('type_name')
    gbv_categories = GBVCategory.objects.all().order_by('category_name')
    
    context = {
        'documents': documents,
        'search_query': search_query,
        'selected_doc_type': doc_type_id,
        'selected_gbv_category': gbv_category_id,
        'document_types': document_types,
        'gbv_categories': gbv_categories,
        'total_documents': documents.count(),
    }
    
    return render(request, 'common/document_list.html', context)


@login_required
def document_detail(request, document_id):
    """Show document details"""
    document = get_object_or_404(
        Document.objects.select_related(
            'facility__ward__constituency__county',
            'gbv_category',
            'document_type',
            'uploaded_by'
        ),
        document_id=document_id
    )
    
    context = {
        'document': document,
    }
    
    return render(request, 'common/document_detail.html', context)
