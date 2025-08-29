# apps/core/urls.py
from django.urls import path
from .views import clear_cache_view, posts_list, health_check, UserListView

app_name = 'core'

urlpatterns = [
    # Clear cache endpoint
    path('cache/clear/', clear_cache_view, name='cache-clear'),

    # Posts list endpoint
    path('posts/', posts_list, name='posts-list'),

    # Health check endpoint
    path('health/', health_check, name='health'),

    # Optional: user list for testing
    path('users/', UserListView.as_view(), name='user-list'),
]
