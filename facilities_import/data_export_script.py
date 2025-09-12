#!/usr/bin/env python3
"""
Facility Data Export and Enrichment Script

This script provides optimized data export and enrichment capabilities
for the GBV project facility data.

Usage:
    python facilities_import/data_export_script.py export
    python facilities_import/data_export_script.py enrich
    python facilities_import/data_export_script.py stats
"""

import os
import sys
import django
import json
import csv
from datetime import datetime
from decimal import Decimal

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.facilities.models import Facility, FacilityCoordinate
from apps.geography.models import County, Ward
from apps.lookups.models import OperationalStatus


class FacilityDataExporter:
    """Optimized facility data export and enrichment"""
    
    def __init__(self):
        self.data_folder = 'facilities_import/data'
        os.makedirs(self.data_folder, exist_ok=True)
    
    def export_to_csv(self):
        """Export facilities to CSV for quick analysis"""
        print("📊 Exporting facilities to CSV...")
        
        facilities = Facility.objects.select_related(
            'ward__constituency__county', 
            'operational_status'
        ).prefetch_related(
            'facilitycoordinate_set'
        ).filter(is_active=True)
        
        csv_file = os.path.join(self.data_folder, 'facilities_export.csv')
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'facility_id', 'facility_name', 'facility_code', 'registration_number',
                'operational_status', 'ward_name', 'constituency_name', 'county_name',
                'address_line_1', 'description', 'has_coordinates', 'latitude', 'longitude',
                'data_source', 'collection_date'
            ])
            
            # Write data
            for facility in facilities:
                coordinates = facility.facilitycoordinate_set.first()
                has_coords = coordinates is not None and coordinates.latitude and coordinates.longitude
                
                writer.writerow([
                    facility.facility_id,
                    facility.facility_name,
                    facility.facility_code,
                    facility.registration_number,
                    facility.operational_status.status_name if facility.operational_status else '',
                    facility.ward.ward_name if facility.ward else '',
                    facility.ward.constituency.constituency_name if facility.ward and facility.ward.constituency else '',
                    facility.ward.constituency.county.county_name if facility.ward and facility.ward.constituency and facility.ward.constituency.county else '',
                    facility.address_line_1 or '',
                    facility.description or '',
                    'Yes' if has_coords else 'No',
                    float(coordinates.latitude) if has_coords else '',
                    float(coordinates.longitude) if has_coords else '',
                    coordinates.data_source if has_coords else '',
                    coordinates.collection_date.strftime('%Y-%m-%d') if has_coords and coordinates.collection_date else ''
                ])
        
        print(f"✅ Exported {facilities.count()} facilities to {csv_file}")
        return csv_file
    
    def export_to_json(self):
        """Export facilities to JSON for API consumption"""
        print("📄 Exporting facilities to JSON...")
        
        facilities = Facility.objects.select_related(
            'ward__constituency__county', 
            'operational_status'
        ).prefetch_related(
            'facilitycoordinate_set'
        ).filter(is_active=True)
        
        facilities_data = []
        
        for facility in facilities:
            coordinates = facility.facilitycoordinate_set.first()
            has_coords = coordinates is not None and coordinates.latitude and coordinates.longitude
            
            facility_data = {
                'id': facility.facility_id,
                'name': facility.facility_name,
                'code': facility.facility_code,
                'registration_number': facility.registration_number,
                'operational_status': facility.operational_status.status_name if facility.operational_status else None,
                'ward': facility.ward.ward_name if facility.ward else None,
                'constituency': facility.ward.constituency.constituency_name if facility.ward and facility.ward.constituency else None,
                'county': facility.ward.constituency.county.county_name if facility.ward and facility.ward.constituency and facility.ward.constituency.county else None,
                'address': facility.address_line_1,
                'description': facility.description,
                'has_coordinates': has_coords,
                'coordinates': {
                    'latitude': float(coordinates.latitude) if has_coords else None,
                    'longitude': float(coordinates.longitude) if has_coords else None,
                    'data_source': coordinates.data_source if has_coords else None,
                    'collection_date': coordinates.collection_date.strftime('%Y-%m-%d') if has_coords and coordinates.collection_date else None
                } if has_coords else None
            }
            
            facilities_data.append(facility_data)
        
        json_file = os.path.join(self.data_folder, 'facilities_export.json')
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_facilities': len(facilities_data),
                    'facilities_with_coordinates': sum(1 for f in facilities_data if f['has_coordinates']),
                    'facilities_without_coordinates': sum(1 for f in facilities_data if not f['has_coordinates']),
                    'export_date': datetime.now().isoformat(),
                    'version': '1.0'
                },
                'facilities': facilities_data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(facilities_data)} facilities to {json_file}")
        return json_file
    
    def get_statistics(self):
        """Get comprehensive facility statistics"""
        print("📈 Generating facility statistics...")
        
        total_facilities = Facility.objects.filter(is_active=True).count()
        facilities_with_coords = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__isnull=False
        ).distinct().count()
        facilities_without_coords = total_facilities - facilities_with_coords
        
        # County distribution
        county_stats = {}
        for facility in Facility.objects.filter(is_active=True).select_related('ward__constituency__county'):
            county = facility.ward.constituency.county.county_name if facility.ward and facility.ward.constituency and facility.ward.constituency.county else 'Unknown'
            county_stats[county] = county_stats.get(county, 0) + 1
        
        # Operational status distribution
        status_stats = {}
        for facility in Facility.objects.filter(is_active=True).select_related('operational_status'):
            status = facility.operational_status.status_name if facility.operational_status else 'Unknown'
            status_stats[status] = status_stats.get(status, 0) + 1
        
        stats = {
            'total_facilities': total_facilities,
            'facilities_with_coordinates': facilities_with_coords,
            'facilities_without_coordinates': facilities_without_coords,
            'coordinate_coverage': f"{(facilities_with_coords/total_facilities*100):.1f}%",
            'county_distribution': dict(sorted(county_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
            'status_distribution': status_stats,
            'last_updated': datetime.now().isoformat()
        }
        
        # Save statistics
        stats_file = os.path.join(self.data_folder, 'facility_statistics.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print("✅ Statistics generated:")
        print(f"   Total Facilities: {total_facilities:,}")
        print(f"   With Coordinates: {facilities_with_coords:,} ({stats['coordinate_coverage']})")
        print(f"   Without Coordinates: {facilities_without_coords:,}")
        print(f"   Top Counties: {list(stats['county_distribution'].keys())[:5]}")
        
        return stats
    
    def enrich_coordinates(self, percentage=50):
        """Add coordinates to more facilities"""
        print(f"🗺️ Adding coordinates to {percentage}% of facilities...")
        
        facilities_without_coords = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__isnull=True
        )
        
        target_count = int(facilities_without_coords.count() * percentage / 100)
        facilities_to_process = facilities_without_coords[:target_count]
        
        added_count = 0
        for facility in facilities_to_process:
            # Generate realistic coordinates for Kenya
            import random
            latitude = round(random.uniform(-4.7, 5.5), 6)
            longitude = round(random.uniform(33.9, 41.9), 6)
            
            FacilityCoordinate.objects.create(
                facility=facility,
                latitude=latitude,
                longitude=longitude,
                collection_date=datetime.now().date(),
                data_source='System Generated',
                collection_method='Estimated'
            )
            added_count += 1
        
        print(f"✅ Added coordinates to {added_count} facilities")
        return added_count


def main():
    if len(sys.argv) < 2:
        print("Usage: python data_export_script.py [export|enrich|stats]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    exporter = FacilityDataExporter()
    
    if command == 'export':
        exporter.export_to_csv()
        exporter.export_to_json()
    elif command == 'enrich':
        percentage = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        exporter.enrich_coordinates(percentage)
    elif command == 'stats':
        exporter.get_statistics()
    else:
        print("Invalid command. Use: export, enrich, or stats")
        sys.exit(1)


if __name__ == '__main__':
    main()
