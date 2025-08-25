# -*- encoding: utf-8 -*-
"""
Management command to create admin@hodi.ke user if it doesn't exist
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin@hodi.ke user if it doesn\'t exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for the admin user (default: admin123)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of the user even if it exists',
        )

    def handle(self, *args, **options):
        password = options['password']
        force = options['force']
        
        try:
            # Check if user already exists
            existing_user = User.objects.filter(email='admin@hodi.ke').first()
            
            if existing_user and not force:
                self.stdout.write(
                    self.style.WARNING(
                        f'User admin@hodi.ke already exists with ID: {existing_user.user_id}'
                    )
                )
                self.stdout.write('Use --force to recreate the user')
                return
            
            if existing_user and force:
                # Delete existing user
                existing_user.delete()
                self.stdout.write('Deleted existing admin@hodi.ke user')
            
            # Create new admin user
            admin_user = User.objects.create_user(
                email='admin@hodi.ke',
                full_name='Hodi Admin',
                phone_number='+254700000000',
                password=password,
                is_staff=True,
                is_superuser=True,
                is_active=True,
                verified=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin@hodi.ke user with ID: {admin_user.user_id}'
                )
            )
            
            # Now run the fix command to ensure proper permissions
            self.stdout.write('Running fix command to ensure proper permissions...')
            call_command('fix_admin_user')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )
