# Kenya Geography Data Management

This directory contains Django management commands to populate your database with comprehensive geographic data for all 47 counties in Kenya, including constituencies and wards.

## Available Commands

### 1. `populate_geography` (Original)
- **Purpose**: Populates geography tables with sample data for major counties
- **Coverage**: Limited to Nairobi, Mombasa, Kisumu, Nakuru, and Eldoret
- **Usage**: `python manage.py populate_geography`

### 2. `populate_kenya_geography` (New - Comprehensive)
- **Purpose**: Populates geography tables with complete data for all 47 counties in Kenya
- **Coverage**: All 47 counties with their constituencies
- **Usage**: `python manage.py populate_kenya_geography`

## What's Included

### Counties (47 total)
All 47 counties in Kenya are included with their official codes:
- Mombasa (001) to Nairobi (047)
- Complete alphabetical and numerical coverage

### Constituencies (290+ total)
All constituencies across all counties, including:
- Nairobi: 17 constituencies
- Mombasa: 6 constituencies
- Kiambu: 11 constituencies
- And many more...

### Wards (Sample data provided)
Currently includes sample wards for:
- Complete Nairobi County wards
- Complete Mombasa County wards
- Sample wards for other major counties

## How to Use

### Basic Population
```bash
# Populate with all counties and constituencies
python manage.py populate_kenya_geography

# Or use the original sample data
python manage.py populate_geography
```

### Database Verification
After running the command, you can verify the data:
```python
from apps.geography.models import County, Constituency, Ward

# Check counts
print(f"Counties: {County.objects.count()}")
print(f"Constituencies: {Constituency.objects.count()}")
print(f"Wards: {Ward.objects.count()}")

# List all counties
for county in County.objects.all():
    print(f"{county.county_code}: {county.county_name}")
```

## Expanding Ward Data

The current implementation includes sample ward data. To add complete ward data for all constituencies:

### Option 1: Expand the Data File
Edit `kenya_ward_data.py` and add more ward entries following this format:
```python
{'name': 'Ward Name', 'code': 'CountyCodeConstituencyCodeWardCode', 'constituency': 'Constituency Name'},
```

### Option 2: Create a Complete Data File
You can create a comprehensive JSON or CSV file with all ward data and modify the command to import from it.

### Option 3: Use External Data Sources
- Kenya National Bureau of Statistics (KNBS)
- Independent Electoral and Boundaries Commission (IEBC)
- Open data portals

## Data Structure

### County Codes
- 001: Mombasa
- 002: Kwale
- 003: Kilifi
- ...
- 047: Nairobi

### Constituency Codes
- Format: `CountyCode + ConstituencyNumber`
- Example: `001001` = Mombasa County, Constituency 1 (Changamwe)

### Ward Codes
- Format: `CountyCode + ConstituencyCode + WardNumber`
- Example: `001001001` = Mombasa County, Changamwe Constituency, Ward 1 (Port Reitz)

## Important Notes

1. **Data Accuracy**: This data represents the administrative boundaries as of the 2010 Constitution implementation
2. **Updates**: Administrative boundaries may change; verify with official sources
3. **Performance**: For large datasets, consider running during off-peak hours
4. **Backup**: Always backup your database before running population commands

## Troubleshooting

### Common Issues

1. **Import Error**: If you get import errors, ensure the `kenya_ward_data.py` file is in the same directory
2. **Duplicate Data**: The commands use `get_or_create` to prevent duplicates
3. **Memory Issues**: For very large datasets, consider processing in batches

### Verification Commands
```bash
# Check if tables exist
python manage.py dbshell
.tables

# Check data integrity
python manage.py shell
from apps.geography.models import County
County.objects.filter(county_code__isnull=True).count()
```

## Contributing

To add more comprehensive data:
1. Update `kenya_ward_data.py` with additional ward information
2. Test the command with a small dataset first
3. Verify data accuracy against official sources
4. Submit updates for review

## Data Sources

- Kenya National Bureau of Statistics
- Independent Electoral and Boundaries Commission
- County Government websites
- Official government gazettes

## License

This data is provided for educational and development purposes. Please verify accuracy with official sources before using in production systems.
