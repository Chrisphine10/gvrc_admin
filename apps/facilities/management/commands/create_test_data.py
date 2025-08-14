from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from facilities.models import (
    County, Constituency, Ward, Facility, OperationalStatus,
    FacilityContact, ContactType, ServiceCategory, FacilityService
)
from faker import Faker
import random

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Create test data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--facilities',
            type=int,
            default=50,
            help='Number of facilities to create'
        )

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Create sample counties if they don't exist
        counties_data = [
            'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
            'Thika', 'Malindi', 'Kitale', 'Machakos', 'Meru'
        ]
        
        counties = []
        for county_name in counties_data:
            county, created = County.objects.get_or_create(
                county_name=county_name
            )
            counties.append(county)
        
        # Create constituencies and wards
        constituencies = []
        wards = []
        
        for county in counties:
            for i in range(2, 5):  # 2-4 constituencies per county
                constituency, created = Constituency.objects.get_or_create(
                    constituency_name=f"{county.county_name} {fake.word().title()}",
                    county=county
                )
                constituencies.append(constituency)
                
                for j in range(3, 7):  # 3-6 wards per constituency
                    ward, created = Ward.objects.get_or_create(
                        ward_name=f"{constituency.constituency_name} Ward {j}",
                        constituency=constituency
                    )
                    wards.append(ward)
        
        # Get operational statuses
        operational_statuses = list(OperationalStatus.objects.all())
        contact_types = list(ContactType.objects.all())
        service_categories = list(ServiceCategory.objects.all())
        
        # Create users
        users = []
        for i in range(options['users']):
            email = fake.email()
            user = User.objects.create_user(
                email=email,
                full_name=fake.name(),
                password='testpass123'
            )
            users.append(user)
        
        # Create facilities
        for i in range(options['facilities']):
            facility = Facility.objects.create(
                name=f"{fake.company()} {random.choice(['Hospital', 'Clinic', 'Health Center', 'Dispensary'])}",
                registration_number=f"REG{fake.random_int(10000, 99999)}",
                operational_status=random.choice(operational_statuses),
                ward_detail=random.choice(wards),
                is_active=random.choice([True, True, True, False]),  # 75% active
                created_by=random.choice(users)
            )
            
            # Add contacts
            for contact_type in random.sample(contact_types, random.randint(1, 3)):
                if contact_type.type_name == 'Phone':
                    contact_value = fake.phone_number()[:15]
                elif contact_type.type_name == 'Email':
                    contact_value = fake.email()
                else:
                    contact_value = fake.text(max_nb_chars=50)
                
                FacilityContact.objects.create(
                    facility=facility,
                    contact_type=contact_type,
                    contact_value=contact_value
                )
            
            # Add services
            for service_category in random.sample(service_categories, random.randint(2, 6)):
                FacilityService.objects.create(
                    facility=facility,
                    service_category=service_category,
                    service_description=fake.text(max_nb_chars=200)
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {options["users"]} users and {options["facilities"]} facilities'
            )
        )