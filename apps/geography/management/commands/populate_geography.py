from django.core.management.base import BaseCommand
from apps.geography.models import County, Constituency, Ward


class Command(BaseCommand):
    help = 'Populate geography tables with sample data for Kenya'

    def handle(self, *args, **options):
        self.stdout.write('Populating geography tables...')
        
        # Create sample counties
        counties_data = [
            {'name': 'Nairobi', 'code': 'NBI'},
            {'name': 'Mombasa', 'code': 'MBS'},
            {'name': 'Kisumu', 'code': 'KSM'},
            {'name': 'Nakuru', 'code': 'NKR'},
            {'name': 'Eldoret', 'code': 'ELD'},
        ]
        
        counties = {}
        for county_data in counties_data:
            county, created = County.objects.get_or_create(
                county_name=county_data['name'],
                defaults={'county_code': county_data['code']}
            )
            counties[county.county_name] = county
            if created:
                self.stdout.write(f'Created county: {county.county_name}')
        
        # Create sample constituencies
        constituencies_data = [
            {'name': 'Westlands', 'code': 'WST', 'county': 'Nairobi'},
            {'name': 'Dagoretti North', 'code': 'DGN', 'county': 'Nairobi'},
            {'name': 'Dagoretti South', 'code': 'DGS', 'county': 'Nairobi'},
            {'name': 'Langata', 'code': 'LNG', 'county': 'Nairobi'},
            {'name': 'Kibra', 'code': 'KBR', 'county': 'Nairobi'},
            {'name': 'Roysambu', 'code': 'RYS', 'county': 'Nairobi'},
            {'name': 'Kasarani', 'code': 'KSR', 'county': 'Nairobi'},
            {'name': 'Ruaraka', 'code': 'RRK', 'county': 'Nairobi'},
            {'name': 'Embakasi South', 'code': 'EBS', 'county': 'Nairobi'},
            {'name': 'Embakasi North', 'code': 'EBN', 'county': 'Nairobi'},
            {'name': 'Embakasi Central', 'code': 'EBC', 'county': 'Nairobi'},
            {'name': 'Embakasi East', 'code': 'EBE', 'county': 'Nairobi'},
            {'name': 'Embakasi West', 'code': 'EBW', 'county': 'Nairobi'},
            {'name': 'Makadara', 'code': 'MKD', 'county': 'Nairobi'},
            {'name': 'Kamukunji', 'code': 'KMK', 'county': 'Nairobi'},
            {'name': 'Starehe', 'code': 'STR', 'county': 'Nairobi'},
            {'name': 'Mathare', 'code': 'MTH', 'county': 'Nairobi'},
            {'name': 'Nyali', 'code': 'NYL', 'county': 'Mombasa'},
            {'name': 'Mvita', 'code': 'MVT', 'county': 'Mombasa'},
            {'name': 'Changamwe', 'code': 'CHG', 'county': 'Mombasa'},
            {'name': 'Jomvu', 'code': 'JMV', 'county': 'Mombasa'},
            {'name': 'Kisauni', 'code': 'KSN', 'county': 'Mombasa'},
            {'name': 'Likoni', 'code': 'LKN', 'county': 'Mombasa'},
        ]
        
        constituencies = {}
        for constituency_data in constituencies_data:
            constituency, created = Constituency.objects.get_or_create(
                constituency_name=constituency_data['name'],
                defaults={
                    'constituency_code': constituency_data['code'],
                    'county': counties[constituency_data['county']]
                }
            )
            constituencies[constituency.constituency_name] = constituency
            if created:
                self.stdout.write(f'Created constituency: {constituency.constituency_name} in {constituency.county.county_name}')
        
        # Create sample wards
        wards_data = [
            {'name': 'Parklands/Highridge', 'code': 'PKH', 'constituency': 'Westlands'},
            {'name': 'Karura', 'code': 'KRU', 'constituency': 'Westlands'},
            {'name': 'Kangemi', 'code': 'KNG', 'constituency': 'Westlands'},
            {'name': 'Mountain View', 'code': 'MTV', 'constituency': 'Westlands'},
            {'name': 'Kilimani', 'code': 'KLM', 'constituency': 'Dagoretti North'},
            {'name': 'Mutu-ini', 'code': 'MTI', 'constituency': 'Dagoretti North'},
            {'name': 'Ngando', 'code': 'NGD', 'constituency': 'Dagoretti North'},
            {'name': 'Riruta', 'code': 'RRT', 'constituency': 'Dagoretti North'},
            {'name': 'Uthiru/Ruthimitu', 'code': 'UTR', 'constituency': 'Dagoretti North'},
            {'name': 'Waithaka', 'code': 'WTH', 'constituency': 'Dagoretti North'},
            {'name': 'Karen', 'code': 'KRN', 'constituency': 'Dagoretti South'},
            {'name': 'Nairobi West', 'code': 'NLW', 'constituency': 'Dagoretti South'},
            {'name': 'Mugumu-ini', 'code': 'MGM', 'constituency': 'Dagoretti South'},
            {'name': 'South C', 'code': 'STC', 'constituency': 'Dagoretti South'},
            {'name': 'Nyayo Highrise', 'code': 'NYH', 'constituency': 'Dagoretti South'},
            {'name': 'Lindi', 'code': 'LND', 'constituency': 'Kibra'},
            {'name': 'Makina', 'code': 'MKN', 'constituency': 'Kibra'},
            {'name': 'Woodley/Kenyatta Golf Course', 'code': 'WKG', 'constituency': 'Kibra'},
            {'name': 'Sarangombe', 'code': 'SRG', 'constituency': 'Kibra'},
            {'name': 'Githurai', 'code': 'GTH', 'constituency': 'Roysambu'},
            {'name': 'Kahawa West', 'code': 'KHW', 'constituency': 'Roysambu'},
            {'name': 'Zimmerman', 'code': 'ZMR', 'constituency': 'Roysambu'},
            {'name': 'Roysambu', 'code': 'RYS', 'constituency': 'Roysambu'},
            {'name': 'Kahawa', 'code': 'KHW2', 'constituency': 'Roysambu'},
            {'name': 'Clay City', 'code': 'CLC', 'constituency': 'Kasarani'},
            {'name': 'Mwiki', 'code': 'MWK', 'constituency': 'Kasarani'},
            {'name': 'Kasarani', 'code': 'KSR', 'constituency': 'Kasarani'},
            {'name': 'Njiru', 'code': 'NJR', 'constituency': 'Kasarani'},
            {'name': 'Ruai', 'code': 'RUI', 'constituency': 'Kasarani'},
            {'name': 'Baba Dogo', 'code': 'BBD', 'constituency': 'Ruaraka'},
            {'name': 'Utalii', 'code': 'UTL', 'constituency': 'Ruaraka'},
            {'name': 'Mathare North', 'code': 'MTN', 'constituency': 'Ruaraka'},
            {'name': 'Lucky Summer', 'code': 'LKS', 'constituency': 'Ruaraka'},
            {'name': 'Korogocho', 'code': 'KRG', 'constituency': 'Ruaraka'},
            {'name': 'Imara Daima', 'code': 'IMD', 'constituency': 'Embakasi South'},
            {'name': 'Kwa Njenga', 'code': 'KWN', 'constituency': 'Embakasi South'},
            {'name': 'Kwa Reuben', 'code': 'KWR2', 'constituency': 'Embakasi South'},
            {'name': 'Pipeline', 'code': 'PPL', 'constituency': 'Embakasi South'},
            {'name': 'Kware', 'code': 'KWR3', 'constituency': 'Embakasi South'},
            {'name': 'Dandora Area I', 'code': 'DNI', 'constituency': 'Embakasi North'},
            {'name': 'Dandora Area II', 'code': 'DNII', 'constituency': 'Embakasi North'},
            {'name': 'Dandora Area III', 'code': 'DNIII', 'constituency': 'Embakasi North'},
            {'name': 'Dandora Area IV', 'code': 'DNIV', 'constituency': 'Embakasi North'},
            {'name': 'Kayole Central', 'code': 'KYC', 'constituency': 'Embakasi Central'},
            {'name': 'Kayole North', 'code': 'KYN', 'constituency': 'Embakasi Central'},
            {'name': 'Kayole South', 'code': 'KYS', 'constituency': 'Embakasi Central'},
            {'name': 'Komarock', 'code': 'KMR', 'constituency': 'Embakasi Central'},
            {'name': 'Matopeni', 'code': 'MTP', 'constituency': 'Embakasi Central'},
            {'name': 'Upper Savanna', 'code': 'UPS', 'constituency': 'Embakasi East'},
            {'name': 'Lower Savanna', 'code': 'LWS', 'constituency': 'Embakasi East'},
            {'name': 'Embakasi', 'code': 'EMB', 'constituency': 'Embakasi East'},
            {'name': 'Utawala', 'code': 'UTW', 'constituency': 'Embakasi East'},
            {'name': 'Mihang\'o', 'code': 'MHG', 'constituency': 'Embakasi East'},
            {'name': 'Umoja I', 'code': 'UMI', 'constituency': 'Embakasi West'},
            {'name': 'Umoja II', 'code': 'UMII', 'constituency': 'Embakasi West'},
            {'name': 'Mowlem', 'code': 'MWL', 'constituency': 'Embakasi West'},
            {'name': 'Kariobangi South', 'code': 'KRS', 'constituency': 'Embakasi West'},
            {'name': 'Maringo/Hamza', 'code': 'MRH', 'constituency': 'Makadara'},
            {'name': 'Viwandani', 'code': 'VWD', 'constituency': 'Makadara'},
            {'name': 'Harambee', 'code': 'HRB', 'constituency': 'Makadara'},
            {'name': 'Makongeni', 'code': 'MKG', 'constituency': 'Makadara'},
            {'name': 'Pumwani', 'code': 'PMW', 'constituency': 'Makadara'},
            {'name': 'Eastleigh North', 'code': 'ELN', 'constituency': 'Kamukunji'},
            {'name': 'Eastleigh South', 'code': 'ELS', 'constituency': 'Kamukunji'},
            {'name': 'Airbase', 'code': 'ARB', 'constituency': 'Kamukunji'},
            {'name': 'California', 'code': 'CLF', 'constituency': 'Kamukunji'},
            {'name': 'Nairobi Central', 'code': 'NLC', 'constituency': 'Starehe'},
            {'name': 'Ngara', 'code': 'NGR', 'constituency': 'Starehe'},
            {'name': 'Pangani', 'code': 'PNG', 'constituency': 'Starehe'},
            {'name': 'Ziwani/Kariokor', 'code': 'ZWK', 'constituency': 'Starehe'},
            {'name': 'Landimawe', 'code': 'LDW', 'constituency': 'Starehe'},
            {'name': 'Nairobi South', 'code': 'NLS', 'constituency': 'Starehe'},
            {'name': 'Hospital', 'code': 'HSP', 'constituency': 'Starehe'},
            {'name': 'Mabatini', 'code': 'MBN', 'constituency': 'Mathare'},
            {'name': 'Huruma', 'code': 'HRM', 'constituency': 'Mathare'},
            {'name': 'Ngei', 'code': 'NGI', 'constituency': 'Mathare'},
            {'name': 'Mlango Kubwa', 'code': 'MLK', 'constituency': 'Mathare'},
            {'name': 'Kiamutisya', 'code': 'KMT', 'constituency': 'Mathare'},
            {'name': 'Ngei II', 'code': 'NGI2', 'constituency': 'Mathare'},
            {'name': 'Bamburi', 'code': 'BMB', 'constituency': 'Nyali'},
            {'name': 'Shanzu', 'code': 'SHZ', 'constituency': 'Nyali'},
            {'name': 'Mkomani', 'code': 'MKM', 'constituency': 'Nyali'},
            {'name': 'Kongowea', 'code': 'KGW', 'constituency': 'Nyali'},
            {'name': 'Nyali', 'code': 'NYL', 'constituency': 'Nyali'},
            {'name': 'Old Town', 'code': 'OLT', 'constituency': 'Mvita'},
            {'name': 'Tudor', 'code': 'TDR', 'constituency': 'Mvita'},
            {'name': 'Tononoka', 'code': 'TNK', 'constituency': 'Mvita'},
            {'name': 'Shimanzi', 'code': 'SHM', 'constituency': 'Mvita'},
            {'name': 'Bamburi II', 'code': 'BMB2', 'constituency': 'Changamwe'},
            {'name': 'Miritini', 'code': 'MRT', 'constituency': 'Changamwe'},
            {'name': 'Mchangani', 'code': 'MCH', 'constituency': 'Changamwe'},
            {'name': 'Chaani', 'code': 'CHN', 'constituency': 'Changamwe'},
            {'name': 'Jomvu Kuu', 'code': 'JMK', 'constituency': 'Jomvu'},
            {'name': 'Mikindani', 'code': 'MKD2', 'constituency': 'Jomvu'},
            {'name': 'Miritini II', 'code': 'MRT2', 'constituency': 'Jomvu'},
            {'name': 'Bamachari', 'code': 'BMC', 'constituency': 'Kisauni'},
            {'name': 'Shakani', 'code': 'SHK', 'constituency': 'Kisauni'},
            {'name': 'Bondeni', 'code': 'BND', 'constituency': 'Kisauni'},
            {'name': 'Shanzu II', 'code': 'SHZ2', 'constituency': 'Kisauni'},
            {'name': 'Mtwapa', 'code': 'MTW', 'constituency': 'Kisauni'},
            {'name': 'Mtongwe', 'code': 'MTG', 'constituency': 'Likoni'},
            {'name': 'Shika Adabu', 'code': 'SHA', 'constituency': 'Likoni'},
            {'name': 'Bofu', 'code': 'BFU', 'constituency': 'Likoni'},
            {'name': 'Likoni', 'code': 'LKN', 'constituency': 'Likoni'},
            {'name': 'Timbwani', 'code': 'TMB', 'constituency': 'Likoni'},
        ]
        
        for ward_data in wards_data:
            ward, created = Ward.objects.get_or_create(
                ward_name=ward_data['name'],
                defaults={
                    'ward_code': ward_data['code'],
                    'constituency': constituencies[ward_data['constituency']]
                }
            )
            if created:
                self.stdout.write(f'Created ward: {ward.ward_name} in {ward.constituency.constituency_name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated geography tables with {len(counties)} counties, '
                f'{len(constituencies)} constituencies, and {len(wards_data)} wards'
            )
        )
