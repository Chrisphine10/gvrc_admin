# -*- encoding: utf-8 -*-
"""
Custom WebSocket middleware for chat system
"""

from channels.middleware import BaseMiddleware
from channels.auth import get_user
from django.contrib.auth.models import AnonymousUser


class MobileWebSocketAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that allows unauthenticated connections for mobile WebSocket routes.
    For mobile routes, it sets an AnonymousUser and allows the connection.
    For other routes, it uses standard authentication.
    """
    
    async def __call__(self, scope, receive, send):
        # Check if this is a mobile WebSocket route
        path = scope.get('path', '')
        is_mobile_route = path.startswith('/ws/mobile/')
        
        if is_mobile_route:
            # For mobile routes, set AnonymousUser and allow connection
            scope['user'] = AnonymousUser()
        else:
            # For other routes, use standard authentication
            scope['user'] = await get_user(scope)
        
        # Call the next middleware/consumer in the chain
        return await self.inner(scope, receive, send)

