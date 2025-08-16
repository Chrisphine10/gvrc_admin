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
from apps.facilities.models import Facility
from apps.authentication.models import User
from apps.authentication.views import custom_login_required
from apps.common.geography import County
from apps.common.documents import Document
import logging

logger = logging.getLogger(__name__)


@custom_login_required
def index(request):
    """Dashboard view with system overview"""
    # Get basic counts
    total_facilities = Facility.objects.filter(active_status=True).count()
    total_users = User.objects.filter(is_active=True).count()
    total_counties = County.objects.count()
    total_documents = Document.objects.count()
    
    # Get facility statistics
    operational_facilities = Facility.objects.filter(
        active_status=True,
        operational_status__status_name='Operational'
    ).count()
    
    non_operational_facilities = Facility.objects.filter(
        active_status=True
    ).exclude(
        operational_status__status_name='Operational'
    ).count()
    
    facilities_with_coordinates = Facility.objects.filter(
        active_status=True,
        facilitycoordinate__isnull=False
    ).distinct().count()
    
    facilities_with_services = Facility.objects.filter(
        active_status=True,
        facilityservice__isnull=False
    ).distinct().count()
    
    # Get recent facilities
    recent_facilities = Facility.objects.filter(
        active_status=True
    ).select_related(
        'ward__constituency__county'
    ).order_by('-created_at')[:5]
    
    context = {
        'total_facilities': total_facilities,
        'total_users': total_users,
        'total_counties': total_counties,
        'total_documents': total_documents,
        'operational_facilities': operational_facilities,
        'non_operational_facilities': non_operational_facilities,
        'facilities_with_coordinates': facilities_with_coordinates,
        'facilities_with_services': facilities_with_services,
        'recent_facilities': recent_facilities,
    }
    
    return render(request, 'home/index.html', context)


def community_facilities(request):
    """Community Facilities List Page - redirects to facilities app"""
    return redirect('facilities:facility_list')


def services_programs(request):
    """Services & Programs List Page"""
    from apps.facilities.models import FacilityService, Facility
    from apps.common.lookups import ServiceCategory
    
    # Get search parameters
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    facility_id = request.GET.get('facility', '')
    
    # Base queryset with optimized relationships
    services = FacilityService.objects.filter(active_status=True).select_related(
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
    total_facilities_with_services = services.values('facility').distinct().count()
    total_categories = services.values('service_category').distinct().count()
    
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
        active_status=True,
        facilityservice__active_status=True
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
    from apps.common.lookups import ContactType
    
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
        active_status=True,
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
    total_facilities_with_hr = hr_contacts.values('facility').distinct().count()
    total_contact_types = hr_contacts.values('contact_type').distinct().count()
    
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
        active_status=True,
        facilitycontact__active_status=True,
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


def documents(request):
    """Documents List Page"""
    from apps.common.lookups import DocumentType, GBVCategory
    
    # Get search parameters
    search = request.GET.get('search', '')
    document_type_id = request.GET.get('document_type', '')
    facility_id = request.GET.get('facility', '')
    gbv_category_id = request.GET.get('gbv_category', '')
    
    # Base queryset with optimized relationships
    documents = Document.objects.select_related(
        'document_type', 'gbv_category', 'facility',
        'facility__ward__constituency__county',
        'facility__operational_status'
    ).prefetch_related(
        'facility__facilitygbvcategory_set__gbv_category'
    )
    
    # Apply filters
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(document_type__type_name__icontains=search) |
            Q(facility__facility_name__icontains=search)
        )
    
    if document_type_id:
        documents = documents.filter(document_type_id=document_type_id)
    
    if facility_id:
        documents = documents.filter(facility_id=facility_id)
    
    if gbv_category_id:
        documents = documents.filter(gbv_category_id=gbv_category_id)
    
    # Get statistics
    total_documents = documents.count()
    total_document_types = documents.values('document_type').distinct().count()
    total_facilities_with_docs = documents.values('facility').distinct().count()
    total_gbv_categories = documents.values('gbv_category').distinct().count()
    
    # Group documents by type for summary
    documents_by_type = {}
    for doc in documents:
        if doc.document_type:
            type_name = doc.document_type.type_name
            if type_name not in documents_by_type:
                documents_by_type[type_name] = {
                    'documents': [],
                    'facilities': set(),
                    'document_type_id': doc.document_type.document_type_id
                }
            documents_by_type[type_name]['documents'].append(doc)
            if doc.facility:
                documents_by_type[type_name]['facilities'].add(doc.facility.facility_id)
    
    # Convert sets to counts for template usage
    for type_data in documents_by_type.values():
        type_data['facility_count'] = len(type_data['facilities'])
        type_data['document_count'] = len(type_data['documents'])
    
    # Pagination
    paginator = Paginator(documents.order_by('document_type__type_name', 'title'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    document_types = DocumentType.objects.all().order_by('type_name')
    gbv_categories = GBVCategory.objects.all().order_by('category_name')
    facilities_with_docs = Facility.objects.filter(
        active_status=True,
        document__isnull=False
    ).distinct().order_by('facility_name')
    
    context = {
        'segment': 'documents',
        'page_title': 'Documents',
        'page_obj': page_obj,
        'documents': documents,
        'documents_by_type': documents_by_type,
        'document_types': document_types,
        'gbv_categories': gbv_categories,
        'facilities_with_docs': facilities_with_docs,
        'search': search,
        'selected_document_type': document_type_id,
        'selected_facility': facility_id,
        'selected_gbv_category': gbv_category_id,
        'total_documents': total_documents,
        'total_document_types': total_document_types,
        'total_facilities_with_docs': total_facilities_with_docs,
        'total_gbv_categories': total_gbv_categories,
    }
    
    return render(request, 'home/documents.html', context)


def add_document(request):
    """Add Document Page"""
    from apps.common.lookups import DocumentType, GBVCategory
    from django.utils import timezone
    
    if request.method == 'POST':
        # Handle document creation
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        file_url = request.POST.get('file_url')
        document_type_id = request.POST.get('document_type')
        gbv_category_id = request.POST.get('gbv_category', '')
        facility_id = request.POST.get('facility', '')
        
        # Basic validation
        if not title or not file_url or not document_type_id:
            messages.error(request, 'Title, File URL, and Document Type are required fields.')
            return redirect('add_document')
        
        try:
            # Create document
            document = Document.objects.create(
                title=title,
                description=description,
                file_url=file_url,
                document_type_id=document_type_id,
                gbv_category_id=gbv_category_id if gbv_category_id else None,
                facility_id=facility_id if facility_id else None,
                uploaded_at=timezone.now()
            )
            
            messages.success(request, f'Document "{title}" created successfully!')
            return redirect('document_detail', document_id=document.document_id)
            
        except Exception as e:
            messages.error(request, f'Error creating document: {str(e)}')
            return redirect('add_document')
    
    # GET request - show form
    document_types = DocumentType.objects.all().order_by('type_name')
    gbv_categories = GBVCategory.objects.all().order_by('category_name')
    facilities = Facility.objects.filter(active_status=True).order_by('facility_name')
    
    context = {
        'segment': 'documents',
        'page_title': 'Add New Document',
        'document_types': document_types,
        'gbv_categories': gbv_categories,
        'facilities': facilities,
        'is_update': False,
    }
    
    return render(request, 'home/add_document.html', context)


def document_detail(request, document_id):
    """Document Detail Page"""
    from apps.common.documents import Document
    
    document = get_object_or_404(Document, document_id=document_id)
    
    context = {
        'segment': 'documents',
        'page_title': f'Document - {document.title}',
        'document': document,
    }
    
    return render(request, 'home/document_detail.html', context)


def document_update(request, document_id):
    """Document Update Page"""
    from apps.common.lookups import DocumentType, GBVCategory
    from django.utils import timezone
    
    document = get_object_or_404(Document, document_id=document_id)
    
    if request.method == 'POST':
        # Handle document update
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        file_url = request.POST.get('file_url')
        document_type_id = request.POST.get('document_type')
        gbv_category_id = request.POST.get('gbv_category', '')
        facility_id = request.POST.get('facility', '')
        
        # Basic validation
        if not title or not file_url or not document_type_id:
            messages.error(request, 'Title, File URL, and Document Type are required fields.')
            return redirect('document_update', document_id=document_id)
        
        try:
            # Update document
            document.title = title
            document.description = description
            document.file_url = file_url
            document.document_type_id = document_type_id
            document.gbv_category_id = gbv_category_id if gbv_category_id else None
            document.facility_id = facility_id if facility_id else None
            document.save()
            
            messages.success(request, f'Document "{title}" updated successfully!')
            return redirect('document_detail', document_id=document.document_id)
            
        except Exception as e:
            messages.error(request, f'Error updating document: {str(e)}')
            return redirect('document_update', document_id=document_id)
    
    # GET request or form errors - show form
    document_types = DocumentType.objects.all().order_by('type_name')
    gbv_categories = GBVCategory.objects.all().order_by('category_name')
    facilities = Facility.objects.filter(active_status=True).order_by('facility_name')
    
    context = {
        'segment': 'documents',
        'page_title': f'Edit Document - {document.title}',
        'document': document,
        'document_types': document_types,
        'gbv_categories': gbv_categories,
        'facilities': facilities,
        'is_update': True,
    }
    
    return render(request, 'home/add_document.html', context)


def document_delete(request, document_id):
    """Document Delete Page"""
    from apps.common.documents import Document
    
    document = get_object_or_404(Document, document_id=document_id)
    
    if request.method == 'POST':
        document_title = document.title
        document.delete()
        messages.success(request, f'Document "{document_title}" deleted successfully!')
        return redirect('documents')
    
    context = {
        'segment': 'documents',
        'page_title': f'Delete Document - {document.title}',
        'document': document,
    }
    
    return render(request, 'home/document_delete.html', context)


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
        
    except loader.TemplateDoesNotExist:
        # Try to find the template in the accounts directory
        try:
            html_template = loader.get_template('accounts/' + load_template)
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
    <a href="/">Return to Home</a>
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
    <a href="/">Return to Home</a>
</body>
</html>
        """
        return HttpResponse(error_html)
