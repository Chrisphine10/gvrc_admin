# -*- encoding: utf-8 -*-
"""
Emergency Chat System WebSocket Routing
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Chat WebSocket - for real-time messaging in conversations (admin/staff users)
    re_path(
        r'ws/chat/(?P<conversation_id>\d+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
    
    # Mobile Chat WebSocket - for real-time messaging using device_id authentication
    # URL format: ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx
    re_path(
        r'ws/mobile/chat/(?P<conversation_id>\d+)/$',
        consumers.MobileChatConsumer.as_asgi()
    ),
    
    # Notification WebSocket - for admin notifications
    re_path(
        r'ws/notifications/$',
        consumers.NotificationConsumer.as_asgi()
    ),
]
