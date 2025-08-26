# -*- encoding: utf-8 -*-
"""
Views for home app
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from apps.documents.models import Document
from apps.facilities.models import Facility
from apps.authentication.models import User
from apps.authentication.views import custom_login_required
from apps.geography.models import County
import logging
from django.utils import timezone
from datetime import timedelta
from apps.chat.models import Conversation, Message
from apps.music.models import Music, MusicPlay
from apps.facilities.models import FacilityService, FacilityContact, FacilityInfrastructure
from apps.lookups.models import ServiceCategory, ContactType, InfrastructureType

logger = logging.getLogger(__name__)


def landing_page(request):
    """Landing page for unauthenticated users"""
    if request.user.is_authenticated:
        return redirect('home')
    
    # Get some public statistics to showcase the system
    total_facilities = Facility.objects.filter(is_active=True).count()
    total_counties = County.objects.count()
    
    # Get operational facilities count
    operational_facilities = Facility.objects.filter(
        is_active=True,
        operational_status__status_name='Operational'
    ).count()
    
    context = {
        'total_facilities': total_facilities,
        'total_counties': total_counties,
        'operational_facilities': operational_facilities,
        'segment': 'landing',
    }
    
    return render(request, 'home/landing.html', context)


@custom_login_required
def index(request):
    """Dashboard view with comprehensive system overview - only for authenticated users"""
    
    # Get basic counts
    total_facilities = Facility.objects.filter(is_active=True).count()
    total_users = User.objects.filter(is_active=True).count()
    total_counties = County.objects.count()
    
    # Get facility statistics
    operational_facilities = Facility.objects.filter(
        is_active=True,
        operational_status__status_name='Operational'
    ).count()
    
    non_operational_facilities = Facility.objects.filter(
        is_active=True
    ).exclude(
        operational_status__status_name='Operational'
    ).count()
    
    facilities_with_coordinates = Facility.objects.filter(
        is_active=True,
        facilitycoordinate__isnull=False
    ).distinct().count()
    
    facilities_with_services = Facility.objects.filter(
        is_active=True,
        facilityservice__isnull=False
    ).distinct().count()
    
    # Get document statistics
    total_documents = Document.objects.filter(is_active=True).count()
    recent_documents = Document.objects.filter(
        is_active=True
    ).select_related('document_type', 'gbv_category').order_by('-uploaded_at')[:5]
    
    # Get chat statistics
    total_conversations = Conversation.objects.count()
    active_conversations = Conversation.objects.filter(status__in=['new', 'active']).count()
    urgent_conversations = Conversation.objects.filter(priority='urgent').count()
    total_messages = Message.objects.count()
    
    # Get recent chat activity
    recent_conversations = Conversation.objects.select_related(
        'mobile_session', 'assigned_admin'
    ).order_by('-last_message_at', '-created_at')[:5]
    
    # Get music statistics
    total_music_tracks = Music.objects.filter(is_active=True).count()
    total_music_plays = MusicPlay.objects.count()
    recent_music_plays = MusicPlay.objects.select_related(
        'music', 'user'
    ).order_by('-played_at')[:5]
    
    # Get service statistics
    total_services = FacilityService.objects.filter(is_active=True).count()
    services_by_category = FacilityService.objects.filter(
        is_active=True
    ).values('service_category__category_name').annotate(
        count=Count('service_id')
    ).order_by('-count')[:5]
    
    # Get human resources statistics
    total_contacts = FacilityContact.objects.filter(is_active=True).count()
    contacts_by_type = FacilityContact.objects.filter(
        is_active=True
    ).values('contact_type__type_name').annotate(
        count=Count('contact_id')
    ).order_by('-count')[:5]
    
    # Get infrastructure statistics
    total_infrastructure = FacilityInfrastructure.objects.count()
    infrastructure_by_type = FacilityInfrastructure.objects.values(
        'infrastructure_type__type_name'
    ).annotate(
        count=Count('infrastructure_id'),
        available=Count('infrastructure_id', filter=Q(is_available=True)),
        good_condition=Count('infrastructure_id', filter=Q(condition_status__status_name__in=['Good', 'Excellent']))
    ).order_by('-count')[:5]
    
    # Get recent facilities
    recent_facilities = Facility.objects.filter(
        is_active=True
    ).select_related(
        'ward__constituency__county'
    ).order_by('-created_at')[:5]
    
    # Get system activity in last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_activity = {
        'facilities_created': Facility.objects.filter(created_at__gte=thirty_days_ago).count(),
        'documents_uploaded': Document.objects.filter(uploaded_at__gte=thirty_days_ago).count(),
        'conversations_started': Conversation.objects.filter(created_at__gte=thirty_days_ago).count(),
        'music_plays': MusicPlay.objects.filter(played_at__gte=thirty_days_ago).count(),
    }
    
    # Get top performing items
    top_services = FacilityService.objects.filter(
        is_active=True
    ).values('service_category__category_name').annotate(
        facility_count=Count('facility_id', distinct=True)
    ).order_by('-facility_count')[:5]
    
    top_music = Music.objects.filter(
        is_active=True
    ).annotate(
        play_count=Count('musicplay__play_id')
    ).order_by('-play_count')[:5]
    
    context = {
        'total_facilities': total_facilities,
        'total_users': total_users,
        'total_counties': total_counties,
        'operational_facilities': operational_facilities,
        'non_operational_facilities': non_operational_facilities,
        'facilities_with_coordinates': facilities_with_coordinates,
        'facilities_with_services': facilities_with_services,
        'recent_facilities': recent_facilities,
        
        # Document data
        'total_documents': total_documents,
        'recent_documents': recent_documents,
        
        # Chat data
        'total_conversations': total_conversations,
        'active_conversations': active_conversations,
        'urgent_conversations': urgent_conversations,
        'total_messages': total_messages,
        'recent_conversations': recent_conversations,
        
        # Music data
        'total_music_tracks': total_music_tracks,
        'total_music_plays': total_music_plays,
        'recent_music_plays': recent_music_plays,
        
        # Service data
        'total_services': total_services,
        'services_by_category': services_by_category,
        'top_services': top_services,
        
        # Human resources data
        'total_contacts': total_contacts,
        'contacts_by_type': contacts_by_type,
        
        # Infrastructure data
        'total_infrastructure': total_infrastructure,
        'infrastructure_by_type': infrastructure_by_type,
        
        # Activity data
        'recent_activity': recent_activity,
        'top_music': top_music,
        
        'segment': 'index',
    }
    
    return render(request, 'home/index.html', context)


def community_facilities(request):
    """Community Facilities List Page - redirects to facilities app"""
    return redirect('facilities:facility_list')


def services_programs(request):
    """Services & Programs List Page"""
    from apps.facilities.models import FacilityService, Facility
    from apps.lookups.models import ServiceCategory
    
    # Get search parameters
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    facility_id = request.GET.get('facility', '')
    
    # Base queryset with optimized relationships
    services = FacilityService.objects.filter(is_active=True).select_related(
        'facility', 
        'facility__ward__constituency__county',
        'facility__operational_status',
        'service_category'
    ).prefetch_related(
        'facility__facilitygbvcategory_set__gbv_category',
        'facility__facilitycontact_set__contact_type'
    )
    
    # Apply filters
    if search:
        services = services.filter(
            Q(service_description__icontains=search) |
            Q(service_category__category_name__icontains=search) |
            Q(facility__facility_name__icontains=search) |
            Q(facility__ward__ward_name__icontains=search) |
            Q(facility__ward__constituency__county__county_name__icontains=search)
        )
    
    if category_id:
        services = services.filter(service_category_id=category_id)
    
    if facility_id:
        services = services.filter(facility_id=facility_id)
    
    # Get statistics
    total_services = services.count()
    total_facilities_with_services = services.values('facility_id').distinct().count()
    total_categories = services.values('service_category_id').distinct().count()
    
    # Group services by category for summary
    services_by_category = {}
    for service in services:
        if service.service_category:
            category_name = service.service_category.category_name
            if category_name not in services_by_category:
                services_by_category[category_name] = {
                    'services': [],
                    'facilities': set(),
                    'service_category_id': service.service_category.service_category_id
                }
            services_by_category[category_name]['services'].append(service)
            services_by_category[category_name]['facilities'].add(service.facility.facility_id)
    
    # Convert sets to counts for template usage
    for category_data in services_by_category.values():
        category_data['facility_count'] = len(category_data['facilities'])
        category_data['service_count'] = len(category_data['services'])
    
    # Pagination
    paginator = Paginator(services.order_by('service_category__category_name', 'facility__facility_name'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    service_categories = ServiceCategory.objects.all().order_by('category_name')
    facilities_with_services = Facility.objects.filter(
        is_active=True,
        facilityservice__is_active=True
    ).distinct().order_by('facility_name')
    
    context = {
        'segment': 'services',
        'page_title': 'Services & Programs',
        'page_obj': page_obj,
        'services': services,
        'services_by_category': services_by_category,
        'service_categories': service_categories,
        'facilities_with_services': facilities_with_services,
        'search': search,
        'selected_category': category_id,
        'selected_facility': facility_id,
        'total_services': total_services,
        'total_facilities_with_services': total_facilities_with_services,
        'total_categories': total_categories,
    }
    
    return render(request, 'home/services.html', context)


def add_service(request):
    """Add Service & Program Page - redirects to facilities app for service management"""
    messages.info(request, "Service management is handled through the facility creation/editing process.")
    return redirect('facilities:facility_list')


def human_resources(request):
    """Human Resources List Page - Based on Facility Contacts"""
    from apps.facilities.models import FacilityContact, Facility
    from apps.lookups.models import ContactType
    
    # Get search parameters
    search = request.GET.get('search', '')
    contact_type_id = request.GET.get('contact_type', '')
    facility_id = request.GET.get('facility', '')
    
    # Define HR-related contact types (these should be in your database)
    hr_contact_types = ContactType.objects.filter(
        type_name__in=[
            'Primary Contact', 'Manager', 'Director', 'Supervisor', 
            'Staff', 'Emergency Contact', 'Administrative Contact'
        ]
    )
    
    # Base queryset for HR contacts with optimized relationships
    hr_contacts = FacilityContact.objects.filter(
        is_active=True,
        contact_type__in=hr_contact_types
    ).select_related(
        'facility', 
        'facility__ward__constituency__county',
        'facility__operational_status',
        'contact_type'
    ).prefetch_related(
        'facility__facilitygbvcategory_set__gbv_category',
        'facility__facilityservice_set__service_category'
    )
    
    # Apply filters
    if search:
        hr_contacts = hr_contacts.filter(
            Q(contact_value__icontains=search) |
            Q(facility__facility_name__icontains=search) |
            Q(contact_type__type_name__icontains=search) |
            Q(facility__ward__ward_name__icontains=search) |
            Q(facility__ward__constituency__county__county_name__icontains=search)
        )
    
    if contact_type_id:
        hr_contacts = hr_contacts.filter(contact_type_id=contact_type_id)
    
    if facility_id:
        hr_contacts = hr_contacts.filter(facility_id=facility_id)
    
    # Get statistics
    total_hr_contacts = hr_contacts.count()
    total_facilities_with_hr = hr_contacts.values('facility_id').distinct().count()
    total_contact_types = hr_contacts.values('contact_type_id').distinct().count()
    
    # Group HR contacts by type for summary
    hr_by_type = {}
    for contact in hr_contacts:
        if contact.contact_type:
            type_name = contact.contact_type.type_name
            if type_name not in hr_by_type:
                hr_by_type[type_name] = {
                    'contacts': [],
                    'facilities': set(),
                    'contact_type_id': contact.contact_type.contact_type_id
                }
            hr_by_type[type_name]['contacts'].append(contact)
            hr_by_type[type_name]['facilities'].add(contact.facility.facility_id)
    
    # Convert sets to counts for template usage
    for type_data in hr_by_type.values():
        type_data['facility_count'] = len(type_data['facilities'])
        type_data['contact_count'] = len(type_data['contacts'])
    
    # Pagination
    paginator = Paginator(hr_contacts.order_by('contact_type__type_name', 'facility__facility_name'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    facilities_with_hr = Facility.objects.filter(
        is_active=True,
        facilitycontact__is_active=True,
        facilitycontact__contact_type__in=hr_contact_types
    ).distinct().order_by('facility_name')
    
    context = {
        'segment': 'humanresources',
        'page_title': 'Human Resources',
        'page_obj': page_obj,
        'hr_contacts': hr_contacts,
        'hr_by_type': hr_by_type,
        'hr_contact_types': hr_contact_types,
        'facilities_with_hr': facilities_with_hr,
        'search': search,
        'selected_contact_type': contact_type_id,
        'selected_facility': facility_id,
        'total_hr_contacts': total_hr_contacts,
        'total_facilities_with_hr': total_facilities_with_hr,
        'total_contact_types': total_contact_types,
    }
    
    return render(request, 'home/human_resources.html', context)


def add_staff(request):
    """Add Staff Page - redirects to facilities app for staff management"""
    messages.info(request, "Staff management is handled through the facility creation/editing process.")
    return redirect('facilities:facility_list')


def infrastructure(request):
    """Infrastructure Page - displays list of all infrastructure from facilities"""
    from apps.facilities.models import FacilityInfrastructure
    from apps.lookups.models import InfrastructureType, ConditionStatus
    
    # Get search parameters
    search = request.GET.get('search', '')
    infrastructure_type_id = request.GET.get('infrastructure_type', '')
    condition_id = request.GET.get('condition', '')
    facility_id = request.GET.get('facility', '')
    
    # Base queryset with optimized relationships - FacilityInfrastructure doesn't have is_active
    infrastructure_list = FacilityInfrastructure.objects.select_related(
        'facility', 
        'facility__ward__constituency__county',
        'infrastructure_type',
        'condition_status'
    ).order_by('facility__facility_name', 'infrastructure_type__type_name')
    
    # Apply filters
    if search:
        infrastructure_list = infrastructure_list.filter(
            Q(description__icontains=search) |
            Q(facility__facility_name__icontains=search) |
            Q(infrastructure_type__type_name__icontains=search)
        )
    
    if infrastructure_type_id:
        infrastructure_list = infrastructure_list.filter(infrastructure_type_id=infrastructure_type_id)
    
    if condition_id:
        infrastructure_list = infrastructure_list.filter(condition_status_id=condition_id)
    
    if facility_id:
        infrastructure_list = infrastructure_list.filter(facility_id=facility_id)
    
    # Get statistics
    total_infrastructure = infrastructure_list.count()
    available_infrastructure = infrastructure_list.filter(is_available=True).count()
    unavailable_infrastructure = infrastructure_list.filter(is_available=False).count()
    
    # Group by infrastructure type for summary
    infrastructure_by_type = {}
    for item in infrastructure_list:
        type_name = item.infrastructure_type.type_name
        if type_name not in infrastructure_by_type:
            infrastructure_by_type[type_name] = {
                'items': [],
                'total_capacity': 0,
                'total_utilization': 0,
                'good_condition': 0,
                'needs_attention': 0
            }
        infrastructure_by_type[type_name]['items'].append(item)
        infrastructure_by_type[type_name]['total_capacity'] += item.capacity or 0
        infrastructure_by_type[type_name]['total_utilization'] += item.current_utilization or 0
        
        # Count by condition
        if item.condition_status.status_name in ['Good', 'Excellent']:
            infrastructure_by_type[type_name]['good_condition'] += 1
        else:
            infrastructure_by_type[type_name]['needs_attention'] += 1
    
    # Pagination
    paginator = Paginator(infrastructure_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    infrastructure_types = InfrastructureType.objects.all().order_by('type_name')
    condition_statuses = ConditionStatus.objects.all().order_by('status_name')
    
    context = {
        'segment': 'infrastructure',
        'page_title': 'Infrastructure Overview',
        'page_obj': page_obj,
        'infrastructure_list': page_obj,
        'infrastructure_by_type': infrastructure_by_type,
        'infrastructure_types': infrastructure_types,
        'condition_statuses': condition_statuses,
        'search': search,
        'selected_infrastructure_type': infrastructure_type_id,
        'selected_condition': condition_id,
        'total_infrastructure': total_infrastructure,
        'available_infrastructure': available_infrastructure,
        'unavailable_infrastructure': unavailable_infrastructure,
    }
    
    return render(request, 'home/infrastructure.html', context)


def help_page(request):
    """Help & Documentation Page"""
    context = {
        'segment': 'help',
        'page_title': 'Help & Documentation'
    }
    return render(request, 'home/help.html', context)


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        # Add .html extension if not present
        if not load_template.endswith('.html'):
            load_template += '.html'
        
        context['segment'] = load_template.replace('.html', '')
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
        
    except loader.TemplateDoesNotExist:
        # Return a generic 404 page
        error_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Page Not Found</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 50px; 
            text-align: center;
        }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
<h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <a href="{% url 'landing' %}">Return to Home</a>
</body>
</html>
        """
        return HttpResponse(error_html)

    except Exception as e:
        # Return simple 404 page without template loading
        error_html = """
<!DOCTYPE html>
<html>
<head><title>Page Not Found</title></head>
<body>
    <h1>Page Not Found</h1>
<p>The requested page could not be found.</p>
    <a href="{% url 'landing' %}">Return to Home</a>
</body>
</html>
        """
        return HttpResponse(error_html)
