# -*- encoding: utf-8 -*-
"""
Emergency Chat System Admin Interface
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Conversation, Message, ChatNotification


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin interface for conversations"""
    
    list_display = [
        'conversation_id', 'mobile_device', 'status', 'priority', 'assigned_admin',
        'subject_preview', 'unread_counts', 'created_at', 'last_message_at'
    ]
    list_filter = [
        'status', 'priority', 'assigned_admin', 'created_at', 'last_message_at'
    ]
    search_fields = [
        'conversation_id', 'mobile_session__device_id', 'subject',
        'assigned_admin__username', 'assigned_admin__first_name', 'assigned_admin__last_name'
    ]
    readonly_fields = [
        'conversation_id', 'created_at', 'updated_at', 'last_message_at',
        'unread_count_mobile', 'unread_count_admin'
    ]
    list_per_page = 25
    ordering = ['-last_message_at', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('conversation_id', 'mobile_session', 'subject', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_admin',)
        }),
        ('Message Information', {
            'fields': ('last_message', 'last_message_at', 'last_message_by')
        }),
        ('Unread Counts', {
            'fields': ('unread_count_mobile', 'unread_count_admin')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def mobile_device(self, obj):
        """Display mobile device information"""
        if obj.mobile_session:
            return format_html(
                '<strong>{}</strong><br><small>Location: {:.4f}, {:.4f}</small>',
                obj.mobile_session.device_id,
                obj.mobile_session.latitude or 0,
                obj.mobile_session.longitude or 0
            )
        return '-'
    mobile_device.short_description = 'Mobile Device'
    
    def subject_preview(self, obj):
        """Display subject preview"""
        if obj.subject:
            return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
        return 'No subject'
    subject_preview.short_description = 'Subject'
    
    def unread_counts(self, obj):
        """Display unread counts"""
        return format_html(
            '<span style="color: {};">Mobile: {}</span><br>'
            '<span style="color: {};">Admin: {}</span>',
            'red' if obj.unread_count_mobile > 0 else 'green',
            obj.unread_count_mobile,
            'red' if obj.unread_count_admin > 0 else 'green',
            obj.unread_count_admin
        )
    unread_counts.short_description = 'Unread Messages'
    
    def get_queryset(self, request):
        """Optimize queryset with related fields"""
        return super().get_queryset(request).select_related(
            'mobile_session', 'assigned_admin', 'last_message_by'
        )
    
    actions = ['assign_to_me', 'mark_resolved', 'mark_high_priority']
    
    def assign_to_me(self, request, queryset):
        """Assign selected conversations to current user"""
        updated = queryset.update(assigned_admin=request.user, status='active')
        self.message_user(request, f'{updated} conversation(s) assigned to you.')
    assign_to_me.short_description = "Assign selected conversations to me"
    
    def mark_resolved(self, request, queryset):
        """Mark selected conversations as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} conversation(s) marked as resolved.')
    mark_resolved.short_description = "Mark selected conversations as resolved"
    
    def mark_high_priority(self, request, queryset):
        """Mark selected conversations as high priority"""
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} conversation(s) marked as high priority.')
    mark_high_priority.short_description = "Mark selected conversations as high priority"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for messages"""
    
    list_display = [
        'message_id', 'conversation_link', 'sender_info', 'content_preview',
        'message_type', 'status', 'is_urgent', 'sent_at'
    ]
    list_filter = [
        'message_type', 'status', 'is_urgent', 'sender_type', 'sent_at'
    ]
    search_fields = [
        'content', 'conversation__conversation_id', 'sender__username'
    ]
    readonly_fields = [
        'message_id', 'sent_at', 'delivered_at', 'read_at'
    ]
    list_per_page = 50
    ordering = ['-sent_at']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('message_id', 'conversation', 'content', 'message_type', 'media_url')
        }),
        ('Sender Information', {
            'fields': ('sender_type', 'sender')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'is_urgent', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('sent_at', 'delivered_at', 'read_at'),
            'classes': ('collapse',)
        })
    )
    
    def conversation_link(self, obj):
        """Display conversation as clickable link"""
        if obj.conversation:
            url = reverse('admin:chat_conversation_change', args=[obj.conversation.conversation_id])
            return format_html('<a href="{}">Conversation {}</a>', url, obj.conversation.conversation_id)
        return '-'
    conversation_link.short_description = 'Conversation'
    
    def sender_info(self, obj):
        """Display sender information"""
        if obj.sender_type == 'admin' and obj.sender:
            return format_html(
                '<strong>{}</strong><br><small>Admin</small>',
                obj.sender.username
            )
        elif obj.sender_type == 'mobile':
            return format_html(
                '<span style="color: blue;">Mobile User</span><br>'
                '<small>Device: {}</small>',
                obj.conversation.mobile_session.device_id if obj.conversation else 'Unknown'
            )
        return '-'
    sender_info.short_description = 'Sender'
    
    def content_preview(self, obj):
        """Display content preview"""
        if obj.content:
            return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        return 'No content'
    content_preview.short_description = 'Content'
    
    def get_queryset(self, request):
        """Optimize queryset with related fields"""
        return super().get_queryset(request).select_related(
            'conversation', 'conversation__mobile_session', 'sender'
        )
    
    actions = ['mark_delivered', 'mark_read', 'mark_urgent']
    
    def mark_delivered(self, request, queryset):
        """Mark selected messages as delivered"""
        updated = queryset.filter(status='sent').update(status='delivered')
        self.message_user(request, f'{updated} message(s) marked as delivered.')
    mark_delivered.short_description = "Mark selected messages as delivered"
    
    def mark_read(self, request, queryset):
        """Mark selected messages as read"""
        updated = queryset.filter(status__in=['sent', 'delivered']).update(status='read')
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_read.short_description = "Mark selected messages as read"
    
    def mark_urgent(self, request, queryset):
        """Mark selected messages as urgent"""
        updated = queryset.update(is_urgent=True)
        self.message_user(request, f'{updated} message(s) marked as urgent.')
    mark_urgent.short_description = "Mark selected messages as urgent"


@admin.register(ChatNotification)
class ChatNotificationAdmin(admin.ModelAdmin):
    """Admin interface for chat notifications"""
    
    list_display = [
        'notification_id', 'user', 'notification_type', 'conversation_link',
        'title_preview', 'is_read', 'created_at'
    ]
    list_filter = [
        'notification_type', 'is_read', 'created_at'
    ]
    search_fields = [
        'user__username', 'title', 'body', 'conversation__conversation_id'
    ]
    readonly_fields = [
        'notification_id', 'created_at'
    ]
    list_per_page = 50
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('notification_id', 'user', 'notification_type')
        }),
        ('Content', {
            'fields': ('title', 'body')
        }),
        ('Related Items', {
            'fields': ('conversation', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def conversation_link(self, obj):
        """Display conversation as clickable link"""
        if obj.conversation:
            url = reverse('admin:chat_conversation_change', args=[obj.conversation.conversation_id])
            return format_html('<a href="{}">Conversation {}</a>', url, obj.conversation.conversation_id)
        return '-'
    conversation_link.short_description = 'Conversation'
    
    def title_preview(self, obj):
        """Display title preview"""
        if obj.title:
            return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
        return 'No title'
    title_preview.short_description = 'Title'
    
    def get_queryset(self, request):
        """Optimize queryset with related fields"""
        return super().get_queryset(request).select_related(
            'user', 'conversation', 'message'
        )
    
    actions = ['mark_all_read']
    
    def mark_all_read(self, request, queryset):
        """Mark selected notifications as read"""
        updated = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_all_read.short_description = "Mark selected notifications as read"


# Customize admin site
admin.site.site_header = "GVRC Emergency Chat Admin"
admin.site.site_title = "Emergency Chat Admin"
admin.site.index_title = "Emergency Chat System Administration"
