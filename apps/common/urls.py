# -*- encoding: utf-8 -*-
"""
URL patterns for common app
"""

from django.urls import path
from . import views
from . import settings_views

app_name = 'common'

urlpatterns = [
    path('geography/', views.geography_overview, name='geography_overview'),
    path('geography/county/<int:county_id>/', views.county_detail, name='county_detail'),
    path('geography/constituency/<int:constituency_id>/', views.constituency_detail, name='constituency_detail'),
    path('geography/ward/<int:ward_id>/', views.ward_detail, name='ward_detail'),
    path('lookups/', views.lookup_tables, name='lookup_tables'),
    
    # Operational Status CRUD
    path('lookups/operational-status/add/', views.add_operational_status, name='add_operational_status'),
    path('lookups/operational-status/<int:status_id>/edit/', views.edit_operational_status, name='edit_operational_status'),
    path('lookups/operational-status/<int:status_id>/delete/', views.delete_operational_status, name='delete_operational_status'),
    
    # Contact Type CRUD
    path('lookups/contact-type/add/', views.add_contact_type, name='add_contact_type'),
    path('lookups/contact-type/<int:type_id>/edit/', views.edit_contact_type, name='edit_contact_type'),
    path('lookups/contact-type/<int:type_id>/delete/', views.delete_contact_type, name='delete_contact_type'),
    
    # Service Category CRUD
    path('lookups/service-category/add/', views.add_service_category, name='add_service_category'),
    path('lookups/service-category/<int:category_id>/edit/', views.edit_service_category, name='edit_service_category'),
    path('lookups/service-category/<int:category_id>/delete/', views.delete_service_category, name='delete_service_category'),
    
    # Owner Type CRUD
    path('lookups/owner-type/add/', views.add_owner_type, name='add_owner_type'),
    path('lookups/owner-type/<int:type_id>/edit/', views.edit_owner_type, name='edit_owner_type'),
    path('lookups/owner-type/<int:type_id>/delete/', views.delete_owner_type, name='delete_owner_type'),
    
    # GBV Category CRUD
    path('lookups/gbv-category/add/', views.add_gbv_category, name='add_gbv_category'),
    path('lookups/gbv-category/<int:category_id>/edit/', views.edit_gbv_category, name='edit_gbv_category'),
    path('lookups/gbv-category/<int:category_id>/delete/', views.delete_gbv_category, name='delete_gbv_category'),
    
    # Infrastructure Type CRUD
    path('lookups/infrastructure-type/add/', views.add_infrastructure_type, name='add_infrastructure_type'),
    path('lookups/infrastructure-type/<int:type_id>/edit/', views.edit_infrastructure_type, name='edit_infrastructure_type'),
    path('lookups/infrastructure-type/<int:type_id>/delete/', views.delete_infrastructure_type, name='delete_infrastructure_type'),
    
    # Condition Status CRUD
    path('lookups/condition-status/add/', views.add_condition_status, name='add_condition_status'),
    path('lookups/condition-status/<int:status_id>/edit/', views.edit_condition_status, name='edit_condition_status'),
    path('lookups/condition-status/<int:status_id>/delete/', views.delete_condition_status, name='delete_condition_status'),
    
    # Document Type CRUD
    path('lookups/document-type/add/', views.add_document_type, name='add_document_type'),
    path('lookups/document-type/<int:type_id>/edit/', views.edit_document_type, name='edit_document_type'),
    path('lookups/document-type/<int:type_id>/delete/', views.delete_document_type, name='delete_document_type'),
    
    # Application Settings
    path('settings/', settings_views.application_settings, name='application_settings'),
    path('settings/preview-theme/', settings_views.preview_theme, name='preview_theme'),
    path('settings/reset-theme/', settings_views.reset_theme_colors, name='reset_theme_colors'),
    path('settings/delete-logo/', settings_views.delete_logo, name='delete_logo'),
    path('settings/delete-favicon/', settings_views.delete_favicon, name='delete_favicon'),
    path('settings/delete-apple-touch-icon/', settings_views.delete_apple_touch_icon, name='delete_apple_touch_icon'),
    path('settings/load-defaults/', settings_views.load_default_roles_permissions, name='load_default_roles_permissions'),
    path('settings/test-state/', settings_views.test_roles_permissions, name='test_roles_permissions'),
]
