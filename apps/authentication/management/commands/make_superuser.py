# -*- encoding: utf-8 -*-
"""
Management command to make a user a superuser
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Make a user a superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email of the user to make superuser',
        )

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = User.objects.get(email=email)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully made {email} a superuser and staff member.'
                )
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User with email {email} does not exist.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error making user superuser: {e}')
            )
