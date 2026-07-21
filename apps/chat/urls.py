# -*- encoding: utf-8 -*-
"""
Emergency Chat System URL Configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminConversationViewSet, NotificationViewSet
)
from .web_views import (
    conversation_list, conversation_detail, chat_analytics,
    assign_conversation, update_conversation_status,
    export_conversations, export_conversation, export_analytics,
    debug_user_permissions, debug_auth, test_chat_access, test_conversations_api, debug_messages
)

# Create routers for admin API sections
admin_router = DefaultRouter()
admin_router.register(r'conversations', AdminConversationViewSet, basename='admin-conversation')
admin_router.register(r'notifications', NotificationViewSet, basename='admin-notification')

app_name = 'chat'

urlpatterns = [
    # Debug endpoint to check authentication
    path('debug/auth/', debug_auth, name='debug_auth'),
    
    # Test endpoint for chat access
    path('test/', test_chat_access, name='test_chat_access'),
    
    # Test endpoint for conversations API
    path('test-conversations/', test_conversations_api, name='test_conversations_api'),
    
    # Debug endpoint for messages
    path('debug/messages/<int:conversation_id>/', debug_messages, name='debug_messages'),
    
    # Web interface endpoints (staff authentication required)
    path('', conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('analytics/', chat_analytics, name='chat_analytics'),
    
    # Debug endpoint to check user permissions
    path('debug/user/', debug_user_permissions, name='debug_user_permissions'),
    
    # Web API endpoints for web interface
    path('conversation/<int:conversation_id>/assign/', assign_conversation, name='assign_conversation'),
    path('conversation/<int:conversation_id>/status/', update_conversation_status, name='update_conversation_status'),
    path('export/', export_conversations, name='export_conversations'),
    path('conversation/<int:conversation_id>/export/', export_conversation, name='export_conversation'),
    path('analytics/export/', export_analytics, name='export_analytics'),
    
    # Admin API endpoints (staff authentication required)
    path('admin/', include(admin_router.urls)),
    
    # Mobile API endpoints (no authentication required)
    # The mobile chat system is now handled by a separate application,
    # so these endpoints are no longer directly accessible here.
    # If you need to access the mobile chat system, you would need to
    # include its URL patterns or adjust the mobile_router definition.
    # For now, we'll keep the path for consistency, but it will not
    # render the mobile chat interface.
    # path('mobile/', include(mobile_router.urls)),
]
