# -*- encoding: utf-8 -*-
"""
API views
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    """Simple hello world API endpoint"""
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """API status endpoint"""
    return Response({
        "status": "active",
        "version": "v1",
        "message": "API is running successfully"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def my_endpoint(request):
    """Test endpoint - requires authentication"""
    data = {
        "message": "This is a test endpoint",
        "status": "success",
        "user": request.user.username if request.user.is_authenticated else "anonymous",
        "is_staff": request.user.is_staff if request.user.is_authenticated else False,
        "is_superuser": request.user.is_superuser if request.user.is_authenticated else False,
        "example": [1, 2, 3, 4]
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_endpoint(request):
    """Public endpoint - no authentication required"""
    data = {
        "message": "This is a public endpoint",
        "status": "success",
        "access": "public"
    }
    return Response(data)

