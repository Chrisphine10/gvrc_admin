from django.urls import path
from . import views

app_name = 'geography'

urlpatterns = [
    path('api/constituencies/<int:county_id>/', views.get_constituencies, name='get_constituencies'),
    path('api/wards/<int:constituency_id>/', views.get_wards, name='get_wards'),
    path('api/search/', views.search_geography, name='search_geography'),
    path('api/add/', views.add_geography_item, name='add_geography_item'),
]

