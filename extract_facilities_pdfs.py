#!/usr/bin/env python3
"""
Extract facilities data from PDFs following data architecture
"""

import sys
import os
sys.path.append('.')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.postgres')
django.setup()

from apps.data_architecture.data_source_integration import integration_manager
from apps.data_architecture.enhanced_etl_pipeline import DataArchitectureManager
import json

def extract_all_pdfs():
    """Extract data from all PDFs in facilities raw data directory"""
    
    pdf_directory = "facilities_import/data/raw/"
    pdf_files = [
        "All_Facilities_Facilities_licensed_by_KMPDC_for_year_2024_as_at_7th_June_2024_at_5.00pm.pdf",
        "LIST_OF_LICENSED_HEALTH_CARE_FACILITIES_BY_KMPDC-1.pdf", 
        "LIST_OF_LICENSED_HEALTH_CARE_FACILITIES_BY_KMPDC.pdf",
        "National_Shelters_Network_a5a50b19.pdf"
    ]
    
    data_manager = DataArchitectureManager()
    all_extracted_data = []
    
    for pdf_file in pdf_files:
        file_path = os.path.join(pdf_directory, pdf_file)
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"\n📄 Processing: {pdf_file}")
        
        # Create data source
        source_name = f"pdf_{pdf_file.replace('.pdf', '').replace(' ', '_').lower()}"
        config = {'file_path': file_path, 'encoding': 'utf-8'}
        
        try:
            data_source = integration_manager.create_data_source(
                name=source_name,
                source_type='pdf',
                config=config
            )
            
            # Extract and process data through ETL pipeline
            result = integration_manager.ingest_from_source(data_source)
            
            print(f"✅ Extracted {result['records']} records")
            print(f"   Status: {result['status']}")
            
            if result.get('validation_results'):
                validation = result['validation_results']
                print(f"   Quality Score: {validation.get('quality_score', 'N/A')}")
                print(f"   Valid Records: {validation.get('valid_count', 'N/A')}")
                
            all_extracted_data.append({
                'source': pdf_file,
                'result': result
            })
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {str(e)}")
    
    # Save extraction summary
    summary_path = "facilities_import/data/exports/pdf_extraction_summary.json"
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    
    with open(summary_path, 'w') as f:
        json.dump(all_extracted_data, f, indent=2, default=str)
    
    print(f"\n📊 Summary saved to: {summary_path}")
    print(f"Total PDFs processed: {len(all_extracted_data)}")

if __name__ == "__main__":
    extract_all_pdfs()