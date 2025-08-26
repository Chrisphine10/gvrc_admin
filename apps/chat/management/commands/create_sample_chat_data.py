# -*- encoding: utf-8 -*-
"""
Management command to create sample chat data for testing analytics
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.chat.models import Conversation, Message
from apps.mobile_sessions.models import MobileSession
from datetime import timedelta
import random
from django.db.models import Count

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample chat data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--conversations',
            type=int,
            default=5,
            help='Number of conversations to create (default: 5)'
        )
        parser.add_argument(
            '--messages',
            type=int,
            default=10,
            help='Number of messages per conversation (default: 10)'
        )

    def handle(self, *args, **options):
        num_conversations = options['conversations']
        messages_per_conversation = options['messages']
        
        self.stdout.write(f'Creating {num_conversations} conversations with {messages_per_conversation} messages each...')
        
        # Get or create staff users
        staff_users = User.objects.filter(is_staff=True)
        if not staff_users.exists():
            self.stdout.write('No staff users found. Creating a sample admin user...')
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            staff_users = [admin_user]
        
        # Get or create mobile sessions
        mobile_sessions = MobileSession.objects.all()
        if not mobile_sessions.exists():
            self.stdout.write('No mobile sessions found. Creating sample mobile sessions...')
            for i in range(3):
                MobileSession.objects.create(
                    device_id=f'device_{i+1}',
                    latitude=random.uniform(-90, 90),
                    longitude=random.uniform(-180, 180),
                    is_active=True
                )
            mobile_sessions = MobileSession.objects.all()
        
        # Sample subjects and priorities
        subjects = [
            "Emergency assistance needed",
            "Medical emergency",
            "Fire incident",
            "Security concern",
            "Traffic accident",
            "Natural disaster",
            "Infrastructure issue",
            "Public safety concern"
        ]
        
        priorities = ['low', 'medium', 'high', 'urgent']
        statuses = ['new', 'active', 'resolved', 'closed']
        
        # Create conversations
        conversations_created = 0
        
        for i in range(num_conversations):
            # Random mobile session
            mobile_session = random.choice(mobile_sessions)
            
            # Random subject and priority
            subject = random.choice(subjects)
            priority = random.choice(priorities)
            status = random.choice(statuses)
            
            # Random assignment (some assigned, some not)
            assigned_admin = random.choice(staff_users) if random.choice([True, False]) else None
            
            # Create conversation
            conversation = Conversation.objects.create(
                mobile_session=mobile_session,
                assigned_admin=assigned_admin,
                status=status,
                priority=priority,
                subject=subject,
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            
            # Create messages for this conversation
            messages_created = 0
            
            # First message is always from mobile
            first_message_time = conversation.created_at + timedelta(minutes=random.randint(1, 10))
            Message.objects.create(
                conversation=conversation,
                sender_type='mobile',
                content=f"Emergency: {subject}",
                message_type='text',
                sent_at=first_message_time,
                status='read'
            )
            messages_created += 1
            
            # If conversation is assigned, add admin response
            if assigned_admin and status in ['active', 'resolved']:
                response_time = first_message_time + timedelta(minutes=random.randint(5, 60))
                Message.objects.create(
                    conversation=conversation,
                    sender=assigned_admin,
                    sender_type='admin',
                    content=f"Response: We're handling your emergency. Can you provide more details?",
                    message_type='text',
                    sent_at=response_time,
                    status='read'
                )
                messages_created += 1
                
                # Update conversation metadata
                conversation.last_message = "Response: We're handling your emergency. Can you provide more details?"
                conversation.last_message_at = response_time
                conversation.last_message_by = assigned_admin
                conversation.save()
            
            # Add more messages
            for j in range(messages_per_conversation - messages_created):
                # Alternate between mobile and admin
                is_mobile = (j % 2 == 0)
                
                if is_mobile:
                    content = f"Mobile message {j+1}: Additional information about the emergency"
                    sender_type = 'mobile'
                    sender = None
                else:
                    if assigned_admin:
                        content = f"Admin response {j+1}: We're working on it"
                        sender_type = 'admin'
                        sender = assigned_admin
                    else:
                        continue  # Skip admin messages if no admin assigned
                
                message_time = conversation.created_at + timedelta(
                    minutes=random.randint(15, 120)
                )
                
                Message.objects.create(
                    conversation=conversation,
                    sender=sender,
                    sender_type=sender_type,
                    content=content,
                    message_type='text',
                    sent_at=message_time,
                    status='read'
                )
                messages_created += 1
            
            # Update conversation with final message info
            last_message = conversation.messages.order_by('-sent_at').first()
            if last_message:
                conversation.last_message = last_message.content[:200]
                conversation.last_message_at = last_message.sent_at
                conversation.last_message_by = last_message.sender
                conversation.save()
            
            conversations_created += 1
            self.stdout.write(f'Created conversation {conversation.conversation_id} with {messages_created} messages')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {conversations_created} conversations with sample messages!'
            )
        )
        
        # Display summary
        total_conversations = Conversation.objects.count()
        total_messages = Message.objects.count()
        mobile_messages = Message.objects.filter(sender_type='mobile').count()
        admin_messages = Message.objects.filter(sender_type='admin').count()
        
        self.stdout.write('\nChat System Summary:')
        self.stdout.write(f'Total conversations: {total_conversations}')
        self.stdout.write(f'Total messages: {total_messages}')
        self.stdout.write(f'Mobile messages: {mobile_messages}')
        self.stdout.write(f'Admin messages: {admin_messages}')
        
        if total_conversations > 0:
            avg_messages = round(total_messages / total_conversations, 1)
            self.stdout.write(f'Average messages per conversation: {avg_messages}')
        
        # Status distribution
        status_distribution = Conversation.objects.values('status').annotate(
            count=Count('conversation_id')
        )
        self.stdout.write('\nConversation Status Distribution:')
        for status_info in status_distribution:
            self.stdout.write(f'  {status_info["status"]}: {status_info["count"]}')
        
        # Priority distribution
        priority_distribution = Conversation.objects.values('priority').annotate(
            count=Count('conversation_id')
        )
        self.stdout.write('\nConversation Priority Distribution:')
        for priority_info in priority_distribution:
            self.stdout.write(f'  {priority_info["priority"]}: {priority_info["count"]}')
