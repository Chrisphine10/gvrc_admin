# -*- encoding: utf-8 -*-
"""
Management command to create a test user for authentication testing
"""

from django.core.management.base import BaseCommand
from apps.authentication.models import User
import hashlib


class Command(BaseCommand):
    help = 'Create a test user for authentication testing'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='admin@gvrc.com', help='User email')
        parser.add_argument('--name', type=str, default='GVRC Admin', help='User full name')
        parser.add_argument('--phone', type=str, default='+254700000000', help='User phone number')
        parser.add_argument('--password', type=str, default='admin123', help='User password')

    def handle(self, *args, **options):
        email = options['email']
        full_name = options['name']
        phone_number = options['phone']
        password = options['password']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists')
            )
            return

        # Create user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = User.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash,
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created test user:\n'
                f'  Email: {email}\n'
                f'  Name: {full_name}\n'
                f'  Phone: {phone_number}\n'
                f'  Password: {password}\n'
                f'  User ID: {user.user_id}'
            )
        )
