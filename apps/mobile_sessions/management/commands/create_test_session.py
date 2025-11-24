#!/usr/bin/env python3
"""
Django management command to create a test mobile session
"""

from django.core.management.base import BaseCommand
from apps.mobile_sessions.models import MobileSession
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create a test mobile session for development/testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--device-id',
            type=str,
            default='test-device-123',
            help='Device ID for the test session'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if device ID already exists'
        )

    def handle(self, *args, **options):
        device_id = options['device_id']
        force = options['force']

        # Check if session already exists
        try:
            existing_session = MobileSession.objects.get(device_id=device_id)
            if not force:
                self.stdout.write(
                    self.style.WARNING(
                        f'Mobile session with device ID "{device_id}" already exists. '
                        'Use --force to recreate.'
                    )
                )
                return
            else:
                existing_session.delete()
                self.stdout.write(
                    self.style.WARNING(
                        f'Deleted existing session for device ID "{device_id}"'
                    )
                )
        except MobileSession.DoesNotExist:
            pass

        # Create new session
        session = MobileSession.objects.create(
            device_id=device_id,
            notification_enabled=True,
            preferred_language='en',
            is_active=True,
            last_active_at=timezone.now()
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created mobile session for device ID "{device_id}"'
            )
        )
        self.stdout.write(f'Session ID: {session.device_id}')
        self.stdout.write(f'Notification enabled: {session.notification_enabled}')
        self.stdout.write(f'Preferred language: {session.preferred_language}')
        self.stdout.write(f'Active: {session.is_active}')
