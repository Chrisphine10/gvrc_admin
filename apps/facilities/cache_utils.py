# -*- encoding: utf-8 -*-
"""
Caching utilities for facilities app to handle millions of records efficiently
"""

from django.core.cache import cache
from django.conf import settings
from django.db.models import Count, Q
from .models import Facility, FacilityCoordinate
from apps.geography.models import County
from apps.lookups.models import OperationalStatus
import json
import hashlib


def get_cache_key(prefix, **kwargs):
    """Generate a consistent cache key from parameters"""
    # Sort kwargs for consistent key generation
    sorted_kwargs = sorted(kwargs.items())
    key_string = f"{prefix}:{':'.join(f'{k}={v}' for k, v in sorted_kwargs)}"
    return hashlib.md5(key_string.encode()).hexdigest()


def get_facility_statistics():
    """Get cached facility statistics"""
    cache_key = 'facility_statistics'
    cached_stats = cache.get(cache_key)
    
    if cached_stats is None:
        # Calculate statistics
        total_facilities = Facility.objects.filter(is_active=True).count()
        operational_facilities = Facility.objects.filter(
            is_active=True,
            operational_status__status_name='Operational'
        ).count()
        counties_count = County.objects.count()
        facilities_with_coordinates = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False
        ).distinct().count()
        
        cached_stats = {
            'total_facilities': total_facilities,
            'operational_facilities': operational_facilities,
            'counties_count': counties_count,
            'facilities_with_coordinates': facilities_with_coordinates,
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, cached_stats, 300)
    
    return cached_stats


def get_facilities_by_county():
    """Get cached facilities count by county"""
    cache_key = 'facilities_by_county'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        facilities_by_county = Facility.objects.filter(
            is_active=True
        ).values(
            'ward__constituency__county__county_name'
        ).annotate(
            count=Count('facility_id')
        ).order_by('-count')[:20]  # Top 20 counties
        
        cached_data = list(facilities_by_county)
        
        # Cache for 10 minutes
        cache.set(cache_key, cached_data, 600)
    
    return cached_data


def get_facilities_by_status():
    """Get cached facilities count by operational status"""
    cache_key = 'facilities_by_status'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        facilities_by_status = Facility.objects.filter(
            is_active=True
        ).values('operational_status__status_name').annotate(
            count=Count('facility_id')
        ).order_by('-count')
        
        cached_data = {item['operational_status__status_name']: item['count'] for item in facilities_by_status}
        
        # Cache for 10 minutes
        cache.set(cache_key, cached_data, 600)
    
    return cached_data


def get_facilities_in_viewport(ne_lat, ne_lng, sw_lat, sw_lng, zoom_level=7, **filters):
    """Get cached facilities in a specific viewport"""
    cache_key = get_cache_key(
        'facilities_viewport',
        ne_lat=ne_lat,
        ne_lng=ne_lng,
        sw_lat=sw_lat,
        sw_lng=sw_lng,
        zoom=zoom_level,
        **filters
    )
    
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # Build queryset
        queryset = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False,
            facilitycoordinate__latitude__gte=float(sw_lat),
            facilitycoordinate__latitude__lte=float(ne_lat),
            facilitycoordinate__longitude__gte=float(sw_lng),
            facilitycoordinate__longitude__lte=float(ne_lng)
        ).select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related('facilitycoordinate_set')
        
        # Apply additional filters
        if 'county_id' in filters:
            queryset = queryset.filter(ward__constituency__county_id=filters['county_id'])
        if 'status_id' in filters:
            queryset = queryset.filter(operational_status_id=filters['status_id'])
        
        # Limit based on zoom level
        if zoom_level <= 5:
            queryset = queryset.filter(operational_status__status_name='Operational')[:1000]
        elif zoom_level <= 8:
            queryset = queryset[:5000]
        else:
            queryset = queryset[:10000]
        
        # Serialize data
        facilities_data = []
        for facility in queryset:
            coords = facility.facilitycoordinate_set.filter(is_active=True).first()
            if coords:
                facilities_data.append({
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
        
        cached_data = facilities_data
        
        # Cache for 2 minutes (shorter for viewport data)
        cache.set(cache_key, cached_data, 120)
    
    return cached_data


def invalidate_facility_cache():
    """Invalidate all facility-related cache"""
    cache_keys = [
        'facility_statistics',
        'facilities_by_county',
        'facilities_by_status',
    ]
    
    for key in cache_keys:
        cache.delete(key)
    
    # Clear viewport cache patterns
    cache.delete_many(cache.keys('facilities_viewport:*'))


def get_paginated_facilities(page=1, page_size=50, search_query='', **filters):
    """Get cached paginated facilities"""
    cache_key = get_cache_key(
        'facilities_paginated',
        page=page,
        page_size=page_size,
        search=search_query,
        **filters
    )
    
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        from django.core.paginator import Paginator
        
        # Build queryset
        queryset = Facility.objects.select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            'facilityservice_set__service_category',
            'facilitycontact_set__contact_type',
            'facilityowner_set__owner_type',
            'facilitygbvcategory_set__gbv_category'
        ).filter(is_active=True)
        
        # Apply search
        if search_query:
            queryset = queryset.filter(
                Q(facility_name__icontains=search_query) |
                Q(registration_number__icontains=search_query) |
                Q(ward__ward_name__icontains=search_query) |
                Q(ward__constituency__constituency_name__icontains=search_query) |
                Q(ward__constituency__county__county_name__icontains=search_query)
            )
        
        # Apply filters
        if 'county_id' in filters:
            queryset = queryset.filter(ward__constituency__county_id=filters['county_id'])
        if 'status_id' in filters:
            queryset = queryset.filter(operational_status_id=filters['status_id'])
        
        # Order and paginate
        queryset = queryset.order_by('facility_id')
        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.page(page)
            cached_data = {
                'facilities': list(page_obj.object_list),
                'total_count': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            }
        except:
            cached_data = {
                'facilities': [],
                'total_count': 0,
                'total_pages': 0,
                'current_page': 1,
                'has_previous': False,
                'has_next': False,
                'previous_page_number': None,
                'next_page_number': None,
            }
        
        # Cache for 5 minutes
        cache.set(cache_key, cached_data, 300)
    
    return cached_data
