# Mobile Endpoints - Ready for Testing

## ✅ Endpoints Created and Fixed

### 1. Facility Coordinates for Map
**Endpoint**: `GET /mobile/facilities/map/`

**Status**: ✅ WORKING

**Query Parameters**:
- `device_id` (required) - Device ID from mobile session
- `ne_lat`, `ne_lng`, `sw_lat`, `sw_lng` (optional) - Viewport coordinates
- `zoom` (optional) - Map zoom level (1-20, default: 10)
- `county`, `constituency`, `ward` (optional) - Location filters

**Response**:
```json
{
  "facilities": [
    {
      "facility_id": 1,
      "facility_name": "Facility Name",
      "coordinates": {
        "latitude": -1.2921,
        "longitude": 36.8219
      }
    }
  ],
  "count": 5000
}
```

**Test Result**: ✅ Returns 5000 facilities successfully

### 2. Resources Endpoint
**Endpoint**: `GET /mobile/resources/list/`

**Status**: ✅ CREATED

**Query Parameters**:
- `device_id` (required) - Device ID from mobile session
- `resource_type` (optional) - 'documents', 'music', or 'all' (default: 'all')
- `page` (optional) - Page number (default: 1)
- `page_size` (optional) - Items per page (default: 50, max: 200)

**Response**:
```json
{
  "documents": {
    "count": 25,
    "results": [...]
  },
  "music": {
    "count": 10,
    "results": [...]
  },
  "total_count": 35
}
```

## Mobile Testing Instructions

### Step 1: Create Mobile Session
```bash
curl -X POST "https://hodi.co.ke/mobile/sessions/create/" \
  -H "Content-Type: application/json" \
  -d '{"device_id": "your_mobile_device_id"}'
```

### Step 2: Test Map Endpoint
```bash
curl "https://hodi.co.ke/mobile/facilities/map/?device_id=your_mobile_device_id"
```

### Step 3: Test Resources Endpoint
```bash
curl "https://hodi.co.ke/mobile/resources/list/?device_id=your_mobile_device_id"
```

### Step 4: Test with Viewport (Map)
```bash
curl "https://hodi.co.ke/mobile/facilities/map/?device_id=your_mobile_device_id&ne_lat=-1.2&ne_lng=36.9&sw_lat=-1.3&sw_lng=36.8&zoom=12"
```

## Mobile App Integration

Both endpoints are ready for mobile app integration. See `MOBILE_ENDPOINTS_TEST.md` for detailed integration examples.

## Notes

- Both endpoints require valid mobile session (device_id)
- Map endpoint optimized for performance with viewport filtering
- Resources endpoint provides consolidated access to documents and music
- All endpoints include cache headers for mobile optimization

