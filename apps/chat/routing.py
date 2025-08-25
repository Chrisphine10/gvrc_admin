# -*- encoding: utf-8 -*-
"""
Emergency Chat System WebSocket Routing
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Chat WebSocket - for real-time messaging in conversations
    re_path(
        r'ws/chat/(?P<conversation_id>\d+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
    
    # Notification WebSocket - for admin notifications
    re_path(
        r'ws/notifications/$',
        consumers.NotificationConsumer.as_asgi()
    ),
]
