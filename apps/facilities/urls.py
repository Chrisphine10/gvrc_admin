# -*- encoding: utf-8 -*-
"""
URL patterns for facilities app
"""

from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    path('', views.facility_list, name='facility_list'),
    path('create/', views.facility_create, name='facility_create'),
    path('<int:facility_id>/', views.facility_detail, name='facility_detail'),
    path('<int:facility_id>/edit/', views.facility_update, name='facility_update'),
    path('map/', views.facility_map, name='facility_map'),
]
