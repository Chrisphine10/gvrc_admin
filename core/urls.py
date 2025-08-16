# -*- encoding: utf-8 -*-
"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

try:
    from rest_framework.authtoken.views import obtain_auth_token
except:
    pass

# Swagger / OpenAPI schema views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GVRC Admin API",
        default_version='v1',
        description="Multi-Institutional GBV Response Platform API - Comprehensive endpoints for police, hospitals, NGOs, safe houses, legal aid centers, and all GBV response institutions",
        contact=openapi.Contact(email="admin@gvrc.com"),
        license=openapi.License(name="Internal Use Only"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.authentication.urls")), # Authentication at root
    path("", include("apps.home.urls")),          # Home
    path("facilities/", include("apps.facilities.urls")), # Facilities
    path("common/", include("apps.common.urls")), # Common
    path("api/", include("apps.api.urls")),       # APIs
    path("", include("admin_gradient.urls")),     # Admin theme
    # Swagger / ReDoc documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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
