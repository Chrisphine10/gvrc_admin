"""
Public, non-secret configuration the mobile app reads before showing a map.

The provider is chosen by an administrator under Administration > Map
Settings. No device session is needed: nothing here is private, and the app
must be able to draw a map before (or without) creating a session. No API keys
are returned; the app carries its own platform-restricted Google key.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.models import ApplicationSettings

MAP_CONFIG_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "provider": openapi.Schema(type=openapi.TYPE_STRING, enum=["openstreetmap", "google"],
                                   description="Provider the app should render."),
        "selected_provider": openapi.Schema(type=openapi.TYPE_STRING,
                                            description="Provider the admin picked (google falls back to "
                                                        "openstreetmap when the server has no key)."),
        "osm_tile_url": openapi.Schema(type=openapi.TYPE_STRING),
        "osm_attribution": openapi.Schema(type=openapi.TYPE_STRING),
        "default_center": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
            "lng": openapi.Schema(type=openapi.TYPE_NUMBER),
        }),
        "default_zoom": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)


class MobileMapConfigView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        operation_summary="Map provider and defaults for the mobile app",
        tags=["Mobile Config"],
        responses={200: MAP_CONFIG_SCHEMA},
    )
    def get(self, request):
        config = ApplicationSettings.get_settings().map_config()
        response = Response(config)
        # Short cache: an admin's change reaches phones within minutes.
        response["Cache-Control"] = "public, max-age=300"
        return response
