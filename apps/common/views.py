# -*- encoding: utf-8 -*-
"""
Views for common app
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from apps.geography.models import County, Constituency, Ward
from apps.lookups.models import OperationalStatus, ContactType, ServiceCategory, OwnerType, GBVCategory, DocumentType

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
    total_facilities = Facility.objects.filter(is_active=True).count()
    
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
        'operational_statuses': OperationalStatus.objects.all(),
        'contact_types': ContactType.objects.all(),
        'service_categories': ServiceCategory.objects.all(),
        'owner_types': OwnerType.objects.all(),
        'gbv_categories': GBVCategory.objects.all(),
        'document_types': DocumentType.objects.all(),
    }
    
    return render(request, 'common/lookup_tables.html', context)



