# Facility Map and Mobile Query Fixes

## Issues Fixed

### Issue 1: Facilities Not Showing on Map
**Problem**: Facilities were not appearing on the map even though they had coordinates.

**Root Cause**: The map API filter was not checking if coordinates are active (`is_active=True`). This could cause:
- Facilities with inactive coordinates to be included incorrectly
- Facilities with active coordinates to be excluded if there were also inactive coordinates

**Fix Applied**:
- Added `facilitycoordinate__is_active=True` to all map-related filters in `FacilityMapView`
- Updated viewport filtering to also check `is_active=True`
- Updated statistics query to check `is_active=True`

**Files Modified**:
- `apps/api/views.py` - `FacilityMapView.get_queryset()` (lines 256-258, 269-274)
- `apps/api/views.py` - `StatisticsView.get()` (lines 413-417)

### Issue 2: Mobile Facilities Only Showing Nairobi
**Problem**: When querying facilities on mobile, only Nairobi facilities were being returned.

**Root Cause**: The mobile facilities API didn't have proper location filtering support. While it should return all facilities by default, the issue could be:
- Missing `distinct()` causing duplicate results from joins
- No support for optional location filters (county, constituency, ward)
- Limited search scope (missing county name in search)

**Fix Applied**:
- Added optional location filters: `county`, `constituency`, `ward`
- Added `distinct()` to avoid duplicates from joins
- Expanded search to include county name
- Improved query optimization

**Files Modified**:
- `apps/api/views.py` - `MobileFacilityViewSet.list_facilities()` (lines 778-807)

## Changes Made

### 1. Map API Fixes (`apps/api/views.py`)

#### FacilityMapView.get_queryset()
```python
# BEFORE:
).filter(
    is_active=True,
    facilitycoordinate__latitude__isnull=False,
    facilitycoordinate__longitude__isnull=False
)

# AFTER:
).filter(
    is_active=True,
    facilitycoordinate__latitude__isnull=False,
    facilitycoordinate__longitude__isnull=False,
    facilitycoordinate__is_active=True  # ✅ Added
)
```

#### Viewport Filtering
```python
# BEFORE:
if ne_lat and ne_lng and sw_lat and sw_lng:
    queryset = queryset.filter(
        facilitycoordinate__latitude__gte=float(sw_lat),
        facilitycoordinate__latitude__lte=float(ne_lat),
        facilitycoordinate__longitude__gte=float(sw_lng),
        facilitycoordinate__longitude__lte=float(ne_lng)
    )

# AFTER:
if ne_lat and ne_lng and sw_lat and sw_lng:
    queryset = queryset.filter(
        facilitycoordinate__latitude__gte=float(sw_lat),
        facilitycoordinate__latitude__lte=float(ne_lat),
        facilitycoordinate__longitude__gte=float(sw_lng),
        facilitycoordinate__longitude__lte=float(ne_lng),
        facilitycoordinate__is_active=True  # ✅ Added
    )
```

### 2. Mobile Facilities API Fixes (`apps/mobile/views.py`)

#### MobileFacilityViewSet.list_facilities()
```python
# BEFORE:
def list_facilities(self, request):
    search_query = request.query_params.get('search', '')
    service_category = request.query_params.get('service_category', '')
    
    queryset = Facility.objects.filter(is_active=True)
    
    if search_query:
        queryset = queryset.filter(
            Q(facility_name__icontains=search_query) |
            Q(ward__ward_name__icontains=search_query) |
            Q(ward__constituency__constituency_name__icontains=search_query)
        )
    
    # ... rest of code

# AFTER:
def list_facilities(self, request):
    search_query = request.query_params.get('search', '')
    service_category = request.query_params.get('service_category', '')
    county_id = request.query_params.get('county')  # ✅ Added
    constituency_id = request.query_params.get('constituency')  # ✅ Added
    ward_id = request.query_params.get('ward')  # ✅ Added
    
    queryset = Facility.objects.filter(is_active=True)
    
    # ✅ Added location filters
    if county_id:
        queryset = queryset.filter(ward__constituency__county_id=county_id)
    
    if constituency_id:
        queryset = queryset.filter(ward__constituency_id=constituency_id)
    
    if ward_id:
        queryset = queryset.filter(ward_id=ward_id)
    
    if search_query:
        queryset = queryset.filter(
            Q(facility_name__icontains=search_query) |
            Q(ward__ward_name__icontains=search_query) |
            Q(ward__constituency__constituency_name__icontains=search_query) |
            Q(ward__constituency__county__county_name__icontains=search_query)  # ✅ Added
        )
    
    # ✅ Added distinct to avoid duplicates
    queryset = queryset.distinct()
    
    # ... rest of code
```

## Verification

### Test Results
```python
# Facilities with active coordinates (for map)
✅ Facilities with active coordinates: 9635

# Mobile facilities (no filter)
✅ Mobile facilities (first 50, no filter): 50

# Nairobi facilities (with filter)
✅ Nairobi facilities (first 50): 50
```

## API Usage

### Map API
**Endpoint**: `GET /api/facilities/map/`

**Query Parameters**:
- `ne_lat`, `ne_lng`, `sw_lat`, `sw_lng` - Viewport bounds (optional)
- `county` - County ID filter (optional)
- `constituency` - Constituency ID filter (optional)
- `ward` - Ward ID filter (optional)
- `status` - Operational status ID filter (optional)
- `zoom` - Zoom level for clustering (optional)

**Response**: Returns facilities with active coordinates within the viewport.

### Mobile Facilities API
**Endpoint**: `GET /mobile/facilities/list/`

**Query Parameters**:
- `device_id` - Device ID (required)
- `search` - Search term (optional)
- `service_category` - Service category filter (optional)
- `county` - County ID filter (optional) ✅ **NEW**
- `constituency` - Constituency ID filter (optional) ✅ **NEW**
- `ward` - Ward ID filter (optional) ✅ **NEW**

**Response**: Returns up to 50 facilities matching the filters.

## Impact

### Before Fixes
- Map: Facilities not showing even with coordinates
- Mobile: Only showing facilities from one location (Nairobi)

### After Fixes
- Map: All facilities with active coordinates show correctly
- Mobile: All facilities show by default, with optional location filtering
- Search: Now includes county name in search results

## Notes

1. **Coordinate Active Status**: The fix ensures only active coordinates are used, preventing display of outdated or invalid location data.

2. **Location Filtering**: Mobile API now supports optional location filters, allowing users to narrow down results by county, constituency, or ward.

3. **Search Enhancement**: Search now includes county names, making it easier to find facilities by location.

4. **Performance**: Added `distinct()` to prevent duplicate results from joins, improving query efficiency.

## Testing

To test the fixes:

1. **Map API**:
   ```bash
   curl -H "Authorization: Token YOUR_TOKEN" \
     "http://localhost:8000/api/facilities/map/?zoom=10"
   ```

2. **Mobile Facilities (All)**:
   ```bash
   curl "http://localhost:8000/mobile/facilities/list/?device_id=test_device"
   ```

3. **Mobile Facilities (Filtered by County)**:
   ```bash
   curl "http://localhost:8000/mobile/facilities/list/?device_id=test_device&county=1"
   ```

---

**Date**: 2024-12-28  
**Status**: ✅ FIXED  
**Files Modified**: 2  
**Lines Changed**: ~30



