#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Extract Facility Contacts for Human Resources Registration
This script extracts all facility contacts and formats them for addition to the HR system.
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from apps.facilities.models import FacilityContact, Facility
from apps.lookups.models import ContactType
from django.db.models import Count, Q


def extract_facility_contacts_for_hr():
    """
    Extract all facility contacts and format them for Human Resources registration.
    Returns data ready to be added to the HR contacts system.
    """
    
    print("="*80)
    print("FACILITY CONTACTS EXTRACTION FOR HUMAN RESOURCES")
    print("="*80)
    print()
    
    # Get all active facility contacts
    contacts = FacilityContact.objects.filter(
        is_active=True
    ).select_related(
        'facility',
        'facility__ward__constituency__county',
        'facility__operational_status',
        'contact_type'
    ).prefetch_related(
        'facility__facilityservice_set__service_category'
    ).order_by('facility__facility_name', 'contact_type__type_name')
    
    total_contacts = contacts.count()
    print(f"Total Active Facility Contacts: {total_contacts}")
    print()
    
    # Group by contact type
    print("Contacts by Type:")
    contacts_by_type = {}
    for contact in contacts:
        type_name = contact.contact_type.type_name
        if type_name not in contacts_by_type:
            contacts_by_type[type_name] = []
        contacts_by_type[type_name].append(contact)
    
    for type_name, type_contacts in contacts_by_type.items():
        print(f"  {type_name}: {len(type_contacts)}")
    print()
    
    # Prepare data for HR registration
    hr_contacts_data = []
    
    for contact in contacts:
        # Get facility services
        services = []
        for service in contact.facility.facilityservice_set.filter(is_active=True)[:5]:
            services.append(service.service_category.category_name if service.service_category else 'Unknown')
        
        # Build contact data structure
        contact_data = {
            'contact_id': contact.contact_id,
            'facility_id': contact.facility.facility_id,
            'facility_name': contact.facility.facility_name,
            'facility_code': contact.facility.facility_code or '',
            'registration_number': contact.facility.registration_number,
            
            # Location information
            'ward': contact.facility.ward.ward_name if contact.facility.ward else '',
            'ward_id': contact.facility.ward.ward_id if contact.facility.ward else None,
            'constituency': contact.facility.ward.constituency.constituency_name if contact.facility.ward and contact.facility.ward.constituency else '',
            'constituency_id': contact.facility.ward.constituency.constituency_id if contact.facility.ward and contact.facility.ward.constituency else None,
            'county': contact.facility.ward.constituency.county.county_name if contact.facility.ward and contact.facility.ward.constituency and contact.facility.ward.constituency.county else '',
            'county_id': contact.facility.ward.constituency.county.county_id if contact.facility.ward and contact.facility.ward.constituency and contact.facility.ward.constituency.county else None,
            
            # Contact information
            'contact_type': contact.contact_type.type_name,
            'contact_type_id': contact.contact_type.contact_type_id,
            'contact_value': contact.contact_value,
            'contact_person_name': contact.contact_person_name or '',
            'is_primary': contact.is_primary,
            
            # Facility status
            'operational_status': contact.facility.operational_status.status_name if contact.facility.operational_status else '',
            'facility_is_active': contact.facility.is_active,
            
            # Services offered
            'services': services,
            'service_count': len(services),
            
            # Metadata
            'created_at': contact.created_at.isoformat() if contact.created_at else None,
            'updated_at': contact.updated_at.isoformat() if contact.updated_at else None,
            'is_active': contact.is_active,
        }
        
        hr_contacts_data.append(contact_data)
    
    # Save to JSON file
    output_file = f'facility_contacts_for_hr_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hr_contacts_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data exported to: {output_file}")
    print(f"✅ Total contacts prepared: {len(hr_contacts_data)}")
    print()
    
    # Generate summary statistics
    print("="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print()
    
    # By county
    counties = {}
    for contact_data in hr_contacts_data:
        county = contact_data['county'] or 'Unknown'
        if county not in counties:
            counties[county] = 0
        counties[county] += 1
    
    print("Contacts by County:")
    for county, count in sorted(counties.items(), key=lambda x: x[1], reverse=True):
        print(f"  {county}: {count}")
    print()
    
    # By contact type
    print("Contacts by Type:")
    for type_name, type_contacts in contacts_by_type.items():
        print(f"  {type_name}: {len(type_contacts)}")
    print()
    
    # Facilities with contacts
    facilities_with_contacts = len(set(c['facility_id'] for c in hr_contacts_data))
    print(f"Facilities with contacts: {facilities_with_contacts}")
    print(f"Average contacts per facility: {total_contacts / facilities_with_contacts:.2f}" if facilities_with_contacts > 0 else "N/A")
    print()
    
    # Primary contacts
    primary_contacts = sum(1 for c in hr_contacts_data if c['is_primary'])
    print(f"Primary contacts: {primary_contacts}")
    print()
    
    # Generate SQL insert statements (optional, for reference)
    print("="*80)
    print("SAMPLE DATA FOR HR REGISTRATION")
    print("="*80)
    print()
    print("First 5 contacts (sample):")
    for i, contact_data in enumerate(hr_contacts_data[:5], 1):
        print(f"\n{i}. {contact_data['facility_name']}")
        print(f"   Contact: {contact_data['contact_type']} - {contact_data['contact_value']}")
        print(f"   Location: {contact_data['ward']}, {contact_data['county']}")
        print(f"   Person: {contact_data['contact_person_name'] or 'N/A'}")
        print(f"   Primary: {'Yes' if contact_data['is_primary'] else 'No'}")
    
    print()
    print("="*80)
    print("NEXT STEPS")
    print("="*80)
    print()
    print("1. Review the exported JSON file:", output_file)
    print("2. The data is ready to be imported into the Human Resources system")
    print("3. All facility contacts are now available for HR registration")
    print("4. Update the human_resources view to include ALL contact types, not just HR-specific ones")
    print()
    print("To include all contacts in HR view, modify apps/home/views.py:")
    print("  - Change line 328-333 to include ALL ContactType objects")
    print("  - Or remove the contact_type filter to show all facility contacts")
    print()
    
    return hr_contacts_data, output_file


if __name__ == '__main__':
    try:
        contacts_data, output_file = extract_facility_contacts_for_hr()
        print(f"✅ Extraction complete! Data saved to: {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



