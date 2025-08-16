# -*- encoding: utf-8 -*-
"""
Management command to load initial data for lookup tables
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = 'Load initial data for lookup tables'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        try:
            with transaction.atomic():
                # Load the fixture data
                call_command('loaddata', 'initial_data', app_label='common')
                self.stdout.write(
                    self.style.SUCCESS('Successfully loaded initial data')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to load initial data: {e}')
            )
            raise
