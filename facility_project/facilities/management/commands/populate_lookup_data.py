from django.core.management.base import BaseCommand
from django.db import transaction
from facilities.models import (
    County, Constituency, Ward, OperationalStatus, 
    ContactType, ServiceCategory, OwnerType
)


class Command(BaseCommand):
    help = 'Populate lookup tables with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Populating lookup data...')
        
        with transaction.atomic():
            # Create Operational Statuses
            operational_statuses = [
                'Operational',
                'Under Construction',
                'Temporarily Closed',
                'Permanently Closed',
                'Under Renovation'
            ]
            
            for status in operational_statuses:
                OperationalStatus.objects.get_or_create(status_name=status)
            
            # Create Contact Types
            contact_types = [
                'Phone',
                'Email',
                'Fax',
                'WhatsApp',
                'Website',
                'Physical Address'
            ]
            
            for contact_type in contact_types:
                ContactType.objects.get_or_create(type_name=contact_type)
            
            # Create Service Categories
            service_categories = [
                'Emergency Services',
                'Maternity Services',
                'Pediatric Care',
                'General Medicine',
                'Surgery',
                'Laboratory Services',
                'Radiology',
                'Pharmacy',
                'Dental Services',
                'Mental Health Services',
                'Rehabilitation Services',
                'Outpatient Services',
                'Inpatient Services',
                'Vaccination Services',
                'Family Planning'
            ]
            
            for category in service_categories:
                ServiceCategory.objects.get_or_create(category_name=category)
            
            # Create Owner Types
            owner_types = [
                'Public',
                'Private',
                'Faith-Based Organization',
                'Non-Governmental Organization',
                'Community Based Organization',
                'Government',
                'County Government',
                'National Government'
            ]
            
            for owner_type in owner_types:
                OwnerType.objects.get_or_create(type_name=owner_type)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated lookup data')
        )

