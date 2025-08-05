# -*- encoding: utf-8 -*-
"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

try:
    from rest_framework.authtoken.views import obtain_auth_token
except:
    pass

# Swagger/OpenAPI schema
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

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.home.urls")),          # Home
    path("api/", include("apps.api.urls")),       # APIs
    path("", include("admin_gradient.urls")),     # Admin theme
    # API Documentation
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
    urlpatterns.append(path("login/jwt/", view=obtain_auth_token))
except:
    pass
