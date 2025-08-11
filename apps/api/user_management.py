# -*- encoding: utf-8 -*-
"""
User management API views
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """Create new user with email confirmation"""
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'user')  # user, staff, admin
        
        if not all([username, email, password]):
            return Response({'error': 'Username, email, and password required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Set role
        if role == 'admin':
            user.is_superuser = True
            user.is_staff = True
        elif role == 'staff':
            user.is_staff = True
        
        user.save()
        
        return Response({
            'message': f'{role.title()} user created successfully',
            'username': username,
            'email': email,
            'role': role,
            'email_sent': True
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)