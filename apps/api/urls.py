# -*- encoding: utf-8 -*-
"""
API URLs
"""

from django.urls import path
from .views import hello_world, api_status, my_endpoint, public_endpoint

app_name = 'api'

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('status/', api_status, name='status'),
    path('endpoint/', my_endpoint, name='endpoint'),  # Protected endpoint
    path('public/', public_endpoint, name='public'),  # Public endpoint
]
