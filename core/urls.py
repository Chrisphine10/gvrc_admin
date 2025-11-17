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
from drf_yasg.generators import OpenAPISchemaGenerator
from django.conf import settings

# Limit Swagger schema generation to API endpoints only to avoid duplicated routes
api_urlpatterns = [
    path("api/", include("apps.api.urls")),
]

# Custom schema generator that uses HTTPS for production
class HTTPSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request=request, public=public)
        
        # Determine the scheme from request or settings
        if request:
            # Check if request is secure (HTTPS) via multiple methods
            is_secure = (
                request.is_secure() or 
                request.META.get('HTTP_X_FORWARDED_PROTO') == 'https' or
                request.META.get('HTTP_X_FORWARDED_SSL') == 'on'
            )
            scheme = 'https' if is_secure else 'http'
            host = request.get_host()
        else:
            # Fallback to settings - force HTTPS in production
            use_https = (
                getattr(settings, 'SECURE_SSL_REDIRECT', False) or 
                not getattr(settings, 'DEBUG', True) or
                'hodi.co.ke' in getattr(settings, 'ALLOWED_HOSTS', [])
            )
            scheme = 'https' if use_https else 'http'
            host = getattr(settings, 'APP_DOMAIN', 'hodi.co.ke')
            if not host or host == 'localhost':
                allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
                # Prefer hodi.co.ke if available
                if 'hodi.co.ke' in allowed_hosts:
                    host = 'hodi.co.ke'
                    scheme = 'https'  # Always use HTTPS for hodi.co.ke
                elif allowed_hosts:
                    host = allowed_hosts[0]
                else:
                    host = 'hodi.co.ke'
                    scheme = 'https'  # Default to HTTPS for production domain
        
        # Update the schema's servers to use the correct scheme
        if schema:
            base_url = f"{scheme}://{host}"
            schema['servers'] = [{'url': base_url}]
        
        return schema

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
    generator_class=HTTPSchemaGenerator,  # Use custom generator that enforces HTTPS
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
