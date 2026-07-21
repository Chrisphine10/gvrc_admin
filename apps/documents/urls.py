# -*- encoding: utf-8 -*-
"""
URL configuration for documents app
"""

from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # Document management
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('<int:document_id>/', views.document_detail, name='document_detail'),
    path('<int:document_id>/edit/', views.document_edit, name='document_edit'),
    path('<int:document_id>/delete/', views.document_delete, name='document_delete'),
    
    # AJAX endpoints
    path('<int:document_id>/toggle-public/', views.document_toggle_public, name='document_toggle_public'),
    
    # Analytics
    path('analytics/', views.document_analytics, name='document_analytics'),
]
