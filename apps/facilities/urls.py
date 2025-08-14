from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    # User URLs
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Facility URLs
    path('facilities/', views.FacilityListCreateView.as_view(), name='facility-list-create'),
    path('facilities/<int:id>/', views.FacilityDetailView.as_view(), name='facility-detail'),
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
    
    # GBV URLs
    path('gbv-categories/', views.GbvCategoryListCreateView.as_view(), name='gbv-category-list-create'),
    path('gbv-categories/<int:gbv_category_id>/', views.GbvCategoryDetailView.as_view(), name='gbv-category-detail'),

    # Document URLs
    path('documents/', views.DocumentListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:document_id>/', views.DocumentDetailView.as_view(), name='document-detail'),

    # Contact Click URLs
    path('contact-clicks/', views.ContactClickListCreateView.as_view(), name='contact-click-list-create'),
    path('contact-clicks/<int:click_id>/', views.ContactClickDetailView.as_view(), name='contact-click-detail'),

    # DocumentType URLs
    path('document-types/', views.DocumentTypeListCreateView.as_view(), name='document-type-list-create'),
    path('document-types/<int:document_type_id>/', views.DocumentTypeDetailView.as_view(), name='document-type-detail'),
]