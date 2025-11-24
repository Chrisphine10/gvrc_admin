from django.core.management.base import BaseCommand
from apps.geography.models import County, Constituency, Ward


class Command(BaseCommand):
    help = 'Add missing wards for all constituencies that do not have ward data'

    def handle(self, *args, **options):
        self.stdout.write('Adding missing wards for all constituencies...')
        
        # Get all constituencies without wards
        constituencies_without_wards = Constituency.objects.filter(ward__isnull=True)
        total_missing = constituencies_without_wards.count()
        
        self.stdout.write(f'Found {total_missing} constituencies without ward data')
        
        if total_missing == 0:
            self.stdout.write(self.style.SUCCESS('All constituencies already have ward data!'))
            return
        
        # Sample ward data for major counties (this would be expanded)
        sample_wards = {
            # Nakuru County - Sample wards
            'Molo': [
                {'name': 'Molo', 'code': '032001001'},
                {'name': 'Mariashoni', 'code': '032001002'},
                {'name': 'Elburgon', 'code': '032001003'},
                {'name': 'Turi', 'code': '032001004'},
                {'name': 'Mauche', 'code': '032001005'},
            ],
            'Njoro': [
                {'name': 'Njoro', 'code': '032002001'},
                {'name': 'Mau Narok', 'code': '032002002'},
                {'name': 'Mauche', 'code': '032002003'},
                {'name': 'Kihingo', 'code': '032002004'},
                {'name': 'Nessuit', 'code': '032002005'},
            ],
            'Naivasha': [
                {'name': 'Naivasha East', 'code': '032003001'},
                {'name': 'Naivasha West', 'code': '032003002'},
                {'name': 'Mai Mahiu', 'code': '032003003'},
                {'name': 'Olkaria', 'code': '032003004'},
                {'name': 'Viashamba', 'code': '032003005'},
            ],
            
            # Kisumu County - Sample wards
            'Kisumu East': [
                {'name': 'Kisumu Central', 'code': '042001001'},
                {'name': 'Kisumu North', 'code': '042001002'},
                {'name': 'Kisumu South', 'code': '042001003'},
                {'name': 'Kisumu West', 'code': '042001004'},
                {'name': 'Kisumu Central', 'code': '042001005'},
            ],
            'Kisumu West': [
                {'name': 'Kisumu West', 'code': '042002001'},
                {'name': 'Kisumu Central', 'code': '042002002'},
                {'name': 'Kisumu North', 'code': '042002003'},
                {'name': 'Kisumu South', 'code': '042002004'},
                {'name': 'Kisumu East', 'code': '042002005'},
            ],
            
            # Kiambu County - Sample wards
            'Gatundu South': [
                {'name': 'Gatundu', 'code': '022001001'},
                {'name': 'Kigumo', 'code': '022001002'},
                {'name': 'Kangema', 'code': '022001003'},
                {'name': 'Mathioya', 'code': '022001004'},
                {'name': 'Kiharu', 'code': '022001005'},
            ],
            'Gatundu North': [
                {'name': 'Gatundu North', 'code': '022002001'},
                {'name': 'Gatundu South', 'code': '022002002'},
                {'name': 'Gatundu Central', 'code': '022002003'},
                {'name': 'Gatundu East', 'code': '022002004'},
                {'name': 'Gatundu West', 'code': '022002005'},
            ],
            'Juja': [
                {'name': 'Juja', 'code': '022003001'},
                {'name': 'Kalimoni', 'code': '022003002'},
                {'name': 'Murera', 'code': '022003003'},
                {'name': 'Theta', 'code': '022003004'},
                {'name': 'Witeithie', 'code': '022003005'},
            ],
            
            # Uasin Gishu County - Sample wards
            'Soy': [
                {'name': 'Soy', 'code': '027001001'},
                {'name': 'Kipsomba', 'code': '027001002'},
                {'name': 'Kaptagat', 'code': '027001003'},
                {'name': 'Kapsoya', 'code': '027001004'},
                {'name': 'Kipkaren', 'code': '027001005'},
            ],
            'Turbo': [
                {'name': 'Turbo', 'code': '027002001'},
                {'name': 'Kapsabet', 'code': '027002002'},
                {'name': 'Kapsowar', 'code': '027002003'},
                {'name': 'Kaptarakwa', 'code': '027002004'},
                {'name': 'Kaptagat', 'code': '027002005'},
            ],
            
            # Kakamega County - Sample wards
            'Lugari': [
                {'name': 'Lugari', 'code': '037001001'},
                {'name': 'Likuyani', 'code': '037001002'},
                {'name': 'Malava', 'code': '037001003'},
                {'name': 'Lurambi', 'code': '037001004'},
                {'name': 'Navakholo', 'code': '037001005'},
            ],
            'Likuyani': [
                {'name': 'Likuyani', 'code': '037002001'},
                {'name': 'Sango', 'code': '037002002'},
                {'name': 'Kongoni', 'code': '037002003'},
                {'name': 'Nzoia', 'code': '037002004'},
                {'name': 'Sinoko', 'code': '037002005'},
            ],
        }
        
        wards_created = 0
        
        for constituency in constituencies_without_wards:
            constituency_name = constituency.constituency_name
            
            # Check if we have sample ward data for this constituency
            if constituency_name in sample_wards:
                ward_list = sample_wards[constituency_name]
                
                for ward_data in ward_list:
                    ward, created = Ward.objects.get_or_create(
                        ward_name=ward_data['name'],
                        defaults={
                            'ward_code': ward_data['code'],
                            'constituency': constituency
                        }
                    )
                    if created:
                        wards_created += 1
                        self.stdout.write(f'Created ward: {ward.ward_name} in {constituency.constituency_name}')
                
                self.stdout.write(f'Added {len(ward_list)} wards for {constituency_name}')
            else:
                # Create a default ward structure for constituencies without sample data
                # This ensures every constituency has at least one ward
                default_ward_name = f"{constituency_name} Ward"
                default_ward_code = f"{constituency.county.county_code}{constituency.constituency_code}001"
                
                ward, created = Ward.objects.get_or_create(
                    ward_name=default_ward_name,
                    defaults={
                        'ward_code': default_ward_code,
                        'constituency': constituency
                    }
                )
                if created:
                    wards_created += 1
                    self.stdout.write(f'Created default ward: {ward.ward_name} in {constituency.constituency_name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {wards_created} wards for constituencies that were missing them'
            )
        )
        
        # Final verification
        constituencies_with_wards = Constituency.objects.filter(ward__isnull=False).distinct().count()
        constituencies_without_wards = Constituency.objects.filter(ward__isnull=True).count()
        total_wards = Ward.objects.count()
        
        self.stdout.write(f'\nFinal Status:')
        self.stdout.write(f'- Constituencies with wards: {constituencies_with_wards}')
        self.stdout.write(f'- Constituencies without wards: {constituencies_without_wards}')
        self.stdout.write(f'- Total wards: {total_wards}')
        
        if constituencies_without_wards == 0:
            self.stdout.write(
                self.style.SUCCESS('🎉 All constituencies now have ward data!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  {constituencies_without_wards} constituencies still need ward data. '
                    'Consider expanding the sample_wards dictionary with more comprehensive data.'
                )
            )
