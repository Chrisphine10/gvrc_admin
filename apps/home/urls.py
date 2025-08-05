# -*- encoding: utf-8 -*-
"""
Home app URLs
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('', views.index, name='index'),  # Backward compatibility
]
