# -*- encoding: utf-8 -*-
"""
Document management views for GVRC Admin
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import Document
from .forms import DocumentForm, DocumentUploadForm
from apps.lookups.models import DocumentType, GBVCategory


@login_required
def document_list(request):
    """Display list of documents with filtering and search"""
    # Get filter parameters
    search_query = request.GET.get('search', '')
    document_type_id = request.GET.get('document_type', '')
    is_public = request.GET.get('is_public', '')
    is_active = request.GET.get('is_active', '')
    
    # Base queryset
    documents = Document.objects.select_related(
        'document_type', 'uploaded_by', 'gbv_category'
    ).filter(is_active=True)
    
    # Apply filters
    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(file_name__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if document_type_id:
        documents = documents.filter(document_type_id=document_type_id)
    
    if is_public != '':
        documents = documents.filter(is_public=is_public == 'true')
    
    if is_active != '':
        documents = documents.filter(is_active=is_active == 'true')
    
    # Get filter options
    document_types = DocumentType.objects.all().order_by('type_name')
    gbv_categories = GBVCategory.objects.all().order_by('category_name')
    
    # Pagination
    paginator = Paginator(documents.order_by('-uploaded_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_documents = documents.count()
    public_documents = documents.filter(is_public=True).count()
    private_documents = documents.filter(is_public=False).count()
    
    context = {
        'segment': 'documents',
        'page_title': 'Document Management',
        'page_obj': page_obj,
        'documents': page_obj,
        'document_types': document_types,
        'gbv_categories': gbv_categories,
        'search_query': search_query,
        'selected_document_type': document_type_id,
        'selected_is_public': is_public,
        'selected_is_active': is_active,
        'total_documents': total_documents,
        'public_documents': public_documents,
        'private_documents': private_documents,
    }
    
    return render(request, 'documents/document_list.html', context)


@login_required
def document_detail(request, document_id):
    """Display detailed information about a specific document"""
    document = get_object_or_404(
        Document.objects.select_related(
            'document_type', 'uploaded_by', 'gbv_category'
        ),
        document_id=document_id,
        is_active=True
    )
    
    context = {
        'segment': 'documents',
        'page_title': f'Document: {document.title}',
        'document': document,
    }
    
    return render(request, 'documents/document_detail.html', context)


@login_required
def document_create(request):
    """Create a new document"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                document = form.save(commit=False)
                document.uploaded_by = request.user
                document.save()
                
                messages.success(request, f'Document "{document.title}" created successfully.')
                return redirect('documents:document_list')
                
            except Exception as e:
                messages.error(request, f'Error creating document: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DocumentForm()
    
    # GET request - show form
    context = {
        'segment': 'documents',
        'page_title': 'Create New Document',
        'action': 'Create',
        'form': form,
        'document_types': DocumentType.objects.all().order_by('type_name'),
        'gbv_categories': GBVCategory.objects.all().order_by('category_name'),
    }
    
    return render(request, 'documents/document_form.html', context)


@login_required
def document_edit(request, document_id):
    """Edit an existing document"""
    document = get_object_or_404(
        Document.objects.select_related('document_type', 'gbv_category'),
        document_id=document_id,
        is_active=True
    )
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            try:
                document = form.save()
                messages.success(request, f'Document "{document.title}" updated successfully.')
                return redirect('documents:document_list')
                
            except Exception as e:
                messages.error(request, f'Error updating document: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DocumentForm(instance=document)
    
    context = {
        'segment': 'documents',
        'page_title': f'Edit Document: {document.title}',
        'action': 'Edit',
        'form': form,
        'document': document,
        'document_types': DocumentType.objects.all().order_by('type_name'),
        'gbv_categories': GBVCategory.objects.all().order_by('category_name'),
    }
    
    return render(request, 'documents/document_form.html', context)


@login_required
def document_delete(request, document_id):
    """Delete a document (soft delete by setting is_active=False)"""
    document = get_object_or_404(
        Document.objects.select_related('document_type'),
        document_id=document_id,
        is_active=True
    )
    
    if request.method == 'POST':
        try:
            document.is_active = False
            document.save()
            messages.success(request, f'Document "{document.title}" deleted successfully.')
            return redirect('document_list')
        except Exception as e:
            messages.error(request, f'Error deleting document: {str(e)}')
            return redirect('document_detail', document_id=document_id)
    
    # GET request - show confirmation
    context = {
        'segment': 'documents',
        'page_title': f'Delete Document: {document.title}',
        'document': document,
    }
    
    return render(request, 'documents/document_confirm_delete.html', context)


@login_required
def document_toggle_public(request, document_id):
    """Toggle document public/private status via AJAX"""
    if request.method == 'POST':
        try:
            document = get_object_or_404(Document, document_id=document_id, is_active=True)
            document.is_public = not document.is_public
            document.save()
            
            return JsonResponse({
                'success': True,
                'is_public': document.is_public,
                'message': f'Document is now {"public" if document.is_public else "private"}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def document_analytics(request):
    """Display document analytics and statistics"""
    from django.core.serializers.json import DjangoJSONEncoder
    import json
    
    # Get basic statistics from Document model
    total_documents = Document.objects.filter(is_active=True).count()
    public_documents = Document.objects.filter(is_active=True, is_public=True).count()
    private_documents = Document.objects.filter(is_active=True, is_public=False).count()
    
    # Documents by type - using Document model with related DocumentType
    documents_by_type = Document.objects.filter(is_active=True).values(
        'document_type__type_name'
    ).annotate(
        count=Count('document_id')
    ).order_by('-count')
    
    # Documents by month (last 12 months) - using Document model's uploaded_at field
    from datetime import datetime, timedelta
    months = []
    counts = []
    
    for i in range(12):
        date = datetime.now() - timedelta(days=30*i)
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(seconds=1)
        
        # Count documents from Document model within date range
        count = Document.objects.filter(
            is_active=True,
            uploaded_at__range=(month_start, month_end)
        ).count()
        
        months.append(month_start.strftime('%b %Y'))
        counts.append(count)
    
    # Recent uploads - using Document model with related data
    recent_documents = Document.objects.filter(
        is_active=True
    ).select_related(
        'document_type', 'uploaded_by'
    ).order_by('-uploaded_at')[:10]
    
    # Serialize data for JSON consumption in template
    documents_by_type_json = json.dumps(list(documents_by_type), cls=DjangoJSONEncoder)
    months_json = json.dumps(months, cls=DjangoJSONEncoder)
    counts_json = json.dumps(counts, cls=DjangoJSONEncoder)
    
    context = {
        'segment': 'document_analytics',
        'page_title': 'Document Analytics',
        'total_documents': total_documents,
        'public_documents': public_documents,
        'private_documents': private_documents,
        'documents_by_type': documents_by_type,
        'documents_by_type_json': documents_by_type_json,
        'months': months,
        'months_json': months_json,
        'counts': counts,
        'counts_json': counts_json,
        'recent_documents': recent_documents,
    }
    
    return render(request, 'documents/document_analytics.html', context)
