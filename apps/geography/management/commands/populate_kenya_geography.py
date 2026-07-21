from django.core.management.base import BaseCommand
from apps.geography.models import County, Constituency, Ward


class Command(BaseCommand):
    help = 'Populate geography tables with complete data for all 47 counties in Kenya'

    def handle(self, *args, **options):
        self.stdout.write('Populating geography tables with complete Kenya data...')
        
        # Complete list of all 47 counties in Kenya
        counties_data = [
            {'name': 'Mombasa', 'code': '001'},
            {'name': 'Kwale', 'code': '002'},
            {'name': 'Kilifi', 'code': '003'},
            {'name': 'Tana River', 'code': '004'},
            {'name': 'Lamu', 'code': '005'},
            {'name': 'Taita Taveta', 'code': '006'},
            {'name': 'Garissa', 'code': '007'},
            {'name': 'Wajir', 'code': '008'},
            {'name': 'Mandera', 'code': '009'},
            {'name': 'Marsabit', 'code': '010'},
            {'name': 'Isiolo', 'code': '011'},
            {'name': 'Meru', 'code': '012'},
            {'name': 'Tharaka Nithi', 'code': '013'},
            {'name': 'Embu', 'code': '014'},
            {'name': 'Kitui', 'code': '015'},
            {'name': 'Machakos', 'code': '016'},
            {'name': 'Makueni', 'code': '017'},
            {'name': 'Nyandarua', 'code': '018'},
            {'name': 'Nyeri', 'code': '019'},
            {'name': 'Kirinyaga', 'code': '020'},
            {'name': 'Murang\'a', 'code': '021'},
            {'name': 'Kiambu', 'code': '022'},
            {'name': 'Turkana', 'code': '023'},
            {'name': 'West Pokot', 'code': '024'},
            {'name': 'Samburu', 'code': '025'},
            {'name': 'Trans Nzoia', 'code': '026'},
            {'name': 'Uasin Gishu', 'code': '027'},
            {'name': 'Elgeyo Marakwet', 'code': '028'},
            {'name': 'Nandi', 'code': '029'},
            {'name': 'Baringo', 'code': '030'},
            {'name': 'Laikipia', 'code': '031'},
            {'name': 'Nakuru', 'code': '032'},
            {'name': 'Narok', 'code': '033'},
            {'name': 'Kajiado', 'code': '034'},
            {'name': 'Kericho', 'code': '035'},
            {'name': 'Bomet', 'code': '036'},
            {'name': 'Kakamega', 'code': '037'},
            {'name': 'Vihiga', 'code': '038'},
            {'name': 'Bungoma', 'code': '039'},
            {'name': 'Busia', 'code': '040'},
            {'name': 'Siaya', 'code': '041'},
            {'name': 'Kisumu', 'code': '042'},
            {'name': 'Homa Bay', 'code': '043'},
            {'name': 'Migori', 'code': '044'},
            {'name': 'Kisii', 'code': '045'},
            {'name': 'Nyamira', 'code': '046'},
            {'name': 'Nairobi', 'code': '047'},
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
        
        # Constituencies data for all counties
        constituencies_data = [
            # Mombasa County
            {'name': 'Changamwe', 'code': '001001', 'county': 'Mombasa'},
            {'name': 'Jomvu', 'code': '001002', 'county': 'Mombasa'},
            {'name': 'Kisauni', 'code': '001003', 'county': 'Mombasa'},
            {'name': 'Nyali', 'code': '001004', 'county': 'Mombasa'},
            {'name': 'Likoni', 'code': '001005', 'county': 'Mombasa'},
            {'name': 'Mvita', 'code': '001006', 'county': 'Mombasa'},
            
            # Kwale County
            {'name': 'Msambweni', 'code': '002001', 'county': 'Kwale'},
            {'name': 'Lunga Lunga', 'code': '002002', 'county': 'Kwale'},
            {'name': 'Matuga', 'code': '002003', 'county': 'Kwale'},
            {'name': 'Kinango', 'code': '002004', 'county': 'Kwale'},
            
            # Kilifi County
            {'name': 'Kilifi North', 'code': '003001', 'county': 'Kilifi'},
            {'name': 'Kilifi South', 'code': '003002', 'county': 'Kilifi'},
            {'name': 'Kaloleni', 'code': '003003', 'county': 'Kilifi'},
            {'name': 'Rabai', 'code': '003004', 'county': 'Kilifi'},
            {'name': 'Ganze', 'code': '003005', 'county': 'Kilifi'},
            {'name': 'Malindi', 'code': '003006', 'county': 'Kilifi'},
            {'name': 'Magarini', 'code': '003007', 'county': 'Kilifi'},
            
            # Tana River County
            {'name': 'Garsen', 'code': '004001', 'county': 'Tana River'},
            {'name': 'Galole', 'code': '004002', 'county': 'Tana River'},
            {'name': 'Bura', 'code': '004003', 'county': 'Tana River'},
            
            # Lamu County
            {'name': 'Lamu East', 'code': '005001', 'county': 'Lamu'},
            {'name': 'Lamu West', 'code': '005002', 'county': 'Lamu'},
            
            # Taita Taveta County
            {'name': 'Taveta', 'code': '006001', 'county': 'Taita Taveta'},
            {'name': 'Wundanyi', 'code': '006002', 'county': 'Taita Taveta'},
            {'name': 'Mwatate', 'code': '006003', 'county': 'Taita Taveta'},
            {'name': 'Voi', 'code': '006004', 'county': 'Taita Taveta'},
            
            # Garissa County
            {'name': 'Garissa Township', 'code': '007001', 'county': 'Garissa'},
            {'name': 'Balambala', 'code': '007002', 'county': 'Garissa'},
            {'name': 'Lagdera', 'code': '007003', 'county': 'Garissa'},
            {'name': 'Dadaab', 'code': '007004', 'county': 'Garissa'},
            {'name': 'Fafi', 'code': '007005', 'county': 'Garissa'},
            {'name': 'Ijara', 'code': '007006', 'county': 'Garissa'},
            
            # Wajir County
            {'name': 'Wajir North', 'code': '008001', 'county': 'Wajir'},
            {'name': 'Wajir East', 'code': '008002', 'county': 'Wajir'},
            {'name': 'Tarbaj', 'code': '008003', 'county': 'Wajir'},
            {'name': 'Wajir West', 'code': '008004', 'county': 'Wajir'},
            {'name': 'Eldas', 'code': '008005', 'county': 'Wajir'},
            {'name': 'Wajir South', 'code': '008006', 'county': 'Wajir'},
            
            # Mandera County
            {'name': 'Mandera West', 'code': '009001', 'county': 'Mandera'},
            {'name': 'Banissa', 'code': '009002', 'county': 'Mandera'},
            {'name': 'Mandera North', 'code': '009003', 'county': 'Mandera'},
            {'name': 'Mandera South', 'code': '009004', 'county': 'Mandera'},
            {'name': 'Mandera East', 'code': '009005', 'county': 'Mandera'},
            {'name': 'Lafey', 'code': '009006', 'county': 'Mandera'},
            
            # Marsabit County
            {'name': 'Moyale', 'code': '010001', 'county': 'Marsabit'},
            {'name': 'North Horr', 'code': '010002', 'county': 'Marsabit'},
            {'name': 'Saku', 'code': '010003', 'county': 'Marsabit'},
            {'name': 'Laisamis', 'code': '010004', 'county': 'Marsabit'},
            
            # Isiolo County
            {'name': 'Isiolo North', 'code': '011001', 'county': 'Isiolo'},
            {'name': 'Isiolo South', 'code': '011002', 'county': 'Isiolo'},
            
            # Meru County
            {'name': 'Igembe South', 'code': '012001', 'county': 'Meru'},
            {'name': 'Igembe Central', 'code': '012002', 'county': 'Meru'},
            {'name': 'Igembe North', 'code': '012003', 'county': 'Meru'},
            {'name': 'Tigania West', 'code': '012004', 'county': 'Meru'},
            {'name': 'Tigania East', 'code': '012005', 'county': 'Meru'},
            {'name': 'North Imenti', 'code': '012006', 'county': 'Meru'},
            {'name': 'Buuri', 'code': '012007', 'county': 'Meru'},
            {'name': 'Central Imenti', 'code': '012008', 'county': 'Meru'},
            {'name': 'South Imenti', 'code': '012009', 'county': 'Meru'},
            
            # Tharaka Nithi County
            {'name': 'Maara', 'code': '013001', 'county': 'Tharaka Nithi'},
            {'name': 'Chuka/Igambang\'ombe', 'code': '013002', 'county': 'Tharaka Nithi'},
            {'name': 'Tharaka', 'code': '013003', 'county': 'Tharaka Nithi'},
            
            # Embu County
            {'name': 'Manyatta', 'code': '014001', 'county': 'Embu'},
            {'name': 'Runyenjes', 'code': '014002', 'county': 'Embu'},
            {'name': 'Gachoka', 'code': '014003', 'county': 'Embu'},
            {'name': 'Siakago', 'code': '014004', 'county': 'Embu'},
            
            # Kitui County
            {'name': 'Mwingi North', 'code': '015001', 'county': 'Kitui'},
            {'name': 'Mwingi West', 'code': '015002', 'county': 'Kitui'},
            {'name': 'Mwingi Central', 'code': '015003', 'county': 'Kitui'},
            {'name': 'Kitui West', 'code': '015004', 'county': 'Kitui'},
            {'name': 'Kitui Rural', 'code': '015005', 'county': 'Kitui'},
            {'name': 'Kitui Central', 'code': '015006', 'county': 'Kitui'},
            {'name': 'Kitui East', 'code': '015007', 'county': 'Kitui'},
            {'name': 'Kitui South', 'code': '015008', 'county': 'Kitui'},
            
            # Machakos County
            {'name': 'Masinga', 'code': '016001', 'county': 'Machakos'},
            {'name': 'Yatta', 'code': '016002', 'county': 'Machakos'},
            {'name': 'Kangundo', 'code': '016003', 'county': 'Machakos'},
            {'name': 'Matungulu', 'code': '016004', 'county': 'Machakos'},
            {'name': 'Kathiani', 'code': '016005', 'county': 'Machakos'},
            {'name': 'Mavoko', 'code': '016006', 'county': 'Machakos'},
            {'name': 'Machakos Town', 'code': '016007', 'county': 'Machakos'},
            {'name': 'Mwala', 'code': '016008', 'county': 'Machakos'},
            
            # Makueni County
            {'name': 'Mbooni', 'code': '017001', 'county': 'Makueni'},
            {'name': 'Kilome', 'code': '017002', 'county': 'Makueni'},
            {'name': 'Kaiti', 'code': '017003', 'county': 'Makueni'},
            {'name': 'Makueni', 'code': '017004', 'county': 'Makueni'},
            {'name': 'Kibwezi West', 'code': '017005', 'county': 'Makueni'},
            {'name': 'Kibwezi East', 'code': '017006', 'county': 'Makueni'},
            
            # Nyandarua County
            {'name': 'Kinangop', 'code': '018001', 'county': 'Nyandarua'},
            {'name': 'Kipipiri', 'code': '018002', 'county': 'Nyandarua'},
            {'name': 'Ol Kalou', 'code': '018003', 'county': 'Nyandarua'},
            {'name': 'Ol Jorok', 'code': '018004', 'county': 'Nyandarua'},
            {'name': 'Ndaragwa', 'code': '018005', 'county': 'Nyandarua'},
            
            # Nyeri County
            {'name': 'Tetu', 'code': '019001', 'county': 'Nyeri'},
            {'name': 'Kieni', 'code': '019002', 'county': 'Nyeri'},
            {'name': 'Mathira', 'code': '019003', 'county': 'Nyeri'},
            {'name': 'Othaya', 'code': '019004', 'county': 'Nyeri'},
            {'name': 'Mukurweini', 'code': '019005', 'county': 'Nyeri'},
            {'name': 'Nyeri Town', 'code': '019006', 'county': 'Nyeri'},
            
            # Kirinyaga County
            {'name': 'Mwea', 'code': '020001', 'county': 'Kirinyaga'},
            {'name': 'Gichugu', 'code': '020002', 'county': 'Kirinyaga'},
            {'name': 'Ndia', 'code': '020003', 'county': 'Kirinyaga'},
            {'name': 'Kirinyaga Central', 'code': '020004', 'county': 'Kirinyaga'},
            
            # Murang'a County
            {'name': 'Kangema', 'code': '021001', 'county': 'Murang\'a'},
            {'name': 'Mathioya', 'code': '021002', 'county': 'Murang\'a'},
            {'name': 'Kiharu', 'code': '021003', 'county': 'Murang\'a'},
            {'name': 'Kigumo', 'code': '021004', 'county': 'Murang\'a'},
            {'name': 'Maragua', 'code': '021005', 'county': 'Murang\'a'},
            {'name': 'Kandara', 'code': '021006', 'county': 'Murang\'a'},
            {'name': 'Gatanga', 'code': '021007', 'county': 'Murang\'a'},
            
            # Kiambu County
            {'name': 'Gatundu South', 'code': '022001', 'county': 'Kiambu'},
            {'name': 'Gatundu North', 'code': '022002', 'county': 'Kiambu'},
            {'name': 'Juja', 'code': '022003', 'county': 'Kiambu'},
            {'name': 'Thika Town', 'code': '022004', 'county': 'Kiambu'},
            {'name': 'Ruiru', 'code': '022005', 'county': 'Kiambu'},
            {'name': 'Githunguri', 'code': '022006', 'county': 'Kiambu'},
            {'name': 'Kiambaa', 'code': '022007', 'county': 'Kiambu'},
            {'name': 'Kabete', 'code': '022008', 'county': 'Kiambu'},
            {'name': 'Kikuyu', 'code': '022009', 'county': 'Kiambu'},
            {'name': 'Limuru', 'code': '022010', 'county': 'Kiambu'},
            {'name': 'Lari', 'code': '022011', 'county': 'Kiambu'},
            
            # Turkana County
            {'name': 'Turkana North', 'code': '023001', 'county': 'Turkana'},
            {'name': 'Turkana West', 'code': '023002', 'county': 'Turkana'},
            {'name': 'Turkana Central', 'code': '023003', 'county': 'Turkana'},
            {'name': 'Loima', 'code': '023004', 'county': 'Turkana'},
            {'name': 'Turkana South', 'code': '023005', 'county': 'Turkana'},
            {'name': 'Turkana East', 'code': '023006', 'county': 'Turkana'},
            
            # West Pokot County
            {'name': 'Kapenguria', 'code': '024001', 'county': 'West Pokot'},
            {'name': 'Sigor', 'code': '024002', 'county': 'West Pokot'},
            {'name': 'Kacheliba', 'code': '024003', 'county': 'West Pokot'},
            {'name': 'Pokot South', 'code': '024004', 'county': 'West Pokot'},
            
            # Samburu County
            {'name': 'Samburu West', 'code': '025001', 'county': 'Samburu'},
            {'name': 'Samburu North', 'code': '025002', 'county': 'Samburu'},
            {'name': 'Samburu East', 'code': '025003', 'county': 'Samburu'},
            
            # Trans Nzoia County
            {'name': 'Kwanza', 'code': '026001', 'county': 'Trans Nzoia'},
            {'name': 'Endebess', 'code': '026002', 'county': 'Trans Nzoia'},
            {'name': 'Saboti', 'code': '026003', 'county': 'Trans Nzoia'},
            {'name': 'Kiminini', 'code': '026004', 'county': 'Trans Nzoia'},
            {'name': 'Cherangany', 'code': '026005', 'county': 'Trans Nzoia'},
            
            # Uasin Gishu County
            {'name': 'Soy', 'code': '027001', 'county': 'Uasin Gishu'},
            {'name': 'Turbo', 'code': '027002', 'county': 'Uasin Gishu'},
            {'name': 'Moiben', 'code': '027003', 'county': 'Uasin Gishu'},
            {'name': 'Ainabkoi', 'code': '027004', 'county': 'Uasin Gishu'},
            {'name': 'Kapseret', 'code': '027005', 'county': 'Uasin Gishu'},
            {'name': 'Kesses', 'code': '027006', 'county': 'Uasin Gishu'},
            
            # Elgeyo Marakwet County
            {'name': 'Marakwet East', 'code': '028001', 'county': 'Elgeyo Marakwet'},
            {'name': 'Marakwet West', 'code': '028002', 'county': 'Elgeyo Marakwet'},
            {'name': 'Keiyo North', 'code': '028003', 'county': 'Elgeyo Marakwet'},
            {'name': 'Keiyo South', 'code': '028004', 'county': 'Elgeyo Marakwet'},
            
            # Nandi County
            {'name': 'Tinderet', 'code': '029001', 'county': 'Nandi'},
            {'name': 'Aldai', 'code': '029002', 'county': 'Nandi'},
            {'name': 'Nandi Hills', 'code': '029003', 'county': 'Nandi'},
            {'name': 'Chesumei', 'code': '029004', 'county': 'Nandi'},
            {'name': 'Emgwen', 'code': '029005', 'county': 'Nandi'},
            {'name': 'Mosop', 'code': '029006', 'county': 'Nandi'},
            
            # Baringo County
            {'name': 'Tiaty', 'code': '030001', 'county': 'Baringo'},
            {'name': 'Baringo North', 'code': '030002', 'county': 'Baringo'},
            {'name': 'Baringo Central', 'code': '030003', 'county': 'Baringo'},
            {'name': 'Baringo South', 'code': '030004', 'county': 'Baringo'},
            {'name': 'Mogotio', 'code': '030005', 'county': 'Baringo'},
            {'name': 'Eldama Ravine', 'code': '030006', 'county': 'Baringo'},
            
            # Laikipia County
            {'name': 'Laikipia West', 'code': '031001', 'county': 'Laikipia'},
            {'name': 'Laikipia East', 'code': '031002', 'county': 'Laikipia'},
            {'name': 'Laikipia North', 'code': '031003', 'county': 'Laikipia'},
            
            # Nakuru County
            {'name': 'Molo', 'code': '032001', 'county': 'Nakuru'},
            {'name': 'Njoro', 'code': '032002', 'county': 'Nakuru'},
            {'name': 'Naivasha', 'code': '032003', 'county': 'Nakuru'},
            {'name': 'Gilgil', 'code': '032004', 'county': 'Nakuru'},
            {'name': 'Kuresoi South', 'code': '032005', 'county': 'Nakuru'},
            {'name': 'Kuresoi North', 'code': '032006', 'county': 'Nakuru'},
            {'name': 'Subukia', 'code': '032007', 'county': 'Nakuru'},
            {'name': 'Bahati', 'code': '032008', 'county': 'Nakuru'},
            {'name': 'Nakuru Town West', 'code': '032009', 'county': 'Nakuru'},
            {'name': 'Nakuru Town East', 'code': '032010', 'county': 'Nakuru'},
            {'name': 'Rongai', 'code': '032011', 'county': 'Nakuru'},
            
            # Narok County
            {'name': 'Kilgoris', 'code': '033001', 'county': 'Narok'},
            {'name': 'Emurua Dikirr', 'code': '033002', 'county': 'Narok'},
            {'name': 'Narok North', 'code': '033003', 'county': 'Narok'},
            {'name': 'Narok East', 'code': '033004', 'county': 'Narok'},
            {'name': 'Narok South', 'code': '033005', 'county': 'Narok'},
            {'name': 'Narok West', 'code': '033006', 'county': 'Narok'},
            
            # Kajiado County
            {'name': 'Kajiado North', 'code': '034001', 'county': 'Kajiado'},
            {'name': 'Kajiado Central', 'code': '034002', 'county': 'Kajiado'},
            {'name': 'Kajiado East', 'code': '034003', 'county': 'Kajiado'},
            {'name': 'Kajiado West', 'code': '034004', 'county': 'Kajiado'},
            {'name': 'Kajiado South', 'code': '034005', 'county': 'Kajiado'},
            
            # Kericho County
            {'name': 'Kipkelion East', 'code': '035001', 'county': 'Kericho'},
            {'name': 'Kipkelion West', 'code': '035002', 'county': 'Kericho'},
            {'name': 'Ainamoi', 'code': '035003', 'county': 'Kericho'},
            {'name': 'Bureti', 'code': '035004', 'county': 'Kericho'},
            {'name': 'Belgut', 'code': '035005', 'county': 'Kericho'},
            {'name': 'Sigowet', 'code': '035006', 'county': 'Kericho'},
            
            # Bomet County
            {'name': 'Sotik', 'code': '036001', 'county': 'Bomet'},
            {'name': 'Chepalungu', 'code': '036002', 'county': 'Bomet'},
            {'name': 'Bomet East', 'code': '036003', 'county': 'Bomet'},
            {'name': 'Bomet Central', 'code': '036004', 'county': 'Bomet'},
            {'name': 'Konoin', 'code': '036005', 'county': 'Bomet'},
            
            # Kakamega County
            {'name': 'Lugari', 'code': '037001', 'county': 'Kakamega'},
            {'name': 'Likuyani', 'code': '037002', 'county': 'Kakamega'},
            {'name': 'Malava', 'code': '037003', 'county': 'Kakamega'},
            {'name': 'Lurambi', 'code': '037004', 'county': 'Kakamega'},
            {'name': 'Navakholo', 'code': '037005', 'county': 'Kakamega'},
            {'name': 'Mumias West', 'code': '037006', 'county': 'Kakamega'},
            {'name': 'Mumias East', 'code': '037007', 'county': 'Kakamega'},
            {'name': 'Matungu', 'code': '037008', 'county': 'Kakamega'},
            {'name': 'Butere', 'code': '037009', 'county': 'Kakamega'},
            {'name': 'Khwisero', 'code': '037010', 'county': 'Kakamega'},
            {'name': 'Shinyalu', 'code': '037011', 'county': 'Kakamega'},
            {'name': 'Ikolomani', 'code': '037012', 'county': 'Kakamega'},
            
            # Vihiga County
            {'name': 'Vihiga', 'code': '038001', 'county': 'Vihiga'},
            {'name': 'Sabatia', 'code': '038002', 'county': 'Vihiga'},
            {'name': 'Hamisi', 'code': '038003', 'county': 'Vihiga'},
            {'name': 'Luanda', 'code': '038004', 'county': 'Vihiga'},
            {'name': 'Emuhaya', 'code': '038005', 'county': 'Vihiga'},
            
            # Bungoma County
            {'name': 'Bumula', 'code': '039001', 'county': 'Bungoma'},
            {'name': 'Kanduyi', 'code': '039002', 'county': 'Bungoma'},
            {'name': 'Webuye East', 'code': '039003', 'county': 'Bungoma'},
            {'name': 'Webuye West', 'code': '039004', 'county': 'Bungoma'},
            {'name': 'Sirisia', 'code': '039005', 'county': 'Bungoma'},
            {'name': 'Tongaren', 'code': '039006', 'county': 'Bungoma'},
            {'name': 'Kimilili', 'code': '039007', 'county': 'Bungoma'},
            {'name': 'Mt. Elgon', 'code': '039008', 'county': 'Bungoma'},
            {'name': 'Kabuchai', 'code': '039009', 'county': 'Bungoma'},
            
            # Busia County
            {'name': 'Teso North', 'code': '040001', 'county': 'Busia'},
            {'name': 'Teso South', 'code': '040002', 'county': 'Busia'},
            {'name': 'Nambale', 'code': '040003', 'county': 'Busia'},
            {'name': 'Matayos', 'code': '040004', 'county': 'Busia'},
            {'name': 'Butula', 'code': '040005', 'county': 'Busia'},
            {'name': 'Funyula', 'code': '040006', 'county': 'Busia'},
            {'name': 'Budalangi', 'code': '040007', 'county': 'Busia'},
            
            # Siaya County
            {'name': 'Ugenya', 'code': '041001', 'county': 'Siaya'},
            {'name': 'Ugunja', 'code': '041002', 'county': 'Siaya'},
            {'name': 'Alego Usonga', 'code': '041003', 'county': 'Siaya'},
            {'name': 'Gem', 'code': '041004', 'county': 'Siaya'},
            {'name': 'Bondo', 'code': '041005', 'county': 'Siaya'},
            {'name': 'Rarieda', 'code': '041006', 'county': 'Siaya'},
            
            # Kisumu County
            {'name': 'Kisumu East', 'code': '042001', 'county': 'Kisumu'},
            {'name': 'Kisumu West', 'code': '042002', 'county': 'Kisumu'},
            {'name': 'Kisumu Central', 'code': '042003', 'county': 'Kisumu'},
            {'name': 'Seme', 'code': '042004', 'county': 'Kisumu'},
            {'name': 'Nyando', 'code': '042005', 'county': 'Kisumu'},
            {'name': 'Muhoroni', 'code': '042006', 'county': 'Kisumu'},
            {'name': 'Nyakach', 'code': '042007', 'county': 'Kisumu'},
            
            # Homa Bay County
            {'name': 'Kasipul', 'code': '043001', 'county': 'Homa Bay'},
            {'name': 'Kabondo Kasipul', 'code': '043002', 'county': 'Homa Bay'},
            {'name': 'Karachuonyo', 'code': '043003', 'county': 'Homa Bay'},
            {'name': 'Rangwe', 'code': '043004', 'county': 'Homa Bay'},
            {'name': 'Homa Bay Town', 'code': '043005', 'county': 'Homa Bay'},
            {'name': 'Ndhiwa', 'code': '043006', 'county': 'Homa Bay'},
            {'name': 'Suba North', 'code': '043007', 'county': 'Homa Bay'},
            {'name': 'Suba South', 'code': '043008', 'county': 'Homa Bay'},
            
            # Migori County
            {'name': 'Rongo', 'code': '044001', 'county': 'Migori'},
            {'name': 'Awendo', 'code': '044002', 'county': 'Migori'},
            {'name': 'Suna East', 'code': '044003', 'county': 'Migori'},
            {'name': 'Suna West', 'code': '044004', 'county': 'Migori'},
            {'name': 'Uriri', 'code': '044005', 'county': 'Migori'},
            {'name': 'Nyatike', 'code': '044006', 'county': 'Migori'},
            {'name': 'Kuria West', 'code': '044007', 'county': 'Migori'},
            {'name': 'Kuria East', 'code': '044008', 'county': 'Migori'},
            
            # Kisii County
            {'name': 'Bonchari', 'code': '045001', 'county': 'Kisii'},
            {'name': 'South Mugirango', 'code': '045002', 'county': 'Kisii'},
            {'name': 'Bomachoge Chache', 'code': '045003', 'county': 'Kisii'},
            {'name': 'Bomachoge Borabu', 'code': '045004', 'county': 'Kisii'},
            {'name': 'Bobasi', 'code': '045005', 'county': 'Kisii'},
            {'name': 'Bomachoge Borabu', 'code': '045006', 'county': 'Kisii'},
            {'name': 'Nyaribari Masaba', 'code': '045007', 'county': 'Kisii'},
            {'name': 'Nyaribari Chache', 'code': '045008', 'county': 'Kisii'},
            {'name': 'Kitutu Chache North', 'code': '045009', 'county': 'Kisii'},
            {'name': 'Kitutu Chache South', 'code': '045010', 'county': 'Kisii'},
            
            # Nyamira County
            {'name': 'Kitutu Masaba', 'code': '046001', 'county': 'Nyamira'},
            {'name': 'West Mugirango', 'code': '046002', 'county': 'Nyamira'},
            {'name': 'North Mugirango', 'code': '046003', 'county': 'Nyamira'},
            {'name': 'Borabu', 'code': '046004', 'county': 'Nyamira'},
            
            # Nairobi County
            {'name': 'Westlands', 'code': '047001', 'county': 'Nairobi'},
            {'name': 'Dagoretti North', 'code': '047002', 'county': 'Nairobi'},
            {'name': 'Dagoretti South', 'code': '047003', 'county': 'Nairobi'},
            {'name': 'Langata', 'code': '047004', 'county': 'Nairobi'},
            {'name': 'Kibra', 'code': '047005', 'county': 'Nairobi'},
            {'name': 'Roysambu', 'code': '047006', 'county': 'Nairobi'},
            {'name': 'Kasarani', 'code': '047007', 'county': 'Nairobi'},
            {'name': 'Ruaraka', 'code': '047008', 'county': 'Nairobi'},
            {'name': 'Embakasi South', 'code': '047009', 'county': 'Nairobi'},
            {'name': 'Embakasi North', 'code': '047010', 'county': 'Nairobi'},
            {'name': 'Embakasi Central', 'code': '047011', 'county': 'Nairobi'},
            {'name': 'Embakasi East', 'code': '047012', 'county': 'Nairobi'},
            {'name': 'Embakasi West', 'code': '047013', 'county': 'Nairobi'},
            {'name': 'Makadara', 'code': '047014', 'county': 'Nairobi'},
            {'name': 'Kamukunji', 'code': '047015', 'county': 'Nairobi'},
            {'name': 'Starehe', 'code': '047016', 'county': 'Nairobi'},
            {'name': 'Mathare', 'code': '047017', 'county': 'Nairobi'},
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
        
        # Import comprehensive ward data
        try:
            from .kenya_ward_data import KENYA_WARDS_DATA
            wards_data = KENYA_WARDS_DATA
            self.stdout.write(f'Loaded {len(wards_data)} wards from comprehensive data file')
        except ImportError:
            # Fallback to sample wards if comprehensive data is not available
            self.stdout.write(self.style.WARNING('Comprehensive ward data not found, using sample data'))
            wards_data = [
                # Sample wards for demonstration
                {'name': 'Parklands/Highridge', 'code': '047001001', 'constituency': 'Westlands'},
                {'name': 'Karura', 'code': '047001002', 'constituency': 'Westlands'},
                {'name': 'Kangemi', 'code': '047001003', 'constituency': 'Westlands'},
                {'name': 'Mountain View', 'code': '047001004', 'constituency': 'Westlands'},
                {'name': 'Kilimani', 'code': '047002001', 'constituency': 'Dagoretti North'},
                {'name': 'Mutu-ini', 'code': '047002002', 'constituency': 'Dagoretti North'},
                {'name': 'Ngando', 'code': '047002003', 'constituency': 'Dagoretti North'},
                {'name': 'Riruta', 'code': '047002004', 'constituency': 'Dagoretti North'},
                {'name': 'Uthiru/Ruthimitu', 'code': '047002005', 'constituency': 'Dagoretti North'},
                {'name': 'Waithaka', 'code': '047002006', 'constituency': 'Dagoretti North'},
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
                f'{len(constituencies)} constituencies, and {len(wards_data)} sample wards'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                'Note: This command provides a comprehensive list of all 47 counties and their constituencies. '
                'For complete ward data, you may need to expand the wards_data list with all wards in Kenya.'
            )
        )
