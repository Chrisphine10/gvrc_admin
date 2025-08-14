from django.core.management.base import BaseCommand
from facilities.models import Facility, County, Constituency, Ward, OperationalStatus
import csv
from decimal import Decimal, InvalidOperation


class Command(BaseCommand):
    help = 'Import facilities from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to CSV file'
        )

    def handle(self, *args, **options):
        self.stdout.write(f'Importing facilities from {options["csv_file"]}...')
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        try:
            with open(options['csv_file'], 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # Get or create location hierarchy
                        county, _ = County.objects.get_or_create(
                            county_name=row.get('county', '').strip()
                        )
                        
                        constituency, _ = Constituency.objects.get_or_create(
                            constituency_name=row.get('constituency', '').strip(),
                            county=county
                        )
                        
                        ward, _ = Ward.objects.get_or_create(
                            ward_name=row.get('ward', '').strip(),
                            constituency=constituency
                        )
                        
                        # Get operational status
                        status_name = row.get('operational_status', 'Operational').strip()
                        operational_status, _ = OperationalStatus.objects.get_or_create(
                            status_name=status_name
                        )
                        
                        # Create or update facility
                        facility_name = row.get('facility_name', '').strip()
                        registration_number = row.get('registration_number', '').strip()
                        
                        facility, created = Facility.objects.get_or_create(
                            name=facility_name,
                            defaults={
                                'registration_number': registration_number,
                                'operational_status': operational_status,
                                'ward_detail': ward,
                                'is_active': True
                            }
                        )
                        
                        if created:
                            created_count += 1
                        else:
                            # Update existing facility
                            facility.registration_number = registration_number
                            facility.operational_status = operational_status
                            facility.ward_detail = ward
                            facility.save()
                            updated_count += 1
                        
                        # Add coordinates if provided
                        latitude = row.get('latitude', '').strip()
                        longitude = row.get('longitude', '').strip()
                        
                        if latitude and longitude:
                            try:
                                lat_decimal = Decimal(latitude)
                                lng_decimal = Decimal(longitude)
                                
                                from facilities.models import FacilityCoordinate
                                coordinate, coord_created = FacilityCoordinate.objects.get_or_create(
                                    facility=facility,
                                    defaults={
                                        'latitude': lat_decimal,
                                        'longitude': lng_decimal,
                                        'data_source': 'CSV Import'
                                    }
                                )
                                
                                if not coord_created:
                                    coordinate.latitude = lat_decimal
                                    coordinate.longitude = lng_decimal
                                    coordinate.save()
                                
                            except (InvalidOperation, ValueError):
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'Invalid coordinates for {facility_name}: {latitude}, {longitude}'
                                    )
                                )
                        
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error processing row: {str(e)}'
                            )
                        )
                        continue
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {options["csv_file"]}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Import completed: {created_count} created, {updated_count} updated, {error_count} errors'
            )
        )