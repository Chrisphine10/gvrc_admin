# -*- encoding: utf-8 -*-
"""
API URLs
"""

from django.urls import path, include
from .views import hello_world, api_status

app_name = 'api'

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('status/', api_status, name='status'),
    path('facilities/', include('apps.facilities.urls')),
]