# -*- encoding: utf-8 -*-
"""
Emergency Chat System Services
"""

from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from typing import Optional, List, Dict, Any, TYPE_CHECKING, Union
from .models import Conversation, Message, ChatNotification
from apps.mobile_sessions.models import MobileSession
from django.db import models

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser
    UserType = AbstractUser
else:
    UserType = None

User = get_user_model()


class ConversationService:
    """Service for managing conversations"""
    
    @staticmethod
    def get_or_create_conversation(mobile_session: MobileSession, subject: str = "") -> Conversation:
        """
        Get existing conversation or create new one for mobile session
        
        Args:
            mobile_session: Mobile session instance
            subject: Optional subject for the conversation
            
        Returns:
            Conversation instance
        """
        # Check if there's an active conversation for this session
        existing_conversation = Conversation.objects.filter(
            mobile_session=mobile_session,
            status__in=['new', 'active']
        ).first()
        
        if existing_conversation:
            return existing_conversation
        
        # Create new conversation
        conversation = Conversation.objects.create(
            mobile_session=mobile_session,
            subject=subject,
            status='new'
        )
        
        return conversation
    
    @staticmethod
    def assign_admin_to_conversation(conversation: Conversation, admin_user: "UserType") -> Conversation:
        """
        Assign an admin to a conversation
        
        Args:
            conversation: Conversation to assign
            admin_user: Admin user to assign
            
        Returns:
            Updated conversation
        """
        if not admin_user.is_staff:
            raise ValueError("User must be staff to be assigned to conversations")
        
        conversation.assign_admin(admin_user)
        
        # Create notification for admin
        ChatNotification.objects.create(
            user=admin_user,
            notification_type='conversation_assigned',
            conversation=conversation,
            title=f"New conversation assigned",
            body=f"You have been assigned to conversation {conversation.conversation_id}"
        )
        
        return conversation
    
    @staticmethod
    def auto_assign_conversation(conversation: Conversation) -> Optional["UserType"]:
        """
        Auto-assign conversation to first available admin
        
        Args:
            conversation: Conversation to assign
            
        Returns:
            Assigned admin user or None if no admin available
        """
        # Find first available admin (not currently handling too many conversations)
        available_admin = User.objects.filter(
            is_staff=True,
            is_active=True
        ).annotate(
            active_conversation_count=models.Count(
                'assigned_conversations',
                filter=models.Q(assigned_conversations__status='active')
            )
        ).filter(
            active_conversation_count__lt=5  # Limit to 5 active conversations per admin
        ).order_by('active_conversation_count').first()
        
        if available_admin:
            ConversationService.assign_admin_to_conversation(conversation, available_admin)
            return available_admin
        
        return None
    

    def get_conversations_for_admin(admin_user: "UserType", status: str = None) -> List[Conversation]:
        """
        Get conversations for a specific admin
        
        Args:
            admin_user: Admin user
            status: Optional status filter
            
        Returns:
            List of conversations
        """
        queryset = Conversation.objects.filter(assigned_admin=admin_user)
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-last_message_at', '-created_at')
    
    @staticmethod
    def get_unassigned_conversations() -> List[Conversation]:
        """
        Get all unassigned conversations
        
        Returns:
            List of unassigned conversations
        """
        return Conversation.objects.filter(
            assigned_admin__isnull=True,
            status='new'
        ).order_by('-created_at')
    
    @staticmethod
    def mark_conversation_resolved(conversation: Conversation) -> Conversation:
        """
        Mark conversation as resolved
        
        Args:
            conversation: Conversation to resolve
            
        Returns:
            Updated conversation
        """
        conversation.mark_resolved()
        
        # Create notification for mobile user (if they have notifications enabled)
        if conversation.mobile_session.notification_enabled:
            # In a real implementation, this would trigger a push notification
            pass
        
        return conversation


class MessageService:
    """Service for managing messages"""
    
    @staticmethod
    def create_message(
        conversation: Conversation,
        content: str,
        sender_type: str,
        sender: Optional["UserType"] = None,
        message_type: str = 'text',
        media_file = None,
        media_url: str = "",
        is_urgent: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Create a new message in a conversation
        
        Args:
            conversation: Conversation to add message to
            content: Message content
            sender_type: Type of sender ('mobile' or 'admin')
            sender: User who sent the message (null for mobile users)
            message_type: Type of message content
            media_file: Uploaded media file if applicable
            media_url: URL to media file if applicable
            is_urgent: Whether message is urgent
            metadata: Additional message metadata
            
        Returns:
            Created message
        """
        if metadata is None:
            metadata = {}
        
        # Handle file upload
        if media_file:
            # Update metadata with file information
            metadata.update({
                'file_name': media_file.name,
                'file_size': media_file.size,
                'file_type': media_file.content_type,
                'original_name': getattr(media_file, 'original_name', media_file.name)
            })
        
        message = Message.objects.create(
            conversation=conversation,
            content=content,
            sender_type=sender_type,
            sender=sender,
            message_type=message_type,
            media_file=media_file,
            media_url=media_url,
            is_urgent=is_urgent,
            metadata=metadata
        )
        
        # Auto-assign admin if this is the first message and no admin assigned
        if (sender_type == 'mobile' and 
            conversation.status == 'new' and 
            not conversation.assigned_admin):
            ConversationService.auto_assign_conversation(conversation)
        
        return message
    
    @staticmethod
    def create_mobile_message(
        conversation: Conversation,
        content: str,
        message_type: str = 'text',
        media_file = None,
        media_url: str = "",
        is_urgent: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Create a message from mobile user
        
        Args:
            conversation: Conversation to add message to
            content: Message content
            message_type: Type of message content
            media_file: Uploaded media file if applicable
            media_url: URL to media file if applicable
            is_urgent: Whether message is urgent
            metadata: Additional message metadata
            
        Returns:
            Created message
        """
        return MessageService.create_message(
            conversation=conversation,
            content=content,
            sender_type='mobile',
            message_type=message_type,
            media_file=media_file,
            media_url=media_url,
            is_urgent=is_urgent,
            metadata=metadata
        )
    
    @staticmethod
    def create_admin_message(
        conversation: Conversation,
        content: str,
        admin_user: "UserType",
        message_type: str = 'text',
        media_file = None,
        media_url: str = "",
        is_urgent: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Create a message from admin
        
        Args:
            conversation: Conversation to add message to
            content: Message content
            admin_user: Admin user sending the message
            message_type: Type of message content
            media_file: Uploaded media file if applicable
            media_url: URL to media file if applicable
            is_urgent: Whether message is urgent
            metadata: Additional message metadata
            
        Returns:
            Created message
        """
        if not admin_user.is_staff:
            raise ValueError("User must be staff to send admin messages")
        
        return MessageService.create_message(
            conversation=conversation,
            content=content,
            sender_type='admin',
            sender=admin_user,
            message_type=message_type,
            media_file=media_file,
            media_url=media_url,
            is_urgent=is_urgent,
            metadata=metadata
        )
    
    @staticmethod
    def mark_message_delivered(message: Message) -> Message:
        """
        Mark message as delivered
        
        Args:
            message: Message to mark as delivered
            
        Returns:
            Updated message
        """
        message.mark_delivered()
        return message
    
    @staticmethod
    def mark_message_read(message: Message) -> Message:
        """
        Mark message as read
        
        Args:
            message: Message to mark as read
            
        Returns:
            Updated message
        """
        message.mark_read()
        
        # Update conversation unread count
        if message.sender_type == 'mobile':
            message.conversation.unread_count_admin = max(0, message.conversation.unread_count_admin - 1)
        else:
            message.conversation.unread_count_mobile = max(0, message.conversation.unread_count_mobile - 1)
        
        message.conversation.save(update_fields=['unread_count_mobile', 'unread_count_admin'])
        
        return message
    
    @staticmethod
    def get_conversation_messages(
        conversation: Conversation,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        Get messages for a conversation with pagination
        
        Args:
            conversation: Conversation to get messages for
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            
        Returns:
            List of messages
        """
        return Message.objects.filter(
            conversation=conversation
        ).order_by('-sent_at')[offset:offset + limit]
    
    @staticmethod
    def mark_conversation_messages_read(
        conversation: Conversation,
        user_type: str
    ) -> int:
        """
        Mark all messages in a conversation as read for a specific user type
        
        Args:
            conversation: Conversation to mark messages read for
            user_type: Type of user ('mobile' or 'admin')
            
        Returns:
            Number of messages marked as read
        """
        messages = Message.objects.filter(
            conversation=conversation,
            sender_type__ne=user_type,
            status__in=['sent', 'delivered']
        )
        
        count = messages.count()
        messages.update(
            status='read',
            read_at=timezone.now()
        )
        
        # Update conversation unread count
        if user_type == 'mobile':
            conversation.unread_count_mobile = 0
        else:
            conversation.unread_count_admin = 0
        
        conversation.save(update_fields=['unread_count_mobile', 'unread_count_admin'])
        
        return count


class NotificationService:
    """Service for managing chat notifications"""
    
    @staticmethod
    def create_notification(
        user: "UserType",
        notification_type: str,
        conversation: Conversation,
        title: str,
        body: str,
        message: Optional[Message] = None
    ) -> ChatNotification:
        """
        Create a new notification
        
        Args:
            user: User to notify
            notification_type: Type of notification
            conversation: Related conversation
            title: Notification title
            body: Notification body
            message: Related message if applicable
            
        Returns:
            Created notification
        """
        return ChatNotification.objects.create(
            user=user,
            notification_type=notification_type,
            conversation=conversation,
            message=message,
            title=title,
            body=body
        )
    
    @staticmethod
    def get_unread_notifications(user: "UserType") -> List[ChatNotification]:
        """
        Get unread notifications for a user
        
        Args:
            user: User to get notifications for
            
        Returns:
            List of unread notifications
        """
        return ChatNotification.objects.filter(
            user=user,
            is_read=False
        ).order_by('-created_at')
    
    @staticmethod
    def mark_notification_read(notification: ChatNotification) -> ChatNotification:
        """
        Mark notification as read
        
        Args:
            notification: Notification to mark as read
            
        Returns:
            Updated notification
        """
        notification.mark_read()
        return notification
    
    @staticmethod
    def mark_all_notifications_read(user: "UserType") -> int:
        """
        Mark all notifications as read for a user
        
        Args:
            user: User to mark notifications read for
            
        Returns:
            Number of notifications marked as read
        """
        notifications = ChatNotification.objects.filter(
            user=user,
            is_read=False
        )
        
        count = notifications.count()
        notifications.update(is_read=True)
        
        return count
