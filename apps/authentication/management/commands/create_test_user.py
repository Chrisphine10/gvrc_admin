# -*- encoding: utf-8 -*-
"""
Management command to create a test user for development
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a test user for development purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@hodi.ke',
            help='Email for the test user'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for the test user'
        )
        parser.add_argument(
            '--full-name',
            type=str,
            default='Admin User',
            help='Full name for the test user'
        )
        parser.add_argument(
            '--phone',
            type=str,
            default='+254700000000',
            help='Phone number for the test user'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Create as superuser'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        full_name = options['full_name']
        phone = options['phone']
        is_superuser = options['superuser']

        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.WARNING(f'User with email {email} already exists')
                    )
                    return

                # Create user
                if is_superuser:
                    user = User.objects.create_superuser(
                        email=email,
                        full_name=full_name,
                        phone_number=phone,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Superuser created successfully: {user.email}'
                        )
                    )
                else:
                    user = User.objects.create_user(
                        email=email,
                        full_name=full_name,
                        phone_number=phone,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'User created successfully: {user.email}'
                        )
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Login credentials:\n'
                        f'Email: {email}\n'
                        f'Password: {password}\n'
                        f'Login URL: /login/'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to create user: {e}')
            )
