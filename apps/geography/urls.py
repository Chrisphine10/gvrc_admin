from django.urls import path
from . import views

app_name = 'geography'

urlpatterns = [
    path('api/constituencies/<int:county_id>/', views.get_constituencies, name='get_constituencies'),
    path('api/wards/<int:constituency_id>/', views.get_wards, name='get_wards'),
    path('api/search/', views.search_geography, name='search_geography'),
    path('api/add/', views.add_geography_item, name='add_geography_item'),
    path('api/edit/', views.edit_geography_item, name='edit_geography_item'),
    path('api/delete/', views.delete_geography_item, name='delete_geography_item'),
    path('api/counties/', views.get_all_counties, name='get_all_counties'),
    path('api/constituencies/', views.get_all_constituencies, name='get_all_constituencies'),
    path('api/check-facilities/', views.check_facility_connections, name='check_facility_connections'),
]

