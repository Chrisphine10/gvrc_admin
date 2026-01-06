# Mobile Endpoints Testing Guide

## Endpoints Created/Fixed

### 1. Facility Coordinates for Map
**Endpoint**: `GET /mobile/facilities/map/`

**Description**: Get facilities with coordinates optimized for map display

**Query Parameters**:
- `device_id` (required) - Device ID from mobile session
- `ne_lat` (optional) - Northeast latitude for viewport filtering
- `ne_lng` (optional) - Northeast longitude for viewport filtering
- `sw_lat` (optional) - Southwest latitude for viewport filtering
- `sw_lng` (optional) - Southwest longitude for viewport filtering
- `zoom` (optional) - Map zoom level (1-20, default: 10)
- `county` (optional) - Filter by county ID
- `constituency` (optional) - Filter by constituency ID
- `ward` (optional) - Filter by ward ID

**Response Format**:
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
  "count": 150,
  "viewport": {
    "ne_lat": -1.2,
    "ne_lng": 36.9,
    "sw_lat": -1.3,
    "sw_lng": 36.8,
    "zoom": 10
  }
}
```

**Example Request**:
```bash
curl "https://hodi.co.ke/mobile/facilities/map/?device_id=YOUR_DEVICE_ID"
```

### 2. Resources Endpoint
**Endpoint**: `GET /mobile/resources/list/`

**Description**: Get all resources (documents, music) for mobile app in a single consolidated response

**Query Parameters**:
- `device_id` (required) - Device ID from mobile session
- `resource_type` (optional) - Filter by resource type: 'documents', 'music', or 'all' (default: 'all')
- `page` (optional) - Page number (default: 1)
- `page_size` (optional) - Items per page (default: 50, max: 200)

**Response Format**:
```json
{
  "documents": {
    "count": 25,
    "results": [
      {
        "document_id": 1,
        "title": "Document Title",
        "file_url": "https://...",
        ...
      }
    ]
  },
  "music": {
    "count": 10,
    "results": [
      {
        "music_id": 1,
        "name": "Track Name",
        "artist": "Artist Name",
        ...
      }
    ]
  },
  "total_count": 35
}
```

**Example Request**:
```bash
curl "https://hodi.co.ke/mobile/resources/list/?device_id=YOUR_DEVICE_ID&resource_type=all"
```

## Testing Steps

### Step 1: Create Mobile Session
```bash
curl -X POST "https://hodi.co.ke/mobile/sessions/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_mobile_device_123"
  }'
```

### Step 2: Test Facility Map Endpoint
```bash
curl "https://hodi.co.ke/mobile/facilities/map/?device_id=test_mobile_device_123"
```

### Step 3: Test Resources Endpoint
```bash
curl "https://hodi.co.ke/mobile/resources/list/?device_id=test_mobile_device_123"
```

### Step 4: Test with Viewport (Map)
```bash
curl "https://hodi.co.ke/mobile/facilities/map/?device_id=test_mobile_device_123&ne_lat=-1.2&ne_lng=36.9&sw_lat=-1.3&sw_lng=36.8&zoom=12"
```

### Step 5: Test Resources Filtering
```bash
# Get only documents
curl "https://hodi.co.ke/mobile/resources/list/?device_id=test_mobile_device_123&resource_type=documents"

# Get only music
curl "https://hodi.co.ke/mobile/resources/list/?device_id=test_mobile_device_123&resource_type=music"
```

## Mobile App Integration

### Android (Kotlin)
```kotlin
// Get facility coordinates for map
fun getFacilitiesForMap(deviceId: String, viewport: Viewport? = null): Call<FacilityMapResponse> {
    val params = mutableMapOf<String, String>()
    params["device_id"] = deviceId
    viewport?.let {
        params["ne_lat"] = it.northeast.latitude.toString()
        params["ne_lng"] = it.northeast.longitude.toString()
        params["sw_lat"] = it.southwest.latitude.toString()
        params["sw_lng"] = it.southwest.longitude.toString()
        params["zoom"] = it.zoom.toString()
    }
    return apiService.getFacilitiesMap(params)
}

// Get resources
fun getResources(deviceId: String, resourceType: String = "all"): Call<ResourcesResponse> {
    return apiService.getResources(deviceId, resourceType)
}
```

### iOS (Swift)
```swift
// Get facility coordinates for map
func getFacilitiesForMap(deviceId: String, viewport: Viewport? = nil) async throws -> FacilityMapResponse {
    var params = ["device_id": deviceId]
    if let viewport = viewport {
        params["ne_lat"] = String(viewport.northeast.latitude)
        params["ne_lng"] = String(viewport.northeast.longitude)
        params["sw_lat"] = String(viewport.southwest.latitude)
        params["sw_lng"] = String(viewport.southwest.longitude)
        params["zoom"] = String(viewport.zoom)
    }
    return try await apiService.getFacilitiesMap(params: params)
}

// Get resources
func getResources(deviceId: String, resourceType: String = "all") async throws -> ResourcesResponse {
    return try await apiService.getResources(deviceId: deviceId, resourceType: resourceType)
}
```

## Notes

1. **Authentication**: Both endpoints require a valid mobile session (device_id)
2. **Caching**: Responses include cache headers for mobile optimization
3. **Performance**: Map endpoint uses viewport filtering and zoom-based limiting for optimal performance
4. **Pagination**: Resources endpoint supports pagination for large datasets

