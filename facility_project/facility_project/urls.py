from django.urls import path, include
from rest_framework.routers import DefaultRouter
from facilities import views

urlpatterns = [
    path('api/', include([
        # Authentication URLs
        path('auth/login/', views.login_view, name='login'),
        path('auth/register/', views.register_view, name='register'),
        path('auth/logout/', views.logout_view, name='logout'),
        
        # User URLs
        path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
        path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user-detail'),
        path('users/profile/', views.UserProfileView.as_view(), name='user-profile'),
        
        # Facility URLs
        path('facilities/', views.FacilityListCreateView.as_view(), name='facility-list-create'),
        path('facilities/<int:facility_id>/', views.FacilityDetailView.as_view(), name='facility-detail'),
        path('facilities/search/', views.FacilitySearchView.as_view(), name='facility-search'),
        
        # Facility Related URLs
        path('facilities/<int:facility_id>/contacts/',
             views.FacilityContactListCreateView.as_view(),
             name='facility-contact-list-create'),
        path('facility-contacts/<int:contact_id>/',
             views.FacilityContactDetailView.as_view(),
             name='facility-contact-detail'),
        
        path('facilities/<int:facility_id>/coordinates/',
             views.FacilityCoordinateView.as_view(),
             name='facility-coordinate'),
        
        path('facilities/<int:facility_id>/services/',
             views.FacilityServiceListCreateView.as_view(),
             name='facility-service-list-create'),
        path('facility-services/<int:service_id>/',
             views.FacilityServiceDetailView.as_view(),
             name='facility-service-detail'),
        
        path('facilities/<int:facility_id>/owners/',
             views.FacilityOwnerListCreateView.as_view(),
             name='facility-owner-list-create'),
        path('facility-owners/<int:owner_id>/',
             views.FacilityOwnerDetailView.as_view(),
             name='facility-owner-detail'),
        
        # Location URLs
        path('counties/', views.CountyListView.as_view(), name='county-list'),
        path('constituencies/', views.ConstituencyListView.as_view(), name='constituency-list'),
        path('wards/', views.WardListView.as_view(), name='ward-list'),
        
        # Lookup URLs
        path('operational-statuses/', views.OperationalStatusListView.as_view(), name='operational-status-list'),
        path('contact-types/', views.ContactTypeListView.as_view(), name='contact-type-list'),
        path('service-categories/', views.ServiceCategoryListView.as_view(), name='service-category-list'),
        path('owner-types/', views.OwnerTypeListView.as_view(), name='owner-type-list'),
        
        # User Location URLs
        path('user-locations/', views.UserLocationListCreateView.as_view(), name='user-location-list-create'),
        path('user-locations/<int:location_id>/', views.UserLocationDetailView.as_view(), name='user-location-detail'),
        
        # Session URLs
        path('user-sessions/', views.UserSessionListView.as_view(), name='user-session-list'),
        
        # Dashboard URLs
        path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
        path('facilities/nearby/', views.nearby_facilities, name='nearby-facilities'),
    ])),
]