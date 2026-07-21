# -*- encoding: utf-8 -*-
"""
Views for facilities app
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, F, FloatField, Case, When, Value, Prefetch
from django.db.models.functions import Power, Sqrt
import logging
from django.db import transaction
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .cache_utils import (
    get_facility_statistics, get_facilities_by_county, get_facilities_by_status,
    get_paginated_facilities, invalidate_facility_cache
)
from apps.authentication.permissions import (
    permission_required, role_required, any_role_required,
    staff_required, superuser_required
)
from .forms import (
    FacilityCoordinateForm, FacilityGBVCategoryForm, FacilityContactFormSet,
    FacilityServiceFormSet, FacilityOwnerFormSet, FacilityInfrastructureFormSet
)
from apps.geography.models import County
from apps.lookups.models import OperationalStatus, ServiceCategory
from .models import (
    Facility, FacilityCoordinate, FacilityGBVCategory, FacilityContact,
    FacilityService, FacilityOwner, FacilityInfrastructure
)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_ip_location(request):
    """Get user location from their IP address (backend IP geolocation)"""
    import logging
    import requests
    
    logger = logging.getLogger(__name__)
    
    try:
        # Get user's real IP from request headers
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        if not user_ip:
            user_ip = request.META.get('HTTP_X_REAL_IP', '').strip()
        if not user_ip:
            user_ip = request.META.get('REMOTE_ADDR', '').strip()
        
        logger.info(f"🌐 IP geolocation request - User IP: {user_ip}")
        
        if not user_ip:
            return JsonResponse({
                'success': False,
                'error': 'Could not determine IP address'
            }, status=400)
        
        # Try multiple IP geolocation services
        services = [
            {
                'url': f'https://ipapi.co/{user_ip}/json/',
                'parse': lambda d: {
                    'lat': d.get('latitude'),
                    'lng': d.get('longitude'),
                    'city': d.get('city'),
                    'country': d.get('country_name')
                }
            },
            {
                'url': f'http://ip-api.com/json/{user_ip}',
                'parse': lambda d: {
                    'lat': d.get('lat'),
                    'lng': d.get('lon'),
                    'city': d.get('city'),
                    'country': d.get('country')
                }
            }
        ]
        
        for service in services:
            try:
                response = requests.get(service['url'], timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    parsed = service['parse'](data)
                    
                    if parsed['lat'] and parsed['lng']:
                        lat = float(parsed['lat'])
                        lng = float(parsed['lng'])
                        
                        logger.info(f"✅ IP geolocation success: {lat}, {lng} - {parsed['city']}, {parsed['country']}")
                        
                        return JsonResponse({
                            'success': True,
                            'latitude': lat,
                            'longitude': lng,
                            'city': parsed['city'],
                            'country': parsed['country'],
                            'accuracy': 10000,  # ~10km accuracy for IP
                            'source': 'ip_geolocation'
                        })
            except Exception as e:
                logger.warning(f"⚠️ IP geolocation service failed: {e}")
                continue
        
        return JsonResponse({
            'success': False,
            'error': 'All IP geolocation services failed'
        }, status=500)
        
    except Exception as e:
        logger.error(f"❌ IP geolocation error: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def set_user_location(request):
    """Set user location in Django session for proximity sorting"""
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Log request details for debugging
        logger.info(f"📍 Location request received - Method: {request.method}, Content-Type: {request.content_type}")
        logger.info(f"📍 Session key: {request.session.session_key}, Session exists: {hasattr(request, 'session')}")
        
        # Parse JSON body
        try:
            body_str = request.body.decode('utf-8')
            logger.info(f"📍 Request body: {body_str[:200]}")
            data = json.loads(body_str)
        except json.JSONDecodeError as e:
            logger.error(f"📍 JSON decode error: {e}")
            return JsonResponse({'error': 'Invalid JSON', 'details': str(e)}, status=400)
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        logger.info(f"📍 Received coordinates - lat: {latitude}, lng: {longitude}")
        
        # If coordinates are null, just check if location is already set
        if latitude is None or longitude is None:
            has_location = 'user_latitude' in request.session and 'user_longitude' in request.session
            logger.info(f"📍 Checking existing location - has_location: {has_location}")
            
            if has_location:
                saved_lat = request.session.get('user_latitude')
                saved_lng = request.session.get('user_longitude')
                logger.info(f"📍 Returning existing location - lat: {saved_lat}, lng: {saved_lng}")
                return JsonResponse({
                    'success': True,
                    'latitude': saved_lat,
                    'longitude': saved_lng,
                    'message': 'Location already set'
                })
            else:
                # Return 200 with error message, not 404 (404 causes HTML response)
                logger.info("📍 No location set in session")
                return JsonResponse({
                    'success': False,
                    'error': 'No location set',
                    'latitude': None,
                    'longitude': None
                }, status=200)
        
        # Validate coordinates
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            logger.info(f"📍 Parsed coordinates - lat: {latitude}, lng: {longitude}")
        except (ValueError, TypeError) as e:
            logger.error(f"📍 Coordinate parse error: {e}")
            return JsonResponse({'error': 'Invalid coordinate format', 'details': str(e)}, status=400)
        
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            logger.error(f"📍 Invalid coordinate range - lat: {latitude}, lng: {longitude}")
            return JsonResponse({'error': 'Invalid coordinates'}, status=400)
        
        # Store in session (works even if not logged in - uses session middleware)
        try:
            request.session['user_latitude'] = latitude
            request.session['user_longitude'] = longitude
            request.session.modified = True  # Ensure session is saved
            
            # Force session save
            request.session.save()
            
            logger.info(f"✅ Location saved to session - lat: {latitude}, lng: {longitude}, session_key: {request.session.session_key}")
            
            return JsonResponse({
                'success': True,
                'latitude': latitude,
                'longitude': longitude,
                'message': 'Location saved successfully',
                'session_key': request.session.session_key
            })
        except Exception as session_error:
            logger.error(f"📍 Session save error: {session_error}")
            return JsonResponse({
                'error': 'Failed to save location',
                'details': str(session_error)
            }, status=500)
            
    except Exception as e:
        # Catch any unexpected errors and return JSON
        logger.error(f"📍 Unexpected error in set_user_location: {e}", exc_info=True)
        return JsonResponse({
            'error': str(e),
            'type': type(e).__name__
        }, status=500)


@permission_required('view_facilities')
def facility_list(request):
    """List all facilities with comprehensive data and pagination for millions of records"""
    import logging
    logger = logging.getLogger(__name__)
    
    # PROXIMITY-BASED SORTING: Get user location from session or request FIRST
    # Only default to Nairobi if NO location is available (prevents Baringo bias)
    user_latitude = None
    user_longitude = None
    use_proximity_sorting = True  # Always use proximity sorting
    location_source = 'none'
    
    # Try to get location from session (set by location-permission.js)
    if 'user_latitude' in request.session and 'user_longitude' in request.session:
        try:
            user_latitude = float(request.session['user_latitude'])
            user_longitude = float(request.session['user_longitude'])
            location_source = 'session'
            logger.info(f"📍 Facility list - Using location from SESSION: lat={user_latitude}, lng={user_longitude}")
            # Validate the coordinates are reasonable (not default Nairobi if user hasn't set location)
            if user_latitude == -1.2921 and user_longitude == 36.8219:
                # This might be a default, but we'll use it if it's explicitly in session
                logger.info("📍 Using default Nairobi coordinates from session")
        except (ValueError, TypeError) as e:
            logger.warning(f"📍 Error parsing session location: {e}")
            user_latitude = None
            user_longitude = None
    
    # Only use default Nairobi if no location is available
    if user_latitude is None or user_longitude is None:
        user_latitude = -1.2921  # Nairobi center (default)
        user_longitude = 36.8219
        location_source = 'default'
        logger.info(f"📍 Facility list - Using DEFAULT location: lat={user_latitude}, lng={user_longitude}")
    
    # Also check GET parameters (for manual testing)
    lat_param = request.GET.get('lat')
    lng_param = request.GET.get('lng')
    if lat_param and lng_param:
        try:
            user_latitude = float(lat_param)
            user_longitude = float(lng_param)
            location_source = 'url_param'
            # Store in session for future requests
            request.session['user_latitude'] = user_latitude
            request.session['user_longitude'] = user_longitude
            request.session.save()
            logger.info(f"📍 Facility list - Using location from URL PARAM: lat={user_latitude}, lng={user_longitude}")
        except (ValueError, TypeError) as e:
            logger.warning(f"📍 Error parsing URL location params: {e}")
            pass  # Use default Nairobi location
    
    # Get base queryset with optimized queries for large datasets
    # Apply proximity sorting annotation FIRST before other operations
    facilities = Facility.objects.select_related(
        'ward__constituency__county', 
        'operational_status'
    ).filter(is_active=True)
    
    # Apply proximity-based sorting annotation BEFORE prefetch_related
    if use_proximity_sorting and user_latitude and user_longitude:
        logger.info(f"📍 Applying proximity sorting with location: lat={user_latitude}, lng={user_longitude}, source={location_source}")
        facilities = facilities.annotate(
            distance_km=Case(
                When(
                    facilitycoordinate__latitude__isnull=False,
                    facilitycoordinate__longitude__isnull=False,
                    facilitycoordinate__is_active=True,
                    then=Sqrt(
                        Power(F('facilitycoordinate__latitude') - user_latitude, 2) +
                        Power(F('facilitycoordinate__longitude') - user_longitude, 2),
                        output_field=FloatField()
                    ) * 111.32  # Approximate conversion to km
                ),
                default=Value(999999, output_field=FloatField()),  # Very large distance for facilities without coordinates
                output_field=FloatField()
            )
        )
    else:
        logger.warning(f"📍 Proximity sorting NOT applied - use_proximity_sorting={use_proximity_sorting}, lat={user_latitude}, lng={user_longitude}")
    
    # Now apply prefetch_related (after annotation)
    facilities = facilities.prefetch_related(
        'facilityservice_set__service_category',
        'facilitycontact_set__contact_type',
        'facilityowner_set__owner_type',
        'facilitygbvcategory_set__gbv_category'
    )
    
    # Search functionality with database-level optimization
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
    
    # Apply ordering - proximity sorting if available, otherwise newest first
    if use_proximity_sorting and user_latitude and user_longitude:
        facilities = facilities.order_by('distance_km', 'facility_name')
    else:
        # Fallback: newest first to avoid Baringo bias
        facilities = facilities.order_by('-facility_id')
    
    # Implement pagination for millions of records
    paginator = Paginator(facilities, 50)  # 50 facilities per page for better performance
    page = request.GET.get('page')
    
    try:
        facilities_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        facilities_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        facilities_page = paginator.page(paginator.num_pages)
    
    # Get statistics efficiently (cached for better performance)
    stats = get_facility_statistics()
    operational_facilities_count = stats['operational_facilities']
    counties_count = stats['counties_count']
    wards_count = facilities.values('ward').distinct().count()
    
    # Get filter options
    counties = County.objects.all().order_by('county_name')
    operational_statuses = OperationalStatus.objects.all().order_by('status_name')
    service_categories = ServiceCategory.objects.all().order_by('category_name')
    
    # Log first few facilities with distances for debugging
    if use_proximity_sorting and user_latitude and user_longitude:
        try:
            sample_facilities = list(facilities_page[:5])
            logger.info(f"📍 Sample facilities with distances (first 5):")
            for f in sample_facilities:
                if hasattr(f, 'distance_km'):
                    logger.info(f"  - {f.facility_name}: {f.distance_km:.2f} km")
        except Exception as e:
            logger.warning(f"📍 Error logging sample facilities: {e}")
    
    context = {
        'facilities': facilities_page,  # Use paginated facilities
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
        'total_facilities': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': facilities_page.number,
        'has_previous': facilities_page.has_previous(),
        'has_next': facilities_page.has_next(),
        'previous_page_number': facilities_page.previous_page_number() if facilities_page.has_previous() else None,
        'next_page_number': facilities_page.next_page_number() if facilities_page.has_next() else None,
        # Add location info for debugging in template
        'user_latitude': user_latitude,
        'user_longitude': user_longitude,
        'location_source': location_source,
        'using_proximity_sorting': use_proximity_sorting and user_latitude and user_longitude,
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
    """Show facilities on a map with coordinates - optimized for millions of records"""
    logger = logging.getLogger(__name__)
    
    try:
        # Get viewport parameters for efficient loading
        ne_lat = request.GET.get('ne_lat')
        ne_lng = request.GET.get('ne_lng')
        sw_lat = request.GET.get('sw_lat')
        sw_lng = request.GET.get('sw_lng')
        zoom_level = request.GET.get('zoom', 7)
        
        # Base queryset with coordinates - only active coordinates
        facilities = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False,
            facilitycoordinate__is_active=True
        ).select_related(
            'ward__constituency__county',
            'operational_status'
        ).prefetch_related(
            Prefetch(
                'facilitycoordinate_set',
                queryset=FacilityCoordinate.objects.filter(
                    is_active=True,
                    latitude__isnull=False,
                    longitude__isnull=False
                ),
                to_attr='active_coordinates'
            )
        ).distinct()
        
        # Apply viewport filtering if provided (for dynamic loading)
        if ne_lat and ne_lng and sw_lat and sw_lng:
            try:
                ne_lat_float = float(ne_lat)
                ne_lng_float = float(ne_lng)
                sw_lat_float = float(sw_lat)
                sw_lng_float = float(sw_lng)
                
                # Validate coordinate ranges
                if -90 <= sw_lat_float <= ne_lat_float <= 90 and -180 <= sw_lng_float <= ne_lng_float <= 180:
                    facilities = facilities.filter(
                        facilitycoordinate__latitude__gte=sw_lat_float,
                        facilitycoordinate__latitude__lte=ne_lat_float,
                        facilitycoordinate__longitude__gte=sw_lng_float,
                        facilitycoordinate__longitude__lte=ne_lng_float,
                        facilitycoordinate__is_active=True
                    )
                else:
                    logger.warning(f"Invalid coordinate ranges: sw_lat={sw_lat_float}, ne_lat={ne_lat_float}, sw_lng={sw_lng_float}, ne_lng={ne_lng_float}")
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid viewport parameters: {e}")
                # Continue without viewport filtering
        
        # Limit results based on zoom level for performance
        try:
            zoom_level = int(zoom_level)
        except (ValueError, TypeError):
            zoom_level = 7
        
        if zoom_level <= 5:
            # Country level - show only major facilities
            facilities = facilities.filter(
                operational_status__status_name='Operational'
            )[:1000]  # Limit to 1000 facilities
        elif zoom_level <= 8:
            # Regional level - show more facilities
            facilities = facilities[:5000]  # Limit to 5000 facilities
        else:
            # Local level - show all facilities in viewport
            facilities = facilities[:10000]  # Limit to 10000 facilities
        
        # Filter facilities with coordinates and serialize for JavaScript
        facilities_with_coords = []
        for facility in facilities:
            try:
                # Use prefetched active_coordinates if available, otherwise fallback
                if hasattr(facility, 'active_coordinates') and facility.active_coordinates:
                    coords = facility.active_coordinates[0]
                else:
                    coords = facility.facilitycoordinate_set.filter(is_active=True).first()
                
                if coords and coords.latitude and coords.longitude:
                    # Ensure ward and operational_status exist with safe access
                    ward_name = facility.ward.ward_name if facility.ward else 'Unknown'
                    county_name = 'Unknown'
                    if facility.ward and facility.ward.constituency and facility.ward.constituency.county:
                        county_name = facility.ward.constituency.county.county_name
                    status_name = facility.operational_status.status_name if facility.operational_status else 'Unknown'
                    
                    facilities_with_coords.append({
                        'facility': {
                            'facility_id': facility.facility_id,
                            'facility_name': facility.facility_name,
                            'registration_number': facility.registration_number or '',
                            'ward': {
                                'ward_name': ward_name,
                                'constituency': {
                                    'county': {
                                        'county_name': county_name
                                    }
                                }
                            },
                            'operational_status': {
                                'status_name': status_name
                            }
                        },
                        'coordinates': {
                            'latitude': float(coords.latitude),
                            'longitude': float(coords.longitude)
                        }
                    })
            except Exception as e:
                logger.warning(f"Error processing facility {facility.facility_id}: {e}")
                continue  # Skip this facility and continue
        
        import json
        
        # Get total counts safely
        try:
            total_facilities = Facility.objects.filter(is_active=True).count()
        except Exception as e:
            logger.error(f"Error getting total facilities count: {e}")
            total_facilities = 0
        
        context = {
            'facilities_with_coords': facilities_with_coords,
            'facilities_with_coords_json': json.dumps(facilities_with_coords),
            'total_facilities': total_facilities,
            'facilities_with_coords_count': len(facilities_with_coords),
            'segment': 'facility_map',
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'viewport_filtered': bool(ne_lat and ne_lng and sw_lat and sw_lng),
            'zoom_level': zoom_level,
        }
        
        return render(request, 'facilities/facility_map.html', context)
    
    except Exception as e:
        logger.error(f"Error in facility_map view: {e}", exc_info=True)
        messages.error(request, 'An error occurred while loading the facility map. Please try again.')
        
        # Return minimal context to prevent template errors
        context = {
            'facilities_with_coords': [],
            'facilities_with_coords_json': '[]',
            'total_facilities': 0,
            'facilities_with_coords_count': 0,
            'segment': 'facility_map',
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'viewport_filtered': False,
            'zoom_level': 7,
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
                    # Invalidate cache after creating facility
                    invalidate_facility_cache()
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
                    # Invalidate cache after updating facility
                    invalidate_facility_cache()
                    return redirect('facilities:facility_list')
                    
            except Exception as e:
                messages.error(request, f'Error updating facility: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        facility_form = FacilityForm(instance=facility)
        coordinate_form = FacilityCoordinateForm(instance=existing_coordinate)
        gbv_form = FacilityGBVCategoryForm(facility=facility)
        contact_formset = FacilityContactFormSet(prefix='contacts', queryset=existing_contacts)
        service_formset = FacilityServiceFormSet(prefix='services', queryset=existing_services)
        owner_formset = FacilityOwnerFormSet(prefix='owners', queryset=existing_owners)
        infrastructure_formset = FacilityInfrastructureFormSet(prefix='infrastructure', queryset=existing_infrastructure)
    
    context = {
        'facility_form': facility_form,
        'coordinate_form': coordinate_form,
        'gbv_form': gbv_form,
        'contact_formset': contact_formset,
        'service_formset': service_formset,
        'owner_formset': owner_formset,
        'infrastructure_formset': infrastructure_formset,
        'form_action': 'Update',
        'page_title': f'Update Facility: {facility.facility_name}',
        'segment': 'facilities',
        'google_places_api_key': settings.GOOGLE_PLACES_API_KEY,
    }
    
    return render(request, 'facilities/facility_form.html', context)