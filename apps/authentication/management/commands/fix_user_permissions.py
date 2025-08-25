# -*- encoding: utf-8 -*-
"""
Management command to fix user permissions
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.authentication.models import User

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix user permissions - ensure superusers have is_staff=True'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email of specific user to fix',
        )
        parser.add_argument(
            '--all-superusers',
            action='store_true',
            help='Fix all superusers',
        )

    def handle(self, *args, **options):
        if options['email']:
            # Fix specific user
            try:
                user = User.objects.get(email=options['email'])
                self.fix_user_permissions(user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with email {options["email"]} not found')
                )
        elif options['all_superusers']:
            # Fix all superusers
            superusers = User.objects.filter(is_superuser=True)
            for user in superusers:
                self.fix_user_permissions(user)
        else:
            # Show current user permissions
            self.show_user_permissions()

    def fix_user_permissions(self, user):
        """Fix permissions for a specific user"""
        changes_made = []
        
        if user.is_superuser and not user.is_staff:
            user.is_staff = True
            changes_made.append('is_staff=True')
        
        if not user.is_active:
            user.is_active = True
            changes_made.append('is_active=True')
        
        if changes_made:
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Fixed user {user.email}: {", ".join(changes_made)}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'User {user.email} already has correct permissions'
                )
            )

    def show_user_permissions(self):
        """Show current user permissions"""
        users = User.objects.all()
        
        self.stdout.write(self.style.SUCCESS('Current User Permissions:'))
        self.stdout.write('-' * 80)
        
        for user in users:
            status = []
            if user.is_superuser:
                status.append('SUPERUSER')
            if user.is_staff:
                status.append('STAFF')
            if user.is_active:
                status.append('ACTIVE')
            else:
                status.append('INACTIVE')
            
            status_str = ' | '.join(status)
            self.stdout.write(
                f'{user.email:<30} {user.full_name:<20} {status_str}'
            )
        
        self.stdout.write('-' * 80)
        self.stdout.write(
            self.style.WARNING(
                'Use --email <email> to fix specific user or --all-superusers to fix all superusers'
            )
        )
