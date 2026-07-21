# -*- encoding: utf-8 -*-
"""
Mobile App API URL Configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Mobile Chat endpoints
    MobileChatViewSet,
    # Mobile Facility endpoints
    MobileFacilityViewSet,
    # Mobile Session endpoints
    MobileSessionViewSet,
    # Mobile Music endpoints
    MobileMusicViewSet,
    # Mobile Document endpoints
    MobileDocumentViewSet,
    # Mobile Emergency endpoints
    MobileEmergencyViewSet,
    # Mobile Lookup endpoints
    MobileLookupViewSet,
    # Mobile Analytics endpoints
    MobileAnalyticsViewSet,
)

# Create routers for different mobile API sections
mobile_chat_router = DefaultRouter()
mobile_chat_router.register(r'chat', MobileChatViewSet, basename='mobile-chat')

mobile_facility_router = DefaultRouter()
mobile_facility_router.register(r'facilities', MobileFacilityViewSet, basename='mobile-facility')

mobile_session_router = DefaultRouter()
mobile_session_router.register(r'sessions', MobileSessionViewSet, basename='mobile-session')

mobile_music_router = DefaultRouter()
mobile_music_router.register(r'music', MobileMusicViewSet, basename='mobile-music')

mobile_document_router = DefaultRouter()
mobile_document_router.register(r'documents', MobileDocumentViewSet, basename='mobile-document')

mobile_emergency_router = DefaultRouter()
mobile_emergency_router.register(r'emergency', MobileEmergencyViewSet, basename='mobile-emergency')

mobile_lookup_router = DefaultRouter()
mobile_lookup_router.register(r'lookups', MobileLookupViewSet, basename='mobile-lookup')

mobile_analytics_router = DefaultRouter()
mobile_analytics_router.register(r'analytics', MobileAnalyticsViewSet, basename='mobile-analytics')

app_name = 'mobile'

urlpatterns = [
    # Mobile Chat System
    path('', include(mobile_chat_router.urls)),
    
    # Mobile Facilities
    path('', include(mobile_facility_router.urls)),
    
    # Mobile Sessions
    path('', include(mobile_session_router.urls)),
    
    # Mobile Music
    path('', include(mobile_music_router.urls)),
    
    # Mobile Documents
    path('', include(mobile_document_router.urls)),
    
    # Mobile Emergency Services
    path('', include(mobile_emergency_router.urls)),
    
    # Mobile Lookups
    path('', include(mobile_lookup_router.urls)),
    
    # Mobile Analytics
    path('', include(mobile_analytics_router.urls)),
]
