# -*- encoding: utf-8 -*-
"""
URLs for monitoring app
"""

from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('', views.monitoring_dashboard, name='dashboard'),
    path('health/', views.health_check, name='health_check'),
    path('system/', views.system_metrics, name='system_metrics'),
    path('database/', views.database_metrics, name='database_metrics'),
    path('application/', views.application_metrics, name='application_metrics'),
    path('status/', views.full_status, name='full_status'),
]

