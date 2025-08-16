# -*- encoding: utf-8 -*-
"""
URL patterns for common app
"""

from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('geography/', views.geography_overview, name='geography_overview'),
    path('geography/county/<int:county_id>/', views.county_detail, name='county_detail'),
    path('geography/constituency/<int:constituency_id>/', views.constituency_detail, name='constituency_detail'),
    path('geography/ward/<int:ward_id>/', views.ward_detail, name='ward_detail'),
    path('lookups/', views.lookup_tables, name='lookup_tables'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),
]
