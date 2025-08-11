# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page (public)
    path('', views.index, name='home'),
    
    # Protected dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Main resource pages
    path('facilities/', views.community_facilities, name='facilities'),
    path('facilities/add/', views.add_facility, name='add_facility'),
    path('services/', views.services_programs, name='services'),
    path('services/add/', views.add_service, name='add_service'),
    path('human-resources/', views.human_resources, name='human_resources'),
    path('human-resources/add/', views.add_staff, name='add_staff'),
    path('infrastructure/', views.infrastructure, name='infrastructure'),
    path('infrastructure/add/', views.add_equipment, name='add_equipment'),

    # Protected pages that should be handled by home app
    path('profile/', views.pages, name='profile'),
    path('billing/', views.pages, name='billing'),
    path('rtl/', views.pages, name='rtl'),
    path('vr/', views.pages, name='vr'),
    path('new-user/', views.pages, name='new-user'),
    path('icons/', views.pages, name='icons'),
    path('notifications/', views.pages, name='notifications'),
    path('tables/', views.pages, name='tables'),
    path('upgrade/', views.pages, name='upgrade'),
    path('help/', views.pages, name='help'),

]
