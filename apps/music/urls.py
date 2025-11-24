# -*- encoding: utf-8 -*-
"""
Music URL Configuration
"""

from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.music_list, name='music_list'),
    path('add/', views.add_music, name='add_music'),
    path('<int:music_id>/', views.music_detail, name='music_detail'),
    path('<int:music_id>/edit/', views.edit_music, name='edit_music'),
    path('analytics/', views.music_analytics, name='music_analytics'),
    path('api/track-play/', views.track_play, name='track_play'),
]
