

"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ✅ FIX: import functions directly instead of api_views/health_views modules
from apps.api import views as api_views

try:
    from rest_framework.authtoken.views import obtain_auth_token
except:
    pass

# ------------------------------
# Health Check View
# ------------------------------
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        "status": "healthy",
        "service": "GVRC Admin",
        "timestamp": "2025-08-16"
    })

# ------------------------------
# API URL patterns
# ------------------------------
api_patterns = [
    path('hello/', api_views.hello_world, name='hello_world'),
    path('status/', api_views.api_status, name='api_status'),
    path('test/', api_views.my_endpoint, name='my_endpoint'),
    path('public/', api_views.public_endpoint, name='public_endpoint'),
    path('run-tests/', api_views.run_tests_api, name='run_tests_api'),
    path('health/', health_check, name='api_health'),  # Health check in API
]

# ------------------------------
# Swagger/OpenAPI schema
# ------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="GVRC Admin API",
        default_version='v1',
        description="API documentation for GVRC Admin Project",
        contact=openapi.Contact(email="admin@gvrc.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ------------------------------
# Main URL patterns
# ------------------------------
urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Health check endpoint (root level)
    path("health/", health_check, name='health'),

    # App routes
    path("", include("apps.home.urls")),             # Home
    path("", include("apps.authentication.urls")),  # Authentication
    path("", include("admin_gradient.urls")),       # Admin theme

    # API routes
    path("api/v1/", include(api_patterns)),  

    # Swagger / API docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Lazy-load on routing is needed
try:
    urlpatterns.append(path("", include("django_dyn_api.urls")))
    urlpatterns.append(path("login/jwt/", view=obtain_auth_token))
except:
    pass