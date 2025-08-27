# -*- encoding: utf-8 -*-
"""
Management command to create UserProfile for existing users that don't have one
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.authentication.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create UserProfile for existing users that don\'t have one'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        
        if not users_without_profiles.exists():
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles!')
            )
            return
        
        self.stdout.write(f'Found {users_without_profiles.count()} users without profiles')
        
        created_count = 0
        for user in users_without_profiles:
            try:
                profile = UserProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for user: {user.email}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create profile for {user.email}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} profiles')
        )
