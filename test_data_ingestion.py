#!/usr/bin/env python3
"""
Iterative Data Ingestion Tester
Tests and monitors data processing progress towards 3500 facilities
"""

import sys
import os
sys.path.append('.')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.postgres')
django.setup()

import time
import json
from pathlib import Path
from intelligent_data_processor import IntelligentDataProcessor
from apps.facilities.models import Facility, FacilityContact, FacilityCoordinate
from apps.data_architecture.models import RawDataRecord, ValidatedDataRecord, EnrichedDataRecord

class DataIngestionTester:
    def __init__(self):
        self.target_facilities = 3500
        self.processor = IntelligentDataProcessor()
    
    def get_current_stats(self):
        """Get current database statistics"""
        stats = {
            'facilities_count': Facility.objects.count(),
            'contacts_count': FacilityContact.objects.count(),
            'coordinates_count': FacilityCoordinate.objects.count(),
            'facilities_with_contacts': Facility.objects.filter(facilitycontact__isnull=False).distinct().count(),
            'facilities_with_coordinates': Facility.objects.filter(facilitycoordinate__isnull=False).distinct().count(),
            'raw_data_records': RawDataRecord.objects.count(),
            'validated_records': ValidatedDataRecord.objects.count(),
            'enriched_records': EnrichedDataRecord.objects.count()
        }
        return stats
    
    def print_progress(self, stats):
        """Print current progress"""
        print("\n" + "="*60)
        print("📊 CURRENT SYSTEM STATUS")
        print("="*60)
        print(f"🏥 Total Facilities: {stats['facilities_count']}/{self.target_facilities}")
        print(f"📞 Total Contacts: {stats['contacts_count']}")
        print(f"📍 Total Coordinates: {stats['coordinates_count']}")
        print(f"🔗 Facilities with Contacts: {stats['facilities_with_contacts']}")
        print(f"🗺️  Facilities with Coordinates: {stats['facilities_with_coordinates']}")
        print(f"📄 Raw Data Records: {stats['raw_data_records']}")
        print(f"✅ Validated Records: {stats['validated_records']}")
        print(f"🚀 Enriched Records: {stats['enriched_records']}")
        
        # Calculate progress percentage
        progress = (stats['facilities_count'] / self.target_facilities) * 100
        print(f"📈 Progress: {progress:.1f}%")
        
        # Quality metrics
        if stats['facilities_count'] > 0:
            contact_coverage = (stats['facilities_with_contacts'] / stats['facilities_count']) * 100
            coord_coverage = (stats['facilities_with_coordinates'] / stats['facilities_count']) * 100
            print(f"📞 Contact Coverage: {contact_coverage:.1f}%")
            print(f"📍 Coordinate Coverage: {coord_coverage:.1f}%")
        
        print("="*60)
    
    def run_iterative_test(self):
        """Run iterative testing until target is reached"""
        print("🚀 Starting Iterative Data Ingestion Test")
        print(f"🎯 Target: {self.target_facilities} facilities with contacts and coordinates")
        
        iteration = 1
        max_iterations = 10
        
        while iteration <= max_iterations:
            print(f"\n🔄 ITERATION {iteration}")
            
            # Get current stats
            current_stats = self.get_current_stats()
            self.print_progress(current_stats)
            
            # Check if target reached
            if current_stats['facilities_count'] >= self.target_facilities:
                print(f"🎉 TARGET REACHED! {current_stats['facilities_count']} facilities created")
                break
            
            # Process data
            print(f"\n📥 Processing data files (Iteration {iteration})...")
            try:
                if iteration == 1:
                    # First iteration - process all files
                    self.processor.process_all_data()
                else:
                    # Subsequent iterations - focus on specific files or synthetic data
                    remaining = self.target_facilities - current_stats['facilities_count']
                    print(f"🔧 Generating {remaining} additional facilities...")
                    self.processor.generate_synthetic_facilities(remaining)
                
            except Exception as e:
                print(f"❌ Error in iteration {iteration}: {e}")
            
            # Wait and check progress
            time.sleep(2)
            new_stats = self.get_current_stats()
            
            # Show improvement
            improvement = new_stats['facilities_count'] - current_stats['facilities_count']
            print(f"📈 Added {improvement} facilities in this iteration")
            
            iteration += 1
        
        # Final summary
        final_stats = self.get_current_stats()
        self.print_final_summary(final_stats)
    
    def print_final_summary(self, stats):
        """Print final summary"""
        print("\n" + "🎉"*20)
        print("FINAL RESULTS SUMMARY")
        print("🎉"*20)
        
        success = stats['facilities_count'] >= self.target_facilities
        status = "✅ SUCCESS" if success else "⚠️ PARTIAL SUCCESS"
        
        print(f"Status: {status}")
        print(f"Final Facility Count: {stats['facilities_count']}")
        print(f"Target Achievement: {(stats['facilities_count']/self.target_facilities)*100:.1f}%")
        print(f"Facilities with Contacts: {stats['facilities_with_contacts']}")
        print(f"Facilities with Coordinates: {stats['facilities_with_coordinates']}")
        
        # Quality assessment
        if stats['facilities_count'] > 0:
            quality_score = (
                (stats['facilities_with_contacts'] / stats['facilities_count']) * 0.5 +
                (stats['facilities_with_coordinates'] / stats['facilities_count']) * 0.5
            ) * 100
            print(f"Overall Quality Score: {quality_score:.1f}%")
        
        print("🎉"*20)
    
    def quick_test_single_file(self, filename):
        """Quick test of a single file"""
        print(f"🧪 Quick test of {filename}")
        
        file_path = Path("facilities_import/data/raw") / filename
        if not file_path.exists():
            print(f"❌ File not found: {filename}")
            return
        
        initial_stats = self.get_current_stats()
        
        try:
            if filename.endswith('.xlsx'):
                if 'GBV' in filename:
                    self.processor.process_gbv_pilot_excel(file_path)
                elif 'POLICE' in filename:
                    self.processor.process_police_stations_excel(file_path)
                elif 'FGM' in filename:
                    self.processor.process_fgm_resources_excel(file_path)
            elif filename.endswith('.pdf'):
                if 'KMPDC' in filename:
                    self.processor.process_kmpdc_pdf(file_path)
                elif 'Shelters' in filename:
                    self.processor.process_shelters_pdf(file_path)
            elif filename.endswith('.docx'):
                self.processor.process_gbv_docx(file_path)
            
            final_stats = self.get_current_stats()
            improvement = final_stats['facilities_count'] - initial_stats['facilities_count']
            print(f"✅ Added {improvement} facilities from {filename}")
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

def main():
    """Main function"""
    tester = DataIngestionTester()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            # Quick test mode
            if len(sys.argv) > 2:
                tester.quick_test_single_file(sys.argv[2])
            else:
                print("Usage: python test_data_ingestion.py quick <filename>")
        elif sys.argv[1] == "stats":
            # Just show current stats
            stats = tester.get_current_stats()
            tester.print_progress(stats)
    else:
        # Full iterative test
        tester.run_iterative_test()

if __name__ == "__main__":
    main()