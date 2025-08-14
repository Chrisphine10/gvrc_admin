from django.core.management.base import BaseCommand
from django.core import serializers
from facilities.models import (
    User, Facility, FacilityContact, FacilityCoordinate,
    FacilityService, FacilityOwner, County, Constituency, Ward
)
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Backup data to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            help='Output filename'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting data backup...')
        
        models_to_backup = [
            County, Constituency, Ward, User, Facility,
            FacilityContact, FacilityCoordinate, FacilityService, FacilityOwner
        ]
        
        all_objects = []
        for model in models_to_backup:
            objects = model.objects.all()
            all_objects.extend(objects)
        
        serialized_data = serializers.serialize('json', all_objects, indent=2)
        
        with open(options['output'], 'w') as f:
            f.write(serialized_data)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully backed up data to {options["output"]}'
            )
        )
