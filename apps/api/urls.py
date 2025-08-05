# -*- encoding: utf-8 -*-
"""
API URLs
"""

from django.urls import path
from .views import hello_world, api_status

app_name = 'api'

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('status/', api_status, name='status'),
]