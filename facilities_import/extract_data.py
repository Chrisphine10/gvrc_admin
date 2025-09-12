#!/usr/bin/env python3
"""
Data extraction and population script for GBV facilities
Extracts data from Excel files and populates the database
"""

import os
import sys
import pandas as pd
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gvrc_admin.settings')
django.setup()

from facilities.models import Facility, FacilityType, County, SubCounty

def extract_excel_data():
    """Extract data from all Excel files in the raw data directory"""
    raw_data_dir = Path(__file__).parent / 'data' / 'raw'
    
    # Process each Excel file
    excel_files = [
        'FGM resources materials.xlsx',
        'GBV SDTATION PILOT.xlsx', 
        'NAIROBI LIST OF POLICE STATIONS.xlsx'
    ]
    
    all_data = []
    
    for file_name in excel_files:
        file_path = raw_data_dir / file_name
        if file_path.exists():
            print(f"Processing {file_name}...")
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Add source file info
                df['source_file'] = file_name
                
                # Clean column names
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                
                all_data.append(df)
                print(f"Extracted {len(df)} rows from {file_name}")
                
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    return all_data

def create_facility_types():
    """Create basic facility types"""
    types = [
        'Police Station',
        'Health Facility', 
        'Legal Aid Center',
        'Shelter/Safe House',
        'Counseling Center',
        'Government Office',
        'NGO/CBO',
        'Court',
        'Other'
    ]
    
    for type_name in types:
        facility_type, created = FacilityType.objects.get_or_create(
            name=type_name,
            defaults={'description': f'{type_name} providing GBV services'}
        )
        if created:
            print(f"Created facility type: {type_name}")

def create_counties():
    """Create basic counties (focusing on Nairobi for now)"""
    counties = [
        'Nairobi',
        'Kiambu', 
        'Machakos',
        'Kajiado',
        'Murang\'a'
    ]
    
    for county_name in counties:
        county, created = County.objects.get_or_create(
            name=county_name,
            defaults={'code': county_name.upper()[:3]}
        )
        if created:
            print(f"Created county: {county_name}")

def populate_facilities(data_frames):
    """Populate facilities from extracted data"""
    
    # Get default values
    default_county = County.objects.get_or_create(name='Nairobi')[0]
    police_type = FacilityType.objects.get_or_create(name='Police Station')[0]
    health_type = FacilityType.objects.get_or_create(name='Health Facility')[0]
    other_type = FacilityType.objects.get_or_create(name='Other')[0]
    
    facilities_created = 0
    
    for df in data_frames:
        source_file = df['source_file'].iloc[0] if 'source_file' in df.columns else 'unknown'
        
        # Determine facility type based on source file
        if 'police' in source_file.lower():
            facility_type = police_type
        elif 'health' in source_file.lower() or 'medical' in source_file.lower():
            facility_type = health_type
        else:
            facility_type = other_type
        
        # Process each row
        for _, row in df.iterrows():
            try:
                # Extract facility name (try common column names)
                name = None
                for col in ['name', 'facility_name', 'station_name', 'organization', 'title']:
                    if col in df.columns and pd.notna(row.get(col)):
                        name = str(row[col]).strip()
                        break
                
                if not name:
                    # Use first non-null string column as name
                    for col in df.columns:
                        if pd.notna(row[col]) and isinstance(row[col], str) and len(str(row[col]).strip()) > 2:
                            name = str(row[col]).strip()
                            break
                
                if not name:
                    continue
                
                # Extract other fields
                address = ''
                phone = ''
                email = ''
                
                # Try to find address
                for col in ['address', 'location', 'area', 'sub_county']:
                    if col in df.columns and pd.notna(row.get(col)):
                        address += str(row[col]) + ' '
                
                # Try to find phone
                for col in ['phone', 'telephone', 'contact', 'mobile']:
                    if col in df.columns and pd.notna(row.get(col)):
                        phone = str(row[col]).strip()
                        break
                
                # Try to find email
                for col in ['email', 'e_mail', 'email_address']:
                    if col in df.columns and pd.notna(row.get(col)):
                        email = str(row[col]).strip()
                        break
                
                # Create facility
                facility, created = Facility.objects.get_or_create(
                    name=name,
                    defaults={
                        'facility_type': facility_type,
                        'county': default_county,
                        'address': address.strip(),
                        'phone': phone,
                        'email': email,
                        'is_active': True,
                        'services_offered': f'Services from {source_file}'
                    }
                )
                
                if created:
                    facilities_created += 1
                    print(f"Created facility: {name}")
                
            except Exception as e:
                print(f"Error creating facility from row: {e}")
                continue
    
    print(f"Total facilities created: {facilities_created}")

def main():
    """Main execution function"""
    print("Starting data extraction and population...")
    
    # Create basic reference data
    print("Creating facility types...")
    create_facility_types()
    
    print("Creating counties...")
    create_counties()
    
    # Extract data from Excel files
    print("Extracting data from Excel files...")
    data_frames = extract_excel_data()
    
    if not data_frames:
        print("No data extracted. Exiting.")
        return
    
    # Populate facilities
    print("Populating facilities...")
    populate_facilities(data_frames)
    
    print("Data population completed!")

if __name__ == '__main__':
    main()