# -*- encoding: utf-8 -*-
"""
Management command to add a test message to conversation 1
"""
from django.core.management.base import BaseCommand
from apps.chat.models import Conversation, Message
from django.utils import timezone


class Command(BaseCommand):
    help = 'Add a test message to conversation 1'

    def handle(self, *args, **options):
        self.stdout.write('Adding test message to conversation 1...')
        
        try:
            # Get conversation 1
            conversation = Conversation.objects.get(conversation_id=1)
            
            # Create a test message
            message = Message.objects.create(
                conversation=conversation,
                content="This is a test message from the system to verify chat functionality is working.",
                sender_type='mobile',
                message_type='text',
                status='sent',
                sent_at=timezone.now()
            )
            
            # Update conversation metadata
            conversation.last_message = message.content[:200]
            conversation.last_message_at = message.sent_at
            conversation.save(update_fields=['last_message', 'last_message_at'])
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully added test message (ID: {message.message_id}) to conversation {conversation.conversation_id}'
                )
            )
            
        except Conversation.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Conversation 1 does not exist. Please create it first.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error adding test message: {str(e)}')
            )
