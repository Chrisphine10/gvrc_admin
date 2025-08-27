from django.urls import path
from .views import health_check, health_detailed

app_name = 'health'

urlpatterns = [
    path('', health_check, name='health-check'),
    path('detailed/', health_detailed, name='health-detailed'),
]