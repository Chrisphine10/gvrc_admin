# -*- encoding: utf-8 -*-
"""
Emergency Chat System Models
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.common.utils import get_chat_file_upload_path
import os

from apps.mobile_sessions.models import MobileSession

User = get_user_model()


class Conversation(models.Model):
    """Emergency chat conversation between mobile user and admin"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    conversation_id = models.AutoField(primary_key=True)
    mobile_session = models.ForeignKey(
        MobileSession, 
        on_delete=models.CASCADE, 
        related_name='conversations',
        help_text="Mobile session that initiated the conversation"
    )
    assigned_admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_conversations',
        help_text="Admin assigned to handle this conversation"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        help_text="Current status of the conversation"
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        help_text="Priority level of the conversation"
    )
    subject = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Brief subject or topic of the conversation"
    )
    last_message = models.TextField(
        blank=True, 
        help_text="Content of the last message sent"
    )
    last_message_at = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="Timestamp of the last message"
    )
    last_message_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='last_message_conversations',
        help_text="User who sent the last message"
    )
    unread_count_mobile = models.IntegerField(
        default=0, 
        help_text="Number of unread messages for mobile user"
    )
    unread_count_admin = models.IntegerField(
        default=0, 
        help_text="Number of unread messages for admin"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        db_table = 'emergency_chat_conversations'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_admin']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_message_at']),
        ]
        ordering = ['-last_message_at', '-created_at']
    
    def __str__(self):
        return f"Conversation {self.conversation_id} - {self.mobile_session.device_id} ({self.status})"
    
    def update_last_message(self, content, sender):
        """Update conversation metadata when a new message is sent"""
        self.last_message = content[:200] if len(content) > 200 else content
        self.last_message_at = timezone.now()
        self.last_message_by = sender
        self.updated_at = timezone.now()
        self.save(update_fields=['last_message', 'last_message_at', 'last_message_by', 'updated_at'])
    
    def assign_admin(self, admin_user):
        """Assign an admin to the conversation"""
        self.assigned_admin = admin_user
        self.status = 'active'
        self.save(update_fields=['assigned_admin', 'status', 'updated_at'])
    
    def mark_resolved(self):
        """Mark conversation as resolved"""
        self.status = 'resolved'
        self.save(update_fields=['status', 'updated_at'])


class Message(models.Model):
    """Individual message within a conversation"""
    
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('voice', 'Voice'),
        ('file', 'File'),
        ('location', 'Location'),
    ]
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ]
    
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        help_text="Conversation this message belongs to"
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sent_messages',
        help_text="User who sent the message (null for mobile users)"
    )
    sender_type = models.CharField(
        max_length=20, 
        choices=[('mobile', 'Mobile User'), ('admin', 'Admin')],
        help_text="Type of sender"
    )
    content = models.TextField(help_text="Message content")
    message_type = models.CharField(
        max_length=20, 
        choices=MESSAGE_TYPES, 
        default='text',
        help_text="Type of message content"
    )
    media_file = models.FileField(
        upload_to=get_chat_file_upload_path,
        blank=True, 
        null=True,
        help_text="Media file if message type is not text"
    )
    media_url = models.URLField(
        blank=True, 
        help_text="URL to media file if message type is not text (for external files)"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='sent',
        help_text="Delivery status of the message"
    )
    sent_at = models.DateTimeField(default=timezone.now)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Additional metadata
    is_urgent = models.BooleanField(
        default=False, 
        help_text="Whether this message is marked as urgent"
    )
    metadata = models.JSONField(
        default=dict, 
        help_text="Additional message metadata (coordinates, file info, etc.)"
    )
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        db_table = 'emergency_chat_messages'
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['sender']),
            models.Index(fields=['sender_type']),
            models.Index(fields=['sent_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_urgent']),
        ]
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message {self.message_id} - {self.conversation.conversation_id} ({self.sender_type})"
    
    def get_original_filename(self):
        """Get the original filename from metadata if available"""
        if self.metadata and 'original_name' in self.metadata:
            return self.metadata['original_name']
        elif self.media_file:
            # Extract original name from the unique filename
            filename = os.path.basename(self.media_file.name)
            # Remove the prefix and timestamp/UUID parts
            if filename.startswith('chat_'):
                filename = filename[5:]  # Remove 'chat_' prefix
            # Find the last underscore before the extension
            parts = filename.rsplit('_', 2)
            if len(parts) >= 3:
                return parts[0] + os.path.splitext(filename)[1]
        return None
    
    def get_file_size_mb(self):
        """Get file size in MB if available"""
        if self.metadata and 'file_size' in self.metadata:
            return round(self.metadata['file_size'] / (1024 * 1024), 2)
        return None
    
    def get_file_type(self):
        """Get file type if available"""
        if self.metadata and 'file_type' in self.metadata:
            return self.metadata['file_type']
        return None
    
    def mark_delivered(self):
        """Mark message as delivered"""
        if self.status == 'sent':
            self.status = 'delivered'
            self.delivered_at = timezone.now()
            self.save(update_fields=['status', 'delivered_at'])
    
    def mark_read(self):
        """Mark message as read"""
        if self.status in ['sent', 'delivered']:
            self.status = 'read'
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])
    
    def save(self, *args, **kwargs):
        """Override save to update conversation metadata"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update conversation metadata
            self.conversation.update_last_message(self.content, self.sender)
            
            # Update unread counts
            if self.sender_type == 'mobile':
                self.conversation.unread_count_admin += 1
            else:
                self.conversation.unread_count_mobile += 1
            self.conversation.save(update_fields=['unread_count_mobile', 'unread_count_admin'])


class ChatNotification(models.Model):
    """Notifications for chat events"""
    
    NOTIFICATION_TYPES = [
        ('new_message', 'New Message'),
        ('conversation_assigned', 'Conversation Assigned'),
        ('urgent_message', 'Urgent Message'),
        ('conversation_resolved', 'Conversation Resolved'),
    ]
    
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='chat_notifications',
        help_text="User to receive the notification"
    )
    notification_type = models.CharField(
        max_length=30, 
        choices=NOTIFICATION_TYPES,
        help_text="Type of notification"
    )
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        help_text="Related conversation"
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True, 
        blank=True,
        help_text="Related message if applicable"
    )
    title = models.CharField(max_length=200, help_text="Notification title")
    body = models.TextField(help_text="Notification body")
    is_read = models.BooleanField(default=False, help_text="Whether notification has been read")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Chat Notification"
        verbose_name_plural = "Chat Notifications"
        db_table = 'emergency_chat_notifications'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} - {self.user.username}"
    
    def mark_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
