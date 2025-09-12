#!/usr/bin/env python3
"""
Sample data population script for GBV facilities
Creates sample facilities based on the raw data files
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gvrc_admin.settings')
django.setup()

from facilities.models import Facility, FacilityType, County, SubCounty

def create_facility_types():
    """Create facility types"""
    types = [
        ('Police Station', 'Law enforcement facilities providing GBV response services'),
        ('Health Facility', 'Medical facilities providing GBV survivor care'),
        ('Legal Aid Center', 'Organizations providing legal support to GBV survivors'),
        ('Shelter/Safe House', 'Temporary accommodation for GBV survivors'),
        ('Counseling Center', 'Psychological support and counseling services'),
        ('Government Office', 'Government departments handling GBV cases'),
        ('NGO/CBO', 'Non-governmental organizations supporting GBV survivors'),
        ('Court', 'Judicial facilities handling GBV cases'),
        ('Other', 'Other facilities providing GBV-related services')
    ]
    
    created_count = 0
    for name, description in types:
        facility_type, created = FacilityType.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            created_count += 1
            print(f"Created facility type: {name}")
    
    print(f"Total facility types created: {created_count}")
    return created_count

def create_counties():
    """Create counties"""
    counties = [
        ('Nairobi', 'NAI'),
        ('Kiambu', 'KIA'), 
        ('Machakos', 'MAC'),
        ('Kajiado', 'KAJ'),
        ('Murang\'a', 'MUR'),
        ('Nakuru', 'NAK'),
        ('Mombasa', 'MOB'),
        ('Kisumu', 'KIS')
    ]
    
    created_count = 0
    for name, code in counties:
        county, created = County.objects.get_or_create(
            name=name,
            defaults={'code': code}
        )
        if created:
            created_count += 1
            print(f"Created county: {name}")
    
    print(f"Total counties created: {created_count}")
    return created_count

def create_sub_counties():
    """Create sub-counties for Nairobi"""
    nairobi = County.objects.get(name='Nairobi')
    
    sub_counties = [
        'Westlands', 'Dagoretti North', 'Dagoretti South', 'Langata',
        'Kibra', 'Roysambu', 'Kasarani', 'Ruaraka', 'Embakasi South',
        'Embakasi North', 'Embakasi Central', 'Embakasi East', 'Embakasi West',
        'Makadara', 'Kamukunji', 'Starehe', 'Mathare'
    ]
    
    created_count = 0
    for name in sub_counties:
        sub_county, created = SubCounty.objects.get_or_create(
            name=name,
            county=nairobi,
            defaults={'code': name.upper()[:3]}
        )
        if created:
            created_count += 1
            print(f"Created sub-county: {name}")
    
    print(f"Total sub-counties created: {created_count}")
    return created_count

def create_sample_facilities():
    """Create sample facilities based on the data files"""
    
    # Get reference objects
    nairobi = County.objects.get(name='Nairobi')
    police_type = FacilityType.objects.get(name='Police Station')
    health_type = FacilityType.objects.get(name='Health Facility')
    legal_type = FacilityType.objects.get(name='Legal Aid Center')
    ngo_type = FacilityType.objects.get(name='NGO/CBO')
    
    # Sample police stations (based on NAIROBI LIST OF POLICE STATIONS.xlsx)
    police_stations = [
        ('Central Police Station', 'Nairobi Central, Tom Mboya Street', '020-2222222'),
        ('Kamukunji Police Station', 'Kamukunji, Nairobi', '020-2333333'),
        ('Makadara Police Station', 'Makadara, Nairobi', '020-2444444'),
        ('Starehe Police Station', 'Starehe, Nairobi', '020-2555555'),
        ('Westlands Police Station', 'Westlands, Nairobi', '020-2666666'),
        ('Langata Police Station', 'Langata, Nairobi', '020-2777777'),
        ('Kasarani Police Station', 'Kasarani, Nairobi', '020-2888888'),
        ('Embakasi Police Station', 'Embakasi, Nairobi', '020-2999999'),
        ('Kibra Police Station', 'Kibra, Nairobi', '020-3000000'),
        ('Roysambu Police Station', 'Roysambu, Nairobi', '020-3111111')
    ]
    
    # Sample health facilities
    health_facilities = [
        ('Kenyatta National Hospital', 'Hospital Road, Upper Hill', '020-2726300'),
        ('Nairobi Hospital', 'Argwings Kodhek Road', '020-2845000'),
        ('Mama Lucy Kibaki Hospital', 'Embakasi, Nairobi', '020-2345678'),
        ('Mbagathi Hospital', 'Mbagathi Way, Nairobi', '020-3456789'),
        ('Pumwani Maternity Hospital', 'Pumwani, Nairobi', '020-4567890'),
        ('Mathare Mental Hospital', 'Mathare, Nairobi', '020-5678901'),
        ('City Hall Clinic', 'City Hall Way, Nairobi', '020-6789012')
    ]
    
    # Sample legal aid centers
    legal_centers = [
        ('FIDA Kenya', 'Argwings Kodhek Road', '020-3874220'),
        ('Legal Resources Foundation', 'Milimani Road', '020-2713540'),
        ('Kituo Cha Sheria', 'Nairobi CBD', '020-3874220'),
        ('Kenya National Commission on Human Rights', 'Valley Road', '020-2270000')
    ]
    
    # Sample NGOs/CBOs
    ngos = [
        ('Coalition on Violence Against Women', 'Nairobi', '020-4444444'),
        ('Gender Violence Recovery Centre', 'Nairobi Hospital', '020-2845000'),
        ('Wangu Kanja Foundation', 'Nairobi', '020-5555555'),
        ('Centre for Rights Education and Awareness', 'Nairobi', '020-6666666')
    ]
    
    facilities_data = [
        (police_stations, police_type, 'Police services including GBV case reporting and investigation'),
        (health_facilities, health_type, 'Medical care, counseling, and support for GBV survivors'),
        (legal_centers, legal_type, 'Legal aid and representation for GBV survivors'),
        (ngos, ngo_type, 'Advocacy, support, and rehabilitation services for GBV survivors')
    ]
    
    created_count = 0
    for facilities_list, facility_type, services in facilities_data:
        for name, address, phone in facilities_list:
            facility, created = Facility.objects.get_or_create(
                name=name,
                defaults={
                    'facility_type': facility_type,
                    'county': nairobi,
                    'address': address,
                    'phone': phone,
                    'email': f'{name.lower().replace(" ", ".")}@example.com',
                    'is_active': True,
                    'services_offered': services,
                    'operating_hours': '24/7' if facility_type == police_type else '8:00 AM - 5:00 PM'
                }
            )
            
            if created:
                created_count += 1
                print(f"Created facility: {name}")
    
    print(f"Total facilities created: {created_count}")
    return created_count

def main():
    """Main execution function"""
    print("=" * 50)
    print("GBV FACILITIES DATA POPULATION")
    print("=" * 50)
    
    print("\n1. Creating facility types...")
    create_facility_types()
    
    print("\n2. Creating counties...")
    create_counties()
    
    print("\n3. Creating sub-counties...")
    create_sub_counties()
    
    print("\n4. Creating sample facilities...")
    create_sample_facilities()
    
    # Print summary
    print("\n" + "=" * 50)
    print("DATA POPULATION SUMMARY")
    print("=" * 50)
    print(f"Facility Types: {FacilityType.objects.count()}")
    print(f"Counties: {County.objects.count()}")
    print(f"Sub-Counties: {SubCounty.objects.count()}")
    print(f"Facilities: {Facility.objects.count()}")
    print("=" * 50)
    print("Data population completed successfully!")

if __name__ == '__main__':
    main()