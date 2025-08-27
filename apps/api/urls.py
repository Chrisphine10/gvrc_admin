# -*- encoding: utf-8 -*-
"""
API URLs
"""

from django.urls import path
from .views import (
    hello_world, api_status, my_endpoint, public_endpoint,
    test_runner_page, run_tests_api,
    clear_cache, post_list, user_list
)
from .user_management import create_user

app_name = 'api'

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('status/', api_status, name='status'),
    path('endpoint/', my_endpoint, name='endpoint'),  # Protected endpoint
    path('public/', public_endpoint, name='public'),  # Public endpoint
    path('create-user/', create_user, name='create_user'),  # User creation with email
    path('test-runner/', test_runner_page, name='test_runner'),  # Web test runner
    path('run-tests/', run_tests_api, name='run_tests'),  # Run tests API

    # 🔥 Missing endpoints you were testing
    path('cache/clear/', clear_cache, name='clear_cache'),
    path('posts/', post_list, name='post_list'),
    path('users/', user_list, name='user_list'),
]
