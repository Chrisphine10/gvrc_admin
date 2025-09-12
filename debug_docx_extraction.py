#!/usr/bin/env python3
"""
Debug script to test DOCX extraction
"""

import sys
import os
sys.path.append('.')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.postgres')
django.setup()

from apps.data_architecture.data_source_integration import DOCXDataSourceAdapter

def test_docx_extraction():
    """Test DOCX extraction directly"""
    file_path = "facilities_import/data/raw/GBV Support Organizations, Legal, Psychological and Child Protection.docx"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    config = {
        'file_path': file_path,
        'encoding': 'utf-8'
    }
    
    adapter = DOCXDataSourceAdapter(config)
    
    print("Testing DOCX connection...")
    if adapter.connect():
        print("✅ DOCX connection successful")
    else:
        print("❌ DOCX connection failed")
        return
    
    print("\nTesting DOCX extraction...")
    data = adapter.extract_data(limit=10)  # Extract first 10 records
    
    print(f"Extracted {len(data)} records")
    
    for i, record in enumerate(data):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    test_docx_extraction()

