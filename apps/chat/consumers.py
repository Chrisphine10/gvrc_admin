# -*- encoding: utf-8 -*-
"""
Emergency Chat System WebSocket Consumers
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Conversation, Message
from .services import MessageService

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time chat functionality
    
    Handles:
    - Joining conversation rooms
    - Sending/receiving messages
    - Message status updates
    - User presence
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope.get('user')
        
        # Verify conversation exists
        if not await self.conversation_exists():
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'conversation_id': self.conversation_id,
            'timestamp': timezone.now().isoformat()
        }))
        
        # Notify others that user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user_id': self.user.id if self.user.is_authenticated else None,
                'timestamp': timezone.now().isoformat()
            }
        )
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Notify others that user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user_id': self.user.id if self.user.is_authenticated else None,
                'timestamp': timezone.now().isoformat()
            }
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'message_status':
                await self.handle_message_status(data)
            elif message_type == 'typing_indicator':
                await self.handle_typing_indicator(data)
            elif message_type == 'read_receipt':
                await self.handle_read_receipt(data)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Server error: {str(e)}'
            }))
    
    async def handle_chat_message(self, data):
        """Handle incoming chat messages"""
        content = data.get('content', '').strip()
        message_type = data.get('message_type', 'text')
        media_url = data.get('media_url', '')
        is_urgent = data.get('is_urgent', False)
        metadata = data.get('metadata', {})
        
        if not content:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Message content cannot be empty'
            }))
            return
        
        # Create message in database
        message = await self.create_message(
            content=content,
            message_type=message_type,
            media_url=media_url,
            is_urgent=is_urgent,
            metadata=metadata
        )
        
        if message:
            # Broadcast message to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'message_id': message.message_id,
                        'content': message.content,
                        'message_type': message.message_type,
                        'media_url': message.media_url,
                        'is_urgent': message.is_urgent,
                        'sender_type': message.sender_type,
                        'sender_info': await self.get_sender_info(message),
                        'sent_at': message.sent_at.isoformat(),
                        'status': message.status
                    }
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to create message'
            }))
    
    async def handle_message_status(self, data):
        """Handle message status updates"""
        message_id = data.get('message_id')
        new_status = data.get('status')
        
        if not message_id or new_status not in ['delivered', 'read']:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid message status update'
            }))
            return
        
        # Update message status
        updated = await self.update_message_status(message_id, new_status)
        
        if updated:
            # Broadcast status update to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_status_update',
                    'message_id': message_id,
                    'status': new_status,
                    'timestamp': timezone.now().isoformat()
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to update message status'
            }))
    
    async def handle_typing_indicator(self, data):
        """Handle typing indicators"""
        is_typing = data.get('is_typing', False)
        
        # Broadcast typing indicator to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': self.user.id if self.user.is_authenticated else None,
                'is_typing': is_typing,
                'timestamp': timezone.now().isoformat()
            }
        )
    
    async def handle_read_receipt(self, data):
        """Handle read receipts"""
        message_ids = data.get('message_ids', [])
        
        if not message_ids:
            return
        
        # Mark messages as read
        count = await self.mark_messages_read(message_ids)
        
        if count > 0:
            # Broadcast read receipt to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_receipt',
                    'user_id': self.user.id if self.user.is_authenticated else None,
                    'message_ids': message_ids,
                    'timestamp': timezone.now().isoformat()
                }
            )
    
    # WebSocket message handlers for broadcasting
    
    async def chat_message(self, event):
        """Send chat message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))
    
    async def message_status_update(self, event):
        """Send message status update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'message_status_update',
            'message_id': event['message_id'],
            'status': event['status'],
            'timestamp': event['timestamp']
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'typing_indicator',
            'user_id': event['user_id'],
            'is_typing': event['is_typing'],
            'timestamp': event['timestamp']
        }))
    
    async def read_receipt(self, event):
        """Send read receipt to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'user_id': event['user_id'],
            'message_ids': event['message_ids'],
            'timestamp': event['timestamp']
        }))
    
    async def user_joined(self, event):
        """Send user joined notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user_id': event['user_id'],
            'timestamp': event['timestamp']
        }))
    
    async def user_left(self, event):
        """Send user left notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'user_id': event['user_id'],
            'timestamp': event['timestamp']
        }))
    
    # Database operations
    
    @database_sync_to_async
    def conversation_exists(self):
        """Check if conversation exists"""
        try:
            return Conversation.objects.filter(conversation_id=self.conversation_id).exists()
        except:
            return False
    
    @database_sync_to_async
    def create_message(self, content, message_type, media_url, is_urgent, metadata):
        """Create a new message"""
        try:
            conversation = Conversation.objects.get(conversation_id=self.conversation_id)
            
            if self.user.is_authenticated and self.user.is_staff:
                # Admin message
                return MessageService.create_admin_message(
                    conversation=conversation,
                    content=content,
                    admin_user=self.user,
                    message_type=message_type,
                    media_url=media_url,
                    is_urgent=is_urgent,
                    metadata=metadata
                )
            else:
                # Mobile message (anonymous)
                return MessageService.create_mobile_message(
                    conversation=conversation,
                    content=content,
                    message_type=message_type,
                    media_url=media_url,
                    is_urgent=is_urgent,
                    metadata=metadata
                )
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
    
    @database_sync_to_async
    def update_message_status(self, message_id, status):
        """Update message status"""
        try:
            message = Message.objects.get(
                message_id=message_id,
                conversation__conversation_id=self.conversation_id
            )
            
            if status == 'delivered':
                MessageService.mark_message_delivered(message)
            elif status == 'read':
                MessageService.mark_message_read(message)
            
            return True
        except Message.DoesNotExist:
            return False
        except Exception as e:
            print(f"Error updating message status: {e}")
            return False
    
    @database_sync_to_async
    def mark_messages_read(self, message_ids):
        """Mark multiple messages as read"""
        try:
            count = Message.objects.filter(
                message_id__in=message_ids,
                conversation__conversation_id=self.conversation_id,
                status__in=['sent', 'delivered']
            ).update(
                status='read',
                read_at=timezone.now()
            )
            return count
        except Exception as e:
            print(f"Error marking messages read: {e}")
            return 0
    
    @database_sync_to_async
    def get_sender_info(self, message):
        """Get sender information for message"""
        if message.sender_type == 'admin' and message.sender:
            return {
                'id': message.sender.id,
                'username': message.sender.username,
                'first_name': message.sender.first_name,
                'last_name': message.sender.last_name
            }
        elif message.sender_type == 'mobile':
            return {
                'type': 'mobile_user',
                'device_id': message.conversation.mobile_session.device_id
            }
        return None


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    
    Handles:
    - Admin notification updates
    - Conversation assignment notifications
    - Urgent message alerts
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope.get('user')
        
        # Only allow authenticated staff users
        if not self.user or not self.user.is_authenticated or not self.user.is_staff:
            await self.close()
            return
        
        self.user_group_name = f'notifications_{self.user.id}'
        
        # Join user's notification group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'notification_connection_established',
            'user_id': self.user.id,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                await self.handle_mark_read(data)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Server error: {str(e)}'
            }))
    
    async def handle_mark_read(self, data):
        """Handle marking notifications as read"""
        notification_id = data.get('notification_id')
        
        if not notification_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Notification ID is required'
            }))
            return
        
        # Mark notification as read
        updated = await self.mark_notification_read(notification_id)
        
        if updated:
            await self.send(text_data=json.dumps({
                'type': 'notification_marked_read',
                'notification_id': notification_id,
                'timestamp': timezone.now().isoformat()
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to mark notification as read'
            }))
    
    # WebSocket message handlers for broadcasting
    
    async def notification_update(self, event):
        """Send notification update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'notification_update',
            'notification': event['notification']
        }))
    
    async def conversation_assigned(self, event):
        """Send conversation assignment notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'conversation_assigned',
            'conversation': event['conversation']
        }))
    
    async def urgent_message(self, event):
        """Send urgent message alert to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'urgent_message',
            'message': event['message']
        }))
    
    # Database operations
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            from .services import NotificationService
            notification = ChatNotification.objects.get(
                notification_id=notification_id,
                user=self.user
            )
            NotificationService.mark_notification_read(notification)
            return True
        except ChatNotification.DoesNotExist:
            return False
        except Exception as e:
            print(f"Error marking notification read: {e}")
            return False
