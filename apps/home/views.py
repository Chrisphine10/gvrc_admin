# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


def index(request):
    """Home page - GVRC Admin Dashboard"""
    try:
        # Import facility models
        from apps.facilities.models import Facility, Facility_Services, Facility_HumanResources, Facility_Infrastructure
        
        # Get facility statistics by type
        facility_stats = Facility.objects.filter(is_active=True).values('facility_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get location statistics
        location_stats = Facility.objects.filter(is_active=True).values('county').annotate(
            count=Count('id')
        ).order_by('-count')[:5]  # Top 5 counties
        
        # Get facilities with coordinates
        facilities_with_coords = Facility.objects.filter(
            is_active=True, 
            latitude__isnull=False, 
            longitude__isnull=False
        ).count()
        
        # Get infrastructure statistics
        infrastructure_stats = Facility_Infrastructure.objects.filter(is_operational=True).values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get vehicle statistics
        vehicles_count = Facility_Infrastructure.objects.filter(
            is_operational=True,
            category__in=['ambulance', 'emergency_vehicle', 'medical_transport', 'police_vehicle', 'security_vehicle']
        ).count()
        
        context = {
            'segment': 'index',
            'page_title': 'GVRC Admin Dashboard',
            'facility_count': Facility.objects.filter(is_active=True).count(),
            'service_count': Facility_Services.objects.filter(is_available=True).count(),
            'hr_summary': {
                'total_staff': Facility_HumanResources.objects.filter(is_active=True).count(),
                'medical_staff': Facility_HumanResources.objects.filter(
                    is_active=True, staff_category__in=['medical', 'nursing', 'pharmacy', 'laboratory']
                ).count(),
                'security_staff': Facility_HumanResources.objects.filter(
                    is_active=True, staff_category__in=['police', 'security']
                ).count(),
                'support_staff': Facility_HumanResources.objects.filter(
                    is_active=True, staff_category__in=['counselor', 'social_worker', 'psychologist', 'legal']
                ).count(),
            },
            'facility_stats': facility_stats,
            'location_stats': location_stats,
            'facilities_with_coords': facilities_with_coords,
            'infrastructure_stats': infrastructure_stats,
            'vehicles_count': vehicles_count,
            'modules': [
                {
                    'name': 'Community Facilities',
                    'description': 'Manage health facilities, police stations, CBOs, safe houses, legal aid centers, and gender desks',
                    'url': '/facilities/',
                    'icon': 'fas fa-building',
                    'count': Facility.objects.count()
                },
                {
                    'name': 'Services & Programs',
                    'description': 'Track services offered by community facilities including health, security, legal, and support services',
                    'url': '/services/',
                    'icon': 'fas fa-hands-helping',
                    'count': Facility_Services.objects.count()
                },
                {
                    'name': 'Operational Equipment',
                    'description': 'Manage ambulances, emergency vehicles, medical equipment, and operational resources',
                    'url': '/infrastructure/',
                    'icon': 'fas fa-ambulance',
                    'count': Facility_Infrastructure.objects.count()
                },
                {
                    'name': 'Human Resources',
                    'description': 'Manage staff across all facility types including medical, security, legal, and support personnel',
                    'url': '/human-resources/',
                    'icon': 'fas fa-users',
                    'count': Facility_HumanResources.objects.count()
                },
                {
                    'name': 'Emergency Vehicles',
                    'description': 'Track ambulances, police vehicles, and emergency transport equipment',
                    'url': '/infrastructure/',
                    'icon': 'fas fa-car',
                    'count': vehicles_count
                },
                {
                    'name': 'Reports & Analytics',
                    'description': 'Generate insights and compliance reports for community facility management',
                    'url': '/admin/',
                    'icon': 'fas fa-chart-bar',
                    'count': 0
                },
            ]
        }
    except ImportError:
        # Fallback if facilities app is not available
        context = {
            'segment': 'index',
            'page_title': 'GVRC Admin Dashboard',
            'facility_count': 0,
            'service_count': 0,
            'hr_summary': {'total_staff': 0, 'medical_staff': 0, 'security_staff': 0, 'support_staff': 0},
            'facility_stats': [],
            'location_stats': [],
            'facilities_with_coords': 0,
            'infrastructure_stats': [],
            'vehicles_count': 0,
            'modules': [
                {
                    'name': 'Community Facilities',
                    'description': 'Manage health facilities, police stations, CBOs, safe houses, legal aid centers, and gender desks',
                    'url': '/facilities/',
                    'icon': 'fas fa-building',
                    'count': 0
                },
                {
                    'name': 'Services & Programs',
                    'description': 'Track services offered by community facilities including health, security, legal, and support services',
                    'url': '/services/',
                    'icon': 'fas fa-hands-helping',
                    'count': 0
                },
                {
                    'name': 'Operational Equipment',
                    'description': 'Manage ambulances, emergency vehicles, medical equipment, and operational resources',
                    'url': '/infrastructure/',
                    'icon': 'fas fa-ambulance',
                    'count': 0
                },
                {
                    'name': 'Human Resources',
                    'description': 'Manage staff across all facility types including medical, security, legal, and support personnel',
                    'url': '/human-resources/',
                    'icon': 'fas fa-users',
                    'count': 0
                },
                {
                    'name': 'Emergency Vehicles',
                    'description': 'Track ambulances, police vehicles, and emergency transport equipment',
                    'url': '/infrastructure/',
                    'icon': 'fas fa-car',
                    'count': 0
                },
                {
                    'name': 'Reports & Analytics',
                    'description': 'Generate insights and compliance reports for community facility management',
                    'url': '/admin/',
                    'icon': 'fas fa-chart-bar',
                    'count': 0
                },
            ]
        }
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required
def community_facilities(request):
    """Community Facilities List Page"""
    try:
        from apps.facilities.models import Facility
        
        # Get search parameters
        search = request.GET.get('search', '')
        facility_type = request.GET.get('facility_type', '')
        county = request.GET.get('county', '')
        ownership = request.GET.get('ownership', '')
        
        # Base queryset
        facilities = Facility.objects.filter(is_active=True)
        
        # Apply filters
        if search:
            facilities = facilities.filter(
                Q(name__icontains=search) |
                Q(registration_number__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(county__icontains=search)
            )
        
        if facility_type:
            facilities = facilities.filter(facility_type=facility_type)
        
        if county:
            facilities = facilities.filter(county__icontains=county)
        
        if ownership:
            facilities = facilities.filter(ownership=ownership)
        
        # Pagination
        paginator = Paginator(facilities.order_by('name'), 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get filter options
        facility_types = Facility.FACILITY_TYPES
        ownership_types = Facility.OWNERSHIP_TYPES
        counties = Facility.objects.values_list('county', flat=True).distinct().order_by('county')
        
        context = {
            'segment': 'facilities',
            'page_title': 'Community Facilities',
            'page_obj': page_obj,
            'facility_types': facility_types,
            'ownership_types': ownership_types,
            'counties': counties,
            'search': search,
            'selected_facility_type': facility_type,
            'selected_county': county,
            'selected_ownership': ownership,
            'total_count': facilities.count(),
        }
        
        html_template = loader.get_template('home/facilities.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'facilities',
            'page_title': 'Community Facilities',
            'error': 'Facilities module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def add_facility(request):
    """Add Community Facility Page"""
    try:
        from apps.facilities.models import Facility
        
        if request.method == 'POST':
            try:
                # Extract form data
                name = request.POST.get('name', '').strip()
                facility_type = request.POST.get('facility_type', '')
                ownership = request.POST.get('ownership', '')
                county = request.POST.get('county', '').strip()
                ward = request.POST.get('ward', '').strip()
                location = request.POST.get('location', '').strip()
                contact_person = request.POST.get('contact_person', '').strip()
                phone = request.POST.get('phone', '').strip()
                email = request.POST.get('email', '').strip()
                registration_number = request.POST.get('registration_number', '').strip()
                target_population = request.POST.get('target_population', '').strip()
                services_offered = request.POST.get('services_offered', '').strip()
                operating_hours = request.POST.get('operating_hours', '').strip()
                emergency_contact = request.POST.get('emergency_contact', '').strip()
                
                # Validation
                errors = []
                if not name:
                    errors.append("Facility name is required")
                if not facility_type:
                    errors.append("Facility type is required")
                if not ownership:
                    errors.append("Ownership type is required")
                if not county:
                    errors.append("County is required")
                if not registration_number:
                    errors.append("Registration number is required")
                
                # Check if registration number already exists
                if Facility.objects.filter(registration_number=registration_number).exists():
                    errors.append("Registration number already exists")
                
                if errors:
                    context = {
                        'segment': 'facilities',
                        'page_title': 'Add Community Facility',
                        'facility_types': Facility.FACILITY_TYPES,
                        'ownership_types': Facility.OWNERSHIP_TYPES,
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_facility.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Create facility
                facility = Facility.objects.create(
                    name=name,
                    facility_type=facility_type,
                    ownership=ownership,
                    county=county,
                    ward=ward,
                    location=location,
                    contact_person=contact_person,
                    phone=phone,
                    email=email,
                    registration_number=registration_number,
                    target_population=target_population,
                    services_offered=services_offered,
                    operating_hours=operating_hours,
                    emergency_contact=emergency_contact,
                    is_active=True
                )
                
                logger.info(f"Facility created successfully: {facility.name} (ID: {facility.id})")
                
                context = {
                    'segment': 'facilities',
                    'page_title': 'Add Community Facility',
                    'facility_types': Facility.FACILITY_TYPES,
                    'ownership_types': Facility.OWNERSHIP_TYPES,
                    'toast_type': 'success',
                    'toast_message': f'Facility "{facility.name}" created successfully!'
                }
                html_template = loader.get_template('home/add_facility.html')
                return HttpResponse(html_template.render(context, request))
                
            except Exception as e:
                logger.error(f"Error creating facility: {str(e)}")
                context = {
                    'segment': 'facilities',
                    'page_title': 'Add Community Facility',
                    'facility_types': Facility.FACILITY_TYPES,
                    'ownership_types': Facility.OWNERSHIP_TYPES,
                    'form_data': request.POST,
                    'toast_type': 'error',
                    'toast_message': 'An error occurred while creating the facility. Please try again.'
                }
                html_template = loader.get_template('home/add_facility.html')
                return HttpResponse(html_template.render(context, request))
        
        # GET request - show form
        context = {
            'segment': 'facilities',
            'page_title': 'Add Community Facility',
            'facility_types': Facility.FACILITY_TYPES,
            'ownership_types': Facility.OWNERSHIP_TYPES,
        }
        
        html_template = loader.get_template('home/add_facility.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'facilities',
            'page_title': 'Add Community Facility',
            'error': 'Facilities module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def services_programs(request):
    """Services & Programs List Page"""
    try:
        from apps.facilities.models import Facility_Services, Facility
        
        # Get search parameters
        search = request.GET.get('search', '')
        category = request.GET.get('category', '')
        facility_name = request.GET.get('facility_name', '')
        
        # Base queryset
        services = Facility_Services.objects.filter(is_available=True)
        
        # Apply filters
        if search:
            services = services.filter(
                Q(service_name__icontains=search) |
                Q(description__icontains=search) |
                Q(facility__name__icontains=search)
            )
        
        if category:
            services = services.filter(category=category)
        
        if facility_name:
            services = services.filter(facility__name__icontains=facility_name)
        
        # Pagination
        paginator = Paginator(services.select_related('facility').order_by('facility__name', 'service_name'), 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get filter options
        service_categories = Facility_Services.SERVICE_CATEGORIES
        facilities = Facility.objects.filter(is_active=True).order_by('name')
        
        context = {
            'segment': 'services',
            'page_title': 'Services & Programs',
            'page_obj': page_obj,
            'service_categories': service_categories,
            'facilities': facilities,
            'search': search,
            'selected_category': category,
            'selected_facility_name': facility_name,
            'total_count': services.count(),
        }
        
        html_template = loader.get_template('home/services.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'services',
            'page_title': 'Services & Programs',
            'error': 'Services module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def add_service(request):
    """Add Service & Program Page"""
    try:
        from apps.facilities.models import Facility_Services, Facility
        
        if request.method == 'POST':
            try:
                # Extract form data
                service_name = request.POST.get('service_name', '').strip()
                facility_id = request.POST.get('facility', '')
                category = request.POST.get('category', '')
                description = request.POST.get('description', '').strip()
                is_available = request.POST.get('is_available') == 'on'
                
                # Validation
                errors = []
                if not service_name:
                    errors.append("Service name is required")
                if not facility_id:
                    errors.append("Facility is required")
                if not category:
                    errors.append("Service category is required")
                
                if errors:
                    context = {
                        'segment': 'services',
                        'page_title': 'Add Service & Program',
                        'service_categories': Facility_Services.SERVICE_CATEGORIES,
                        'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_service.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Get facility
                try:
                    facility = Facility.objects.get(id=facility_id)
                except Facility.DoesNotExist:
                    errors.append("Selected facility does not exist")
                    context = {
                        'segment': 'services',
                        'page_title': 'Add Service & Program',
                        'service_categories': Facility_Services.SERVICE_CATEGORIES,
                        'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_service.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Create service
                service = Facility_Services.objects.create(
                    facility=facility,
                    service_name=service_name,
                    category=category,
                    description=description,
                    is_available=is_available
                )
                
                logger.info(f"Service created successfully: {service.service_name} (ID: {service.id})")
                
                context = {
                    'segment': 'services',
                    'page_title': 'Add Service & Program',
                    'service_categories': Facility_Services.SERVICE_CATEGORIES,
                    'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                    'toast_type': 'success',
                    'toast_message': f'Service "{service.service_name}" created successfully!'
                }
                html_template = loader.get_template('home/add_service.html')
                return HttpResponse(html_template.render(context, request))
                
            except Exception as e:
                logger.error(f"Error creating service: {str(e)}")
                context = {
                    'segment': 'services',
                    'page_title': 'Add Service & Program',
                    'service_categories': Facility_Services.SERVICE_CATEGORIES,
                    'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                    'form_data': request.POST,
                    'toast_type': 'error',
                    'toast_message': 'An error occurred while creating the service. Please try again.'
                }
                html_template = loader.get_template('home/add_service.html')
                return HttpResponse(html_template.render(context, request))
        
        # GET request - show form
        context = {
            'segment': 'services',
            'page_title': 'Add Service & Program',
            'service_categories': Facility_Services.SERVICE_CATEGORIES,
            'facilities': Facility.objects.filter(is_active=True).order_by('name'),
        }
        
        html_template = loader.get_template('home/add_service.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'services',
            'page_title': 'Add Service & Program',
            'error': 'Services module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def human_resources(request):
    """Human Resources List Page"""
    try:
        from apps.facilities.models import Facility_HumanResources, Facility
        
        # Get search parameters
        search = request.GET.get('search', '')
        staff_category = request.GET.get('staff_category', '')
        facility_name = request.GET.get('facility_name', '')
        
        # Base queryset
        staff = Facility_HumanResources.objects.filter(is_active=True)
        
        # Apply filters
        if search:
            staff = staff.filter(
                Q(full_name__icontains=search) |
                Q(position__icontains=search) |
                Q(qualification__icontains=search) |
                Q(facility__name__icontains=search)
            )
        
        if staff_category:
            staff = staff.filter(staff_category=staff_category)
        
        if facility_name:
            staff = staff.filter(facility__name__icontains=facility_name)
        
        # Pagination
        paginator = Paginator(staff.select_related('facility').order_by('facility__name', 'full_name'), 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get filter options
        staff_categories = Facility_HumanResources.STAFF_CATEGORIES
        facilities = Facility.objects.filter(is_active=True).order_by('name')
        
        context = {
            'segment': 'humanresources',
            'page_title': 'Human Resources',
            'page_obj': page_obj,
            'staff_categories': staff_categories,
            'facilities': facilities,
            'search': search,
            'selected_staff_category': staff_category,
            'selected_facility_name': facility_name,
            'total_count': staff.count(),
        }
        
        html_template = loader.get_template('home/human_resources.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'humanresources',
            'page_title': 'Human Resources',
            'error': 'Human Resources module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def add_staff(request):
    """Add Human Resource Staff Page"""
    try:
        from apps.facilities.models import Facility_HumanResources, Facility
        
        if request.method == 'POST':
            try:
                # Extract form data
                full_name = request.POST.get('full_name', '').strip()
                facility_id = request.POST.get('facility', '')
                staff_category = request.POST.get('staff_category', '')
                position = request.POST.get('position', '').strip()
                qualification = request.POST.get('qualification', '').strip()
                license_number = request.POST.get('license_number', '').strip()
                phone = request.POST.get('phone', '').strip()
                email = request.POST.get('email', '').strip()
                is_active = request.POST.get('is_active') == 'on'
                
                # Validation
                errors = []
                if not full_name:
                    errors.append("Full name is required")
                if not facility_id:
                    errors.append("Facility is required")
                if not staff_category:
                    errors.append("Staff category is required")
                if not position:
                    errors.append("Position is required")
                
                if errors:
                    context = {
                        'segment': 'humanresources',
                        'page_title': 'Add Staff Member',
                        'staff_categories': Facility_HumanResources.STAFF_CATEGORIES,
                        'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_staff.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Get facility
                try:
                    facility = Facility.objects.get(id=facility_id)
                except Facility.DoesNotExist:
                    errors.append("Selected facility does not exist")
                    context = {
                        'segment': 'humanresources',
                        'page_title': 'Add Staff Member',
                        'staff_categories': Facility_HumanResources.STAFF_CATEGORIES,
                        'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_staff.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Create staff member
                staff = Facility_HumanResources.objects.create(
                    facility=facility,
                    staff_category=staff_category,
                    position=position,
                    full_name=full_name,
                    qualification=qualification,
                    license_number=license_number,
                    phone=phone,
                    email=email,
                    is_active=is_active
                )
                
                logger.info(f"Staff member created successfully: {staff.full_name} (ID: {staff.id})")
                
                context = {
                    'segment': 'humanresources',
                    'page_title': 'Add Staff Member',
                    'staff_categories': Facility_HumanResources.STAFF_CATEGORIES,
                    'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                    'toast_type': 'success',
                    'toast_message': f'Staff member "{staff.full_name}" created successfully!'
                }
                html_template = loader.get_template('home/add_staff.html')
                return HttpResponse(html_template.render(context, request))
                
            except Exception as e:
                logger.error(f"Error creating staff member: {str(e)}")
                context = {
                    'segment': 'humanresources',
                    'page_title': 'Add Staff Member',
                    'staff_categories': Facility_HumanResources.STAFF_CATEGORIES,
                    'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                    'form_data': request.POST,
                    'toast_type': 'error',
                    'toast_message': 'An error occurred while creating the staff member. Please try again.'
                }
                html_template = loader.get_template('home/add_staff.html')
                return HttpResponse(html_template.render(context, request))
        
        # GET request - show form
        context = {
            'segment': 'humanresources',
            'page_title': 'Add Staff Member',
            'staff_categories': Facility_HumanResources.STAFF_CATEGORIES,
            'facilities': Facility.objects.filter(is_active=True).order_by('name'),
        }
        
        html_template = loader.get_template('home/add_staff.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'humanresources',
            'page_title': 'Add Staff Member',
            'error': 'Human Resources module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def infrastructure(request):
    """Infrastructure List Page"""
    try:
        from apps.facilities.models import Facility_Infrastructure, Facility
        
        # Get search parameters
        search = request.GET.get('search', '')
        category = request.GET.get('category', '')
        facility_name = request.GET.get('facility_name', '')
        condition = request.GET.get('condition', '')
        
        # Base queryset
        equipment = Facility_Infrastructure.objects.all()
        
        # Apply filters
        if search:
            equipment = equipment.filter(
                Q(equipment_name__icontains=search) |
                Q(registration_number__icontains=search) |
                Q(facility__name__icontains=search)
            )
        
        if category:
            equipment = equipment.filter(category=category)
        
        if facility_name:
            equipment = equipment.filter(facility__name__icontains=facility_name)
        
        if condition:
            equipment = equipment.filter(condition=condition)
        
        # Pagination
        paginator = Paginator(equipment.select_related('facility').order_by('facility__name', 'equipment_name'), 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get filter options
        equipment_categories = Facility_Infrastructure.EQUIPMENT_CATEGORIES
        equipment_conditions = Facility_Infrastructure.EQUIPMENT_CONDITIONS
        facilities = Facility.objects.filter(is_active=True).order_by('name')
        
        context = {
            'segment': 'infrastructure',
            'page_title': 'Infrastructure & Equipment',
            'page_obj': page_obj,
            'equipment_categories': equipment_categories,
            'equipment_conditions': equipment_conditions,
            'facilities': facilities,
            'search': search,
            'selected_category': category,
            'selected_facility_name': facility_name,
            'selected_condition': condition,
            'total_count': equipment.count(),
        }
        
        html_template = loader.get_template('home/infrastructure.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'infrastructure',
            'page_title': 'Infrastructure & Equipment',
            'error': 'Infrastructure module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def add_equipment(request):
    """Add Infrastructure Equipment Page"""
    try:
        from apps.facilities.models import Facility_Infrastructure, Facility
        from datetime import datetime
        
        if request.method == 'POST':
            try:
                # Extract form data
                equipment_name = request.POST.get('equipment_name', '').strip()
                facility_id = request.POST.get('facility', '')
                category = request.POST.get('category', '')
                quantity = request.POST.get('quantity', '1')
                condition = request.POST.get('condition', 'good')
                registration_number = request.POST.get('registration_number', '').strip()
                model_year = request.POST.get('model_year', '').strip()
                capacity = request.POST.get('capacity', '').strip()
                fuel_type = request.POST.get('fuel_type', '').strip()
                is_operational = request.POST.get('is_operational') == 'on'
                notes = request.POST.get('notes', '').strip()
                
                # Validation
                errors = []
                if not equipment_name:
                    errors.append("Equipment name is required")
                if not facility_id:
                    errors.append("Facility is required")
                if not category:
                    errors.append("Equipment category is required")
                
                # Validate quantity
                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        errors.append("Quantity must be greater than 0")
                except ValueError:
                    errors.append("Quantity must be a valid number")
                
                # Validate model year
                if model_year:
                    try:
                        model_year = int(model_year)
                        current_year = datetime.now().year
                        if model_year < 1900 or model_year > current_year + 1:
                            errors.append("Model year must be between 1900 and next year")
                    except ValueError:
                        errors.append("Model year must be a valid number")
                
                if errors:
                    context = {
                        'segment': 'infrastructure',
                        'page_title': 'Add Equipment',
                        'equipment_categories': Facility_Infrastructure.EQUIPMENT_CATEGORIES,
                        'equipment_conditions': Facility_Infrastructure.EQUIPMENT_CONDITIONS,
                        'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_equipment.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Get facility
                try:
                    facility = Facility.objects.get(id=facility_id)
                except Facility.DoesNotExist:
                    errors.append("Selected facility does not exist")
                    context = {
                        'segment': 'infrastructure',
                        'page_title': 'Add Equipment',
                        'equipment_categories': Facility_Infrastructure.EQUIPMENT_CATEGORIES,
                        'equipment_conditions': Facility_Infrastructure.EQUIPMENT_CONDITIONS,
                        'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                        'form_data': request.POST,
                        'errors': errors,
                        'toast_type': 'error',
                        'toast_message': 'Please correct the errors below.'
                    }
                    html_template = loader.get_template('home/add_equipment.html')
                    return HttpResponse(html_template.render(context, request))
                
                # Create equipment
                equipment = Facility_Infrastructure.objects.create(
                    facility=facility,
                    equipment_name=equipment_name,
                    category=category,
                    quantity=quantity,
                    condition=condition,
                    registration_number=registration_number,
                    model_year=model_year if model_year else None,
                    capacity=capacity,
                    fuel_type=fuel_type,
                    is_operational=is_operational,
                    notes=notes
                )
                
                logger.info(f"Equipment created successfully: {equipment.equipment_name} (ID: {equipment.id})")
                
                context = {
                    'segment': 'infrastructure',
                    'page_title': 'Add Equipment',
                    'equipment_categories': Facility_Infrastructure.EQUIPMENT_CATEGORIES,
                    'equipment_conditions': Facility_Infrastructure.EQUIPMENT_CONDITIONS,
                    'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                    'toast_type': 'success',
                    'toast_message': f'Equipment "{equipment.equipment_name}" created successfully!'
                }
                html_template = loader.get_template('home/add_equipment.html')
                return HttpResponse(html_template.render(context, request))
                
            except Exception as e:
                logger.error(f"Error creating equipment: {str(e)}")
                context = {
                    'segment': 'infrastructure',
                    'page_title': 'Add Equipment',
                    'equipment_categories': Facility_Infrastructure.EQUIPMENT_CATEGORIES,
                    'equipment_conditions': Facility_Infrastructure.EQUIPMENT_CONDITIONS,
                    'facilities': Facility.objects.filter(is_active=True).order_by('name'),
                    'form_data': request.POST,
                    'toast_type': 'error',
                    'toast_message': 'An error occurred while creating the equipment. Please try again.'
                }
                html_template = loader.get_template('home/add_equipment.html')
                return HttpResponse(html_template.render(context, request))
        
        # GET request - show form
        context = {
            'segment': 'infrastructure',
            'page_title': 'Add Equipment',
            'equipment_categories': Facility_Infrastructure.EQUIPMENT_CATEGORIES,
            'equipment_conditions': Facility_Infrastructure.EQUIPMENT_CONDITIONS,
            'facilities': Facility.objects.filter(is_active=True).order_by('name'),
        }
        
        html_template = loader.get_template('home/add_equipment.html')
        return HttpResponse(html_template.render(context, request))
        
    except ImportError:
        context = {
            'segment': 'infrastructure',
            'page_title': 'Add Equipment',
            'error': 'Infrastructure module not available'
        }
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def dashboard(request):
    """Protected dashboard for staff and super admin"""
    return HttpResponse(f"Hello {request.user.username}, you have full access to the dashboard.")

@login_required
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.strip('/').split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        # Set segment context based on the page
        if load_template == 'help':
            context['segment'] = 'help'
        else:
            context['segment'] = load_template

        # Add page title for better context
        if load_template == 'help':
            context['page_title'] = 'Help Center'
        else:
            context['page_title'] = load_template.replace('-', ' ').title()

        # Use simple template for help page to avoid template inheritance issues
        if load_template == 'help':
            # Return simple HTML directly to avoid template loading issues
            html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Help Center - GVRC Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <h1 class="mb-4"><i class="fas fa-question-circle me-2"></i>GVRC Admin Help Center</h1>
                
                <div class="alert alert-info">
                    <h5><i class="fas fa-info-circle me-2"></i>About GVRC Admin</h5>
                    <p class="mb-0">
                        GVRC Admin is a centralized directory and administrative system for managing community-based facilities 
                        including health facilities, police stations, CBOs, safe houses, legal aid centers, gender desks, 
                        and other community organizations.
                    </p>
                </div>

                <div class="row">
                    <div class="col-md-8">
                        <h3>Community Facility Types</h3>
                        
                        <div class="card mb-3">
                            <div class="card-header">
                                <h5><i class="fas fa-hospital me-2"></i>Health Facilities</h5>
                            </div>
                            <div class="card-body">
                                <p>Manage healthcare facilities and medical services:</p>
                                <ul>
                                    <li>Hospitals, Clinics, Dispensaries</li>
                                    <li>Health Centers, Laboratories, Pharmacies</li>
                                    <li>Medical staff and equipment tracking</li>
                                    <li>Health service availability monitoring</li>
                                </ul>
                            </div>
                        </div>

                        <div class="card mb-3">
                            <div class="card-header">
                                <h5><i class="fas fa-shield-alt me-2"></i>Security & Police Facilities</h5>
                            </div>
                            <div class="card-body">
                                <p>Track police stations and security services:</p>
                                <ul>
                                    <li>Police Stations and Police Posts</li>
                                    <li>Security Offices and Personnel</li>
                                    <li>Emergency response coordination</li>
                                    <li>Security equipment and resources</li>
                                </ul>
                            </div>
                        </div>

                        <div class="card mb-3">
                            <div class="card-header">
                                <h5><i class="fas fa-hands-helping me-2"></i>Community Organizations</h5>
                            </div>
                            <div class="card-body">
                                <p>Manage community-based organizations and support services:</p>
                                <ul>
                                    <li>Community-Based Organizations (CBOs)</li>
                                    <li>Non-Governmental Organizations (NGOs)</li>
                                    <li>Faith-Based Organizations</li>
                                    <li>Community Centers and Youth Centers</li>
                                </ul>
                            </div>
                        </div>

                        <div class="card mb-3">
                            <div class="card-header">
                                <h5><i class="fas fa-home me-2"></i>Support & Protection Services</h5>
                            </div>
                            <div class="card-body">
                                <p>Track support and protection facilities:</p>
                                <ul>
                                    <li>Safe Houses and Shelters</li>
                                    <li>Legal Aid Centers</li>
                                    <li>Gender Desks and Women Centers</li>
                                    <li>Counseling and Rehabilitation Centers</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <h3>Quick Links</h3>
                        <div class="list-group">
                            <a href="/facilities/" class="list-group-item list-group-item-action">
                                <i class="fas fa-building me-2"></i>Manage Community Facilities
                            </a>
                            <a href="/services/" class="list-group-item list-group-item-action">
                                <i class="fas fa-hands-helping me-2"></i>Manage Services & Programs
                            </a>
                            <a href="/human-resources/" class="list-group-item list-group-item-action">
                                <i class="fas fa-users me-2"></i>Manage Staff
                            </a>
                            <a href="/infrastructure/" class="list-group-item list-group-item-action">
                                <i class="fas fa-ambulance me-2"></i>Manage Operational Equipment
                            </a>
                            <a href="/admin/" class="list-group-item list-group-item-action">
                                <i class="fas fa-cog me-2"></i>Admin Panel
                            </a>
                        </div>

                        <div class="card mt-4">
                            <div class="card-header">
                                <h6><i class="fas fa-headset me-2"></i>Support</h6>
                            </div>
                            <div class="card-body">
                                <p class="small">
                                    For technical support or access requests, contact:
                                </p>
                                <ul class="list-unstyled small">
                                    <li><i class="fas fa-envelope me-1"></i>admin@gvrc.com</li>
                                    <li><i class="fas fa-phone me-1"></i>+254 XXX XXX XXX</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
            """
            return HttpResponse(html_content)
        else:
            try:
                html_template = loader.get_template('home/' + load_template)
                return HttpResponse(html_template.render(context, request))
            except:
                # Return simple 404 page if template not found
                error_html = """
<!DOCTYPE html>
<html>
<head><title>Page Not Found</title></head>
<body>
<h1>404 - Page Not Found</h1>
<p>The requested page could not be found.</p>
</body>
</html>
                """
                return HttpResponse(error_html)

    except template.TemplateDoesNotExist as e:
        # Return simple 404 page without template loading
        error_html = """
<!DOCTYPE html>
<html>
<head><title>Page Not Found</title></head>
<body>
<h1>404 - Page Not Found</h1>
<p>The requested page could not be found.</p>
</body>
</html>
        """
        return HttpResponse(error_html)

    except Exception as e:
        # Log the error for debugging (console only)
        print(f"Error in pages view for {request.path}: {str(e)}")
        # Return simple error page without template loading
        error_html = """
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<h1>Error</h1>
<p>Something went wrong: """ + str(e) + """</p>
</body>
</html>
        """
        return HttpResponse(error_html)
