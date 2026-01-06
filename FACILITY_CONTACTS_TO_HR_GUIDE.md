# Facility Contacts to Human Resources Registration Guide

## Overview

This guide explains how to get facility contacts and register them in the Human Resources system.

## Current Situation

- **Total Facility Contacts**: 71 active contacts
- **Contact Types**: Currently all are "Phone" type
- **HR System**: Currently filters for specific HR contact types (Manager, Director, etc.)
- **Issue**: Facility contacts are not showing in HR because they don't match HR-specific types

## Data Extraction

### Script Created
- **File**: `scripts/extract_facility_contacts_for_hr.py`
- **Purpose**: Extracts all facility contacts and formats them for HR registration
- **Output**: JSON file with all contact data

### Run the Script
```bash
cd /home/ubuntu/gvrc_admin
source env/bin/activate
python scripts/extract_facility_contacts_for_hr.py
```

## Data Structure

Each contact includes:
- Contact details (type, value, person name)
- Facility information (name, code, registration number)
- Location (ward, constituency, county)
- Facility status (operational status, active status)
- Services offered by facility
- Metadata (created/updated dates, primary flag)

## Solution Options

### Option 1: Include All Contact Types in HR View (Recommended)

**File to Modify**: `apps/home/views.py` (line 328-333)

**Current Code**:
```python
hr_contact_types = ContactType.objects.filter(
    type_name__in=[
        'Primary Contact', 'Manager', 'Director', 'Supervisor', 
        'Staff', 'Emergency Contact', 'Administrative Contact'
    ]
)
```

**Change To** (include ALL contact types):
```python
# Include ALL contact types, not just HR-specific ones
hr_contact_types = ContactType.objects.all()
```

**OR** (include Phone and Email as well):
```python
hr_contact_types = ContactType.objects.filter(
    Q(type_name__in=[
        'Primary Contact', 'Manager', 'Director', 'Supervisor', 
        'Staff', 'Emergency Contact', 'Administrative Contact'
    ]) |
    Q(type_name__in=['Phone', 'Email'])  # Add common contact types
)
```

### Option 2: Remove Contact Type Filter Entirely

**File to Modify**: `apps/home/views.py` (line 336-338)

**Current Code**:
```python
hr_contacts = FacilityContact.objects.filter(
    is_active=True,
    contact_type__in=hr_contact_types
)
```

**Change To**:
```python
# Show ALL facility contacts, regardless of type
hr_contacts = FacilityContact.objects.filter(
    is_active=True
)
```

### Option 3: Add Contact Types to Database

If you want to categorize facility contacts as HR contacts:

1. **Update Contact Types**: Add HR-related types or update existing ones
2. **Update Facility Contacts**: Assign appropriate contact types to existing contacts
3. **Keep Current Filter**: The HR view will automatically include them

## Data Export Format

The script exports data in this format:

```json
[
  {
    "contact_id": 8753,
    "facility_id": 53697,
    "facility_name": "Buruburu Police Station",
    "contact_type": "Phone",
    "contact_value": "020-786878",
    "contact_person_name": "",
    "is_primary": true,
    "ward": "Nairobi Constituency 1 Ward 111",
    "constituency": "Nairobi Constituency 1",
    "county": "Nairobi",
    "services": ["Emergency Services"],
    "operational_status": "Operational",
    "created_at": "2025-09-12T08:47:24.185862+00:00"
  }
]
```

## Statistics

### Current Data
- **Total Contacts**: 71
- **Contact Types**: Phone (71)
- **Facilities with Contacts**: 71
- **Counties**: All in Nairobi
- **Primary Contacts**: 71 (all marked as primary)

### After Including All Contacts in HR
- All 71 facility contacts will appear in Human Resources
- Can be filtered by type, facility, location
- Search functionality will work across all contacts

## Implementation Steps

1. **Extract Data** (Already done):
   ```bash
   python scripts/extract_facility_contacts_for_hr.py
   ```

2. **Review Data**:
   - Check the generated JSON file
   - Verify contact information is correct

3. **Update HR View** (Choose one option above):
   - Modify `apps/home/views.py`
   - Update the contact type filter
   - Test the human resources page

4. **Verify Results**:
   - Visit `/human-resources/` page
   - Confirm all facility contacts are visible
   - Test filtering and search functionality

## Notes

- **No Data Loss**: All contacts remain in the facility_contacts table
- **No Duplication**: Contacts are displayed, not duplicated
- **Backward Compatible**: Existing HR functionality remains intact
- **Search Works**: All contacts are searchable by facility name, location, contact value

## Files Created

1. **`scripts/extract_facility_contacts_for_hr.py`** - Data extraction script
2. **`facility_contacts_for_hr_YYYYMMDD_HHMMSS.json`** - Exported contact data
3. **`FACILITY_CONTACTS_TO_HR_GUIDE.md`** - This guide

## Next Steps

1. Review the extracted data
2. Choose implementation option (Option 1 recommended)
3. Update the HR view to include all contact types
4. Test the human resources page
5. Verify all contacts are visible and searchable

---

**Date**: 2024-12-28  
**Status**: ✅ Data Ready for HR Registration  
**Total Contacts**: 71



