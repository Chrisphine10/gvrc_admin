# -*- encoding: utf-8 -*-
"""
API views
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    """Simple hello world API endpoint"""
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
def api_status(request):
    """API status endpoint"""
    return Response({
        "status": "active",
        "version": "v1",
        "message": "API is running successfully"
    })