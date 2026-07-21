#!/usr/bin/env python3
"""
Helper script to expand ward data for all constituencies in Kenya.
This script provides a template and structure for adding complete ward data.
"""

# Template for ward data structure
WARD_TEMPLATE = {
    'name': 'Ward Name',
    'code': 'CountyCodeConstituencyCodeWardNumber',
    'constituency': 'Constituency Name'
}

# Example of how to structure ward data for a constituency
EXAMPLE_WARDS = {
    'Westlands': [
        {'name': 'Parklands/Highridge', 'code': '047001001'},
        {'name': 'Karura', 'code': '047001002'},
        {'name': 'Kangemi', 'code': '047001003'},
        {'name': 'Mountain View', 'code': '047001004'},
    ],
    'Dagoretti North': [
        {'name': 'Kilimani', 'code': '047002001'},
        {'name': 'Mutu-ini', 'code': '047002002'},
        {'name': 'Ngando', 'code': '047002003'},
        {'name': 'Riruta', 'code': '047002004'},
        {'name': 'Uthiru/Ruthimitu', 'code': '047002005'},
        {'name': 'Waithaka', 'code': '047002006'},
    ]
}

def generate_ward_structure():
    """
    Generate a structured template for adding ward data.
    This helps organize the data by constituency.
    """
    print("=== Kenya Ward Data Structure Template ===\n")
    
    print("To add complete ward data, follow this structure:")
    print("1. Group wards by constituency")
    print("2. Use consistent naming conventions")
    print("3. Follow the coding system: CountyCode + ConstituencyCode + WardNumber\n")
    
    print("Example structure:")
    for constituency, wards in EXAMPLE_WARDS.items():
        print(f"\n{constituency} Constituency:")
        for ward in wards:
            print(f"  - {ward['name']} ({ward['code']})")
    
    print("\n=== Coding System ===")
    print("County Code: 001 (Mombasa) to 047 (Nairobi)")
    print("Constituency Code: Sequential number within county")
    print("Ward Code: Sequential number within constituency")
    print("Example: 047001001 = Nairobi County, Westlands Constituency, Ward 1")

def get_constituency_ward_counts():
    """
    Display the expected number of wards per constituency.
    This helps in planning the data expansion.
    """
    print("\n=== Expected Ward Counts by County ===")
    
    # Sample data showing typical ward counts
    county_ward_counts = {
        'Nairobi': 85,  # 17 constituencies × 5 wards average
        'Mombasa': 30,  # 6 constituencies × 5 wards average
        'Kiambu': 55,   # 11 constituencies × 5 wards average
        'Nakuru': 55,   # 11 constituencies × 5 wards average
        'Kisumu': 35,   # 7 constituencies × 5 wards average
        'Kakamega': 60, # 12 constituencies × 5 wards average
    }
    
    for county, count in county_ward_counts.items():
        print(f"{county}: ~{count} wards")
    
    print(f"\nTotal estimated wards in Kenya: ~1,450")
    print("Note: Actual counts may vary by constituency")

def export_template():
    """
    Export a template file for adding ward data.
    """
    template_content = '''# Template for adding complete ward data
# Add wards for each constituency following this format

COMPLETE_WARDS_DATA = [
    # Example: Nairobi County - Westlands Constituency
    {'name': 'Parklands/Highridge', 'code': '047001001', 'constituency': 'Westlands'},
    {'name': 'Karura', 'code': '047001002', 'constituency': 'Westlands'},
    {'name': 'Kangemi', 'code': '047001003', 'constituency': 'Westlands'},
    {'name': 'Mountain View', 'code': '047001004', 'constituency': 'Westlands'},
    
    # Example: Nairobi County - Dagoretti North Constituency
    {'name': 'Kilimani', 'code': '047002001', 'constituency': 'Dagoretti North'},
    {'name': 'Mutu-ini', 'code': '047002002', 'constituency': 'Dagoretti North'},
    {'name': 'Ngando', 'code': '047002003', 'constituency': 'Dagoretti North'},
    {'name': 'Riruta', 'code': '047002004', 'constituency': 'Dagoretti North'},
    {'name': 'Uthiru/Ruthimitu', 'code': '047002005', 'constituency': 'Dagoretti North'},
    {'name': 'Waithaka', 'code': '047002006', 'constituency': 'Dagoretti North'},
    
    # Add more constituencies here...
    # Format: {'name': 'Ward Name', 'code': 'CountyCodeConstituencyCodeWardNumber', 'constituency': 'Constituency Name'},
]

# Instructions:
# 1. Replace 'CountyCode' with actual county code (001-047)
# 2. Replace 'ConstituencyCode' with actual constituency number
# 3. Replace 'WardNumber' with sequential ward number
# 4. Ensure constituency name matches exactly with the constituency data
# 5. Verify ward names against official sources
'''
    
    with open('ward_data_template.py', 'w') as f:
        f.write(template_content)
    
    print("\nTemplate file 'ward_data_template.py' created successfully!")
    print("Use this template to add complete ward data for all constituencies.")

if __name__ == '__main__':
    generate_ward_structure()
    get_constituency_ward_counts()
    export_template()
    
    print("\n=== Next Steps ===")
    print("1. Use the template to add ward data for each constituency")
    print("2. Verify ward names against official sources")
    print("3. Test the data with a small subset first")
    print("4. Run the populate command to verify data integrity")
    print("5. Consider using external data sources for complete coverage")
