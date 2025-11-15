# -*- encoding: utf-8 -*-
"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

try:
    from rest_framework.authtoken.views import obtain_auth_token
except:
    pass

# Swagger / OpenAPI schema views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Limit Swagger schema generation to API endpoints only to avoid duplicated routes
api_urlpatterns = [
    path("api/", include("apps.api.urls")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Hodi Admin API",
        default_version='v1',
        description="Hodi App Management Dashboard API - Comprehensive endpoints for managing the Hodi app for GVRC",
        contact=openapi.Contact(email="admin@hodi.ke"),
        license=openapi.License(name="Internal Use Only"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
    patterns=api_urlpatterns,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.authentication.urls")), # Authentication at root
    path("", include("apps.home.urls")),          # Home
    path("facilities/", include("apps.facilities.urls")), # Facilities
    path("geography/", include("apps.geography.urls")), # Geography
    path("common/", include("apps.common.urls")), # Common
    
    # Mobile API endpoints (no authentication required)
    path("mobile/", include("apps.mobile.urls")), # Mobile App APIs
    
    # Admin/Management API endpoints (authentication required)
    *api_urlpatterns,

    # Web interface endpoints
    path("chat/", include("apps.chat.urls")),     # Emergency Chat System Web Interface
    path("music/", include("apps.music.urls")),   # Music
    path("documents/", include("apps.documents.urls")), # Documents
    
    # Swagger / ReDoc documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Favicon route for better browser compatibility
    path('favicon.ico', RedirectView.as_view(url='/static/assets/img/icons/common/favicon.ico', permanent=True)),
]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Lazy-load on routing is needed
# During the first build, API is not yet generated
try:
    urlpatterns.append(path("", include("django_dyn_api.urls")))
    urlpatterns.append(path("api/auth/token/", view=obtain_auth_token, name='api_token_auth'))
except:
    pass
