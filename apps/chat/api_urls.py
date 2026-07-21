from rest_framework.routers import DefaultRouter

from .views import AdminConversationViewSet, NotificationViewSet

app_name = "chat_api"

router = DefaultRouter()
router.register(r'chat/admin/conversations', AdminConversationViewSet, basename='chat-admin-conversation')
router.register(r'chat/admin/notifications', NotificationViewSet, basename='chat-admin-notification')

urlpatterns = router.urls

