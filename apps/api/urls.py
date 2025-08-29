# -*- encoding: utf-8 -*-
"""
Admin/Management API URLs for GVRC Admin
"""
from apps.core.views import clear_cache_view

from django.urls import path
from django.conf import settings
from apps.core.views import clear_cache_view  # Import your cache clear view
from .views import (
    # Facility endpoints
    FacilityListView, FacilityDetailView, FacilityMapView, FacilitySearchView,
    FacilityCompleteView,
    # Specialized GBV endpoints
    EmergencyServicesView, GBVServicesView, ReferralChainView,
    # Analytics endpoints
    ContactInteractionAnalyticsView, ReferralOutcomeView,
    # Statistics and lookup data
    StatisticsView, LookupDataView,
    # Geography endpoints
    CountyListView, ConstituencyListView, WardListView, ConsolidatedGeographyView,
    # Authentication endpoints
    obtain_api_token,
    # Utility endpoints
    api_status, hello_world,
    # User management endpoints
    UserListView,
)

app_name = 'api'

urlpatterns = [
    # Core facility management endpoints
    path('facilities/', FacilityListView.as_view(), name='facility-list'),
    path('facilities/<int:facility_id>/', FacilityDetailView.as_view(), name='facility-detail'),
    path('facilities/<int:facility_id>/complete/', FacilityCompleteView.as_view(), name='facility-complete'),
    path('facilities/map/', FacilityMapView.as_view(), name='facility-map'),
    path('facilities/search/', FacilitySearchView.as_view(), name='facility-search'),
    
    # Specialized GBV response endpoints
    path('facilities/emergency/', EmergencyServicesView.as_view(), name='emergency-services'),
    path('facilities/gbv-services/', GBVServicesView.as_view(), name='gbv-services'),
    path('facilities/referral-chain/', ReferralChainView.as_view(), name='referral-chain'),
    
    # Analytics and tracking endpoints
    path('analytics/contact-interaction/', ContactInteractionAnalyticsView.as_view(), name='contact-interaction'),
    path('analytics/referral-outcome/', ReferralOutcomeView.as_view(), name='referral-outcome'),
    
    # Authentication endpoints
    path('auth/token/', obtain_api_token, name='obtain-api-token'),
    
    # Statistics and lookup data
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('lookups/', LookupDataView.as_view(), name='lookup-data'),
    
    # Geography endpoints
    path('geography/', ConsolidatedGeographyView.as_view(), name='geography-consolidated'),
    path('geography/counties/', CountyListView.as_view(), name='county-list'),
    path('geography/constituencies/', ConstituencyListView.as_view(), name='constituency-list'),
    path('geography/wards/', WardListView.as_view(), name='ward-list'),
    
    # User management endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    
    # Utility endpoints
    path('status/', api_status, name='api-status'),
    path('hello/', hello_world, name='hello-world'),
]

# Only include the cache clear endpoint in DEBUG mode
if settings.DEBUG:
    urlpatterns += [
        path('cache/clear/', clear_cache_view, name='api-cache-clear'),
    ]
