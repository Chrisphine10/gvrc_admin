#!/usr/bin/env python
"""
Verify Django model relationships before making changes
This script helps identify the correct relationship names
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from apps.facilities.models import Facility, FacilityCoordinate, FacilityService, FacilityGBVCategory
from django.db import models

def get_relationship_info(model_class):
    """Get all relationship information for a model"""
    relationships = []
    
    for field in model_class._meta.get_fields():
        if isinstance(field, (models.ForeignKey, models.OneToOneField, models.ManyToManyField)):
            rel_info = {
                'field_name': field.name,
                'related_model': field.related_model.__name__ if field.related_model else None,
                'related_name': getattr(field, 'related_name', None),
                'accessor_name': field.get_accessor_name() if hasattr(field, 'get_accessor_name') else None,
            }
            relationships.append(rel_info)
    
    # Get reverse relationships
    for rel in model_class._meta.related_objects:
        rel_info = {
            'field_name': rel.get_accessor_name(),
            'related_model': rel.related_model.__name__,
            'related_name': None,
            'accessor_name': rel.get_accessor_name(),
            'is_reverse': True,
        }
        relationships.append(rel_info)
    
    return relationships

def main():
    print("=" * 80)
    print("Django Model Relationship Verification")
    print("=" * 80)
    print()
    
    # Verify Facility model relationships
    print("Facility Model Relationships:")
    print("-" * 80)
    facility_rels = get_relationship_info(Facility)
    for rel in facility_rels:
        print(f"  Field: {rel['field_name']}")
        print(f"    Related Model: {rel['related_model']}")
        print(f"    Related Name: {rel['related_name']}")
        print(f"    Accessor Name: {rel['accessor_name']}")
        print(f"    Is Reverse: {rel.get('is_reverse', False)}")
        print()
    
    # Check specific relationships we need
    print("=" * 80)
    print("Key Relationships for API Fixes:")
    print("-" * 80)
    
    # Check FacilityCoordinate reverse relation
    coord_rel = None
    for rel in facility_rels:
        if 'coordinate' in rel['field_name'].lower():
            coord_rel = rel
            break
    
    if coord_rel:
        print(f"✓ FacilityCoordinate relationship found: {coord_rel['accessor_name']}")
    else:
        print("✗ FacilityCoordinate relationship NOT found")
    
    # Check FacilityService reverse relation
    service_rel = None
    for rel in facility_rels:
        if 'service' in rel['field_name'].lower() and 'set' in rel['field_name'].lower():
            service_rel = rel
            break
    
    if service_rel:
        print(f"✓ FacilityService relationship found: {service_rel['accessor_name']}")
    else:
        print("✗ FacilityService relationship NOT found")
    
    # Check FacilityGBVCategory reverse relation
    gbv_rel = None
    for rel in facility_rels:
        if 'gbv' in rel['field_name'].lower() or 'category' in rel['field_name'].lower():
            gbv_rel = rel
            break
    
    if gbv_rel:
        print(f"✓ FacilityGBVCategory relationship found: {gbv_rel['accessor_name']}")
    else:
        print("✗ FacilityGBVCategory relationship NOT found")
    
    print()
    print("=" * 80)
    print("Recommendations:")
    print("-" * 80)
    
    if coord_rel:
        print(f"Use: '{coord_rel['accessor_name']}' for FacilityCoordinate")
    else:
        print("Use: 'facilitycoordinate_set' (default Django reverse relation)")
    
    if service_rel:
        print(f"Use: '{service_rel['accessor_name']}' for FacilityService")
    else:
        print("Use: 'facilityservice_set' (default Django reverse relation)")
    
    if gbv_rel:
        print(f"Use: '{gbv_rel['accessor_name']}' for FacilityGBVCategory")
    else:
        print("Use: 'facilitygbvcategory_set' (default Django reverse relation)")
    
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()



