# -*- encoding: utf-8 -*-
"""
Emergency Chat System Serializers
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message, ChatNotification
from apps.mobile_sessions.models import MobileSession

User = get_user_model()


class MobileSessionSerializer(serializers.ModelSerializer):
    """Serializer for mobile session identification"""
    
    class Meta:
        model = MobileSession
        ref_name = "ChatMobileSessionSerializer"
        fields = ['device_id', 'notification_enabled', 'preferred_language']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information"""
    
    class Meta:
        model = User
        ref_name = "ChatUserSerializer"
        fields = ['user_id', 'username', 'full_name', 'email']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages"""
    
    sender_info = serializers.SerializerMethodField()
    conversation_id = serializers.IntegerField(source='conversation.conversation_id', read_only=True)
    media_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        ref_name = "ChatMessageSerializer"
        fields = [
            'message_id', 'conversation_id', 'sender', 'sender_type', 'content',
            'message_type', 'media_file', 'media_file_url', 'media_url', 'status', 'sent_at', 'delivered_at',
            'read_at', 'is_urgent', 'metadata', 'sender_info'
        ]
        read_only_fields = [
            'message_id', 'conversation_id', 'status', 'sent_at', 
            'delivered_at', 'read_at', 'sender_info', 'media_file_url'
        ]
    
    def get_media_file_url(self, obj):
        """Get full URL for media file if it exists"""
        if obj.media_file:
            # Debug logging
            print(f"DEBUG: Processing media_file for message {obj.message_id}")
            print(f"DEBUG: media_file value: {obj.media_file}")
            print(f"DEBUG: media_file.url: {obj.media_file.url}")
            print(f"DEBUG: media_file.name: {obj.media_file.name}")
            
            request = self.context.get('request')
            if request:
                # Use build_absolute_uri if request is available
                try:
                    url = request.build_absolute_uri(obj.media_file.url)
                    print(f"DEBUG: Using request.build_absolute_uri: {url}")
                    return url
                except Exception as e:
                    print(f"DEBUG: Error in build_absolute_uri: {e}")
                    # Fall through to manual construction
            else:
                print(f"DEBUG: No request context available for message {obj.message_id}")
            
            # Fallback: construct URL manually
            # This handles cases where serializer is used without request context
            try:
                from django.conf import settings
                # Try to get the current site domain from settings
                base_url = getattr(settings, 'BASE_URL', None)
                
                if not base_url:
                    # If no BASE_URL, try to construct from common settings
                    if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
                        host = settings.ALLOWED_HOSTS[0]
                        if host != '*':
                            # Check if we're in production or development
                            if getattr(settings, 'DEBUG', False):
                                base_url = f"http://{host}:8000"
                            else:
                                base_url = f"https://{host}"
                        else:
                            base_url = "http://127.0.0.1:8000"
                    else:
                        base_url = "http://127.0.0.1:8000"
                
                # Ensure the media file URL is properly constructed
                media_url = obj.media_file.url
                if not media_url.startswith('/'):
                    media_url = '/' + media_url
                
                url = f"{base_url.rstrip('/')}{media_url}"
                print(f"DEBUG: Using fallback URL construction: {url}")
                return url
                
            except Exception as e:
                # Final fallback: just return the relative URL
                print(f"DEBUG: Exception in fallback URL construction: {e}")
                print(f"DEBUG: Returning relative URL: {obj.media_file.url}")
                return obj.media_file.url
        else:
            print(f"DEBUG: No media_file for message {obj.message_id}")
        return None
    
    def get_sender_info(self, obj):
        """Get sender information based on sender type"""
        if obj.sender_type == 'admin' and obj.sender:
            return {
                'user_id': obj.sender.user_id,
                'username': obj.sender.username,
                'full_name': obj.sender.full_name
            }
        elif obj.sender_type == 'mobile':
            return {
                'type': 'mobile_user',
                'device_id': obj.conversation.mobile_session.device_id
            }
        return None
    
    def validate_content(self, value):
        """Validate message content"""
        if not value or not value.strip():
            raise serializers.ValidationError("Message content cannot be empty")
        
        if len(value) > 1000:
            raise serializers.ValidationError("Message content cannot exceed 1000 characters")
        
        return value.strip()
    
    def validate_message_type(self, value):
        """Validate message type"""
        valid_types = ['text', 'image', 'voice', 'file', 'location']
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid message type. Must be one of: {', '.join(valid_types)}")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations"""
    
    mobile_session_info = MobileSessionSerializer(source='mobile_session', read_only=True)
    assigned_admin_info = UserSerializer(source='assigned_admin', read_only=True)
    last_message_info = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'mobile_session', 'mobile_session_info',
            'assigned_admin', 'assigned_admin_info', 'status', 'priority',
            'subject', 'last_message', 'last_message_at', 'last_message_by',
            'unread_count_mobile', 'unread_count_admin', 'unread_count',
            'created_at', 'updated_at', 'last_message_info'
        ]
        read_only_fields = [
            'conversation_id', 'mobile_session_info', 'assigned_admin_info',
            'last_message', 'last_message_at', 'last_message_by',
            'unread_count_mobile', 'unread_count_admin', 'unread_count',
            'created_at', 'updated_at', 'last_message_info'
        ]
    
    def get_last_message_info(self, obj):
        """Get information about the last message"""
        if obj.last_message:
            return {
                'content': obj.last_message,
                'timestamp': obj.last_message_at,
                'sender_type': obj.last_message_by.sender_type if obj.last_message_by else None
            }
        return None
    
    def get_unread_count(self, obj):
        """Get unread count for the current user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user.is_staff:
                return obj.unread_count_admin
            else:
                return obj.unread_count_mobile
        return 0


class ConversationDetailSerializer(ConversationSerializer):
    """Detailed serializer for conversations with messages"""
    
    messages = serializers.SerializerMethodField()
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']
    
    def get_messages(self, obj):
        """Get paginated messages for the conversation"""
        request = self.context.get('request')
        limit = int(request.query_params.get('limit', 50)) if request else 50
        offset = int(request.query_params.get('offset', 0)) if request else 0
        
        messages = obj.messages.all().order_by('-sent_at')[offset:offset + limit]
        return MessageSerializer(messages, many=True, context=self.context).data


class CreateConversationSerializer(serializers.Serializer):
    """Serializer for creating new conversations"""
    
    device_id = serializers.CharField(max_length=128, help_text="Mobile device ID")
    subject = serializers.CharField(max_length=200, required=False, allow_blank=True, help_text="Optional conversation subject")
    
    def validate_device_id(self, value):
        """Validate device ID exists"""
        try:
            MobileSession.objects.get(device_id=value, is_active=True)
        except MobileSession.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive device ID")
        return value


class CreateMessageSerializer(serializers.Serializer):
    """Serializer for creating new messages"""
    
    content = serializers.CharField(max_length=1000, required=False, help_text="Message content (optional for file messages)")
    message_type = serializers.ChoiceField(
        choices=Message.MESSAGE_TYPES,
        default='text',
        help_text="Type of message content"
    )
    media_file = serializers.FileField(required=False, help_text="Media file to upload")
    media_url = serializers.URLField(required=False, allow_blank=True, help_text="URL to media file if applicable")
    is_urgent = serializers.BooleanField(default=False, help_text="Whether message is urgent")
    metadata = serializers.JSONField(required=False, default=dict, help_text="Additional message metadata")
    
    def validate(self, data):
        """Validate message data"""
        message_type = data.get('message_type', 'text')
        content = data.get('content', '')
        media_file = data.get('media_file')
        media_url = data.get('media_url')
        
        # If there's a media file, allow it even for text messages (type will be determined later)
        if media_file:
            return data
        
        # For text messages without files, content is required
        if message_type == 'text' and not content:
            raise serializers.ValidationError("Text messages must have content")
        
        # For media messages, either file or URL is required
        if message_type in ['image', 'voice', 'file'] and not media_file and not media_url:
            raise serializers.ValidationError(f"{message_type.title()} messages must have a file or URL")
        
        # For location messages, content should contain coordinates
        if message_type == 'location' and not content:
            raise serializers.ValidationError("Location messages must contain coordinate data")
        
        return data


class UpdateMessageStatusSerializer(serializers.Serializer):
    """Serializer for updating message status"""
    
    status = serializers.ChoiceField(
        choices=['delivered', 'read'],
        help_text="New message status"
    )


class ConversationAssignmentSerializer(serializers.Serializer):
    """Serializer for assigning conversations to admins"""
    
    admin_user_id = serializers.IntegerField(help_text="ID of admin user to assign")
    
    def validate_admin_user_id(self, value):
        """Validate admin user exists and is staff"""
        try:
            admin_user = User.objects.get(user_id=value)
            if not admin_user.is_staff:
                raise serializers.ValidationError("User must be staff to be assigned to conversations")
            if not admin_user.is_active:
                raise serializers.ValidationError("Admin user must be active")
        except User.DoesNotExist:
            raise serializers.ValidationError("Admin user not found")
        return value


class ConversationStatusSerializer(serializers.Serializer):
    """Serializer for updating conversation status"""
    
    status = serializers.ChoiceField(
        choices=Conversation.STATUS_CHOICES,
        help_text="New conversation status"
    )
    priority = serializers.ChoiceField(
        choices=Conversation.PRIORITY_CHOICES,
        required=False,
        help_text="New conversation priority"
    )


class ChatNotificationSerializer(serializers.ModelSerializer):
    """Serializer for chat notifications"""
    
    conversation_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatNotification
        fields = [
            'notification_id', 'notification_type', 'conversation_info',
            'title', 'body', 'is_read', 'created_at'
        ]
        read_only_fields = ['notification_id', 'notification_type', 'conversation_info', 'created_at']
    
    def get_conversation_info(self, obj):
        """Get basic conversation information"""
        return {
            'conversation_id': obj.conversation.conversation_id,
            'subject': obj.conversation.subject,
            'status': obj.conversation.status
        }


class MobileConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for mobile conversation listing"""
    
    last_message_preview = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(source='unread_count_mobile', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'status', 'subject', 'last_message_preview',
            'unread_count', 'created_at', 'last_message_at'
        ]
    
    def get_last_message_preview(self, obj):
        """Get preview of last message"""
        if obj.last_message:
            return obj.last_message[:100] + "..." if len(obj.last_message) > 100 else obj.last_message
        return "No messages yet"


class AdminConversationListSerializer(serializers.ModelSerializer):
    """Serializer for admin conversation listing"""
    
    mobile_session_info = MobileSessionSerializer(source='mobile_session', read_only=True)
    last_message_preview = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(source='unread_count_admin', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'mobile_session_info', 'status', 'priority',
            'subject', 'last_message_preview', 'unread_count', 'assigned_admin',
            'created_at', 'last_message_at'
        ]
    
    def get_last_message_preview(self, obj):
        """Get preview of last message"""
        if obj.last_message:
            return obj.last_message[:100] + "..." if len(obj.last_message) > 100 else obj.last_message
        return "No messages yet"


class ConversationStatsSerializer(serializers.Serializer):
    """Serializer for conversation statistics"""
    
    total_conversations = serializers.IntegerField(help_text="Total number of conversations")
    new_conversations = serializers.IntegerField(help_text="Number of new conversations")
    active_conversations = serializers.IntegerField(help_text="Number of active conversations")
    resolved_conversations = serializers.IntegerField(help_text="Number of resolved conversations")
    unassigned_conversations = serializers.IntegerField(help_text="Number of unassigned conversations")
    urgent_conversations = serializers.IntegerField(help_text="Number of urgent conversations")
