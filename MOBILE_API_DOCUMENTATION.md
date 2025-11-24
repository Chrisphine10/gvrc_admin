# Mobile API Documentation

## Overview
The Hodi Admin system provides a dedicated mobile API section designed specifically for mobile applications and field workers. This API uses mobile session-based authentication, allowing anonymous mobile app users to access services without traditional user login. The mobile session acts as the authentication mechanism, providing device tracking, location awareness, and user analytics.

## Mobile API Base URL
```
/api/mobile/
```

## Available Mobile Endpoints

### 1. Facilities
- **Endpoint**: `/api/mobile/facilities/`
- **Method**: GET
- **Description**: Get a simplified list of facilities optimized for mobile consumption
- **Features**: Pagination, filtering, mobile-optimized response format

### 2. Emergency SOS
- **Endpoint**: `/api/mobile/emergency-sos/`
- **Method**: POST
- **Description**: Find nearest emergency facilities using mobile session location
- **Features**: Location-aware emergency services, automatic GPS from session
- **Request Format**:
  ```json
  {
    "device_id": "mobile_device_abc123",
    "emergency_type": "Medical",
    "radius_km": 5
  }
  ```
  **Note**: Location automatically retrieved from mobile session, no need to provide coordinates
  **Requirements**: Mobile session must have valid GPS coordinates stored
  **Important**: The API no longer expects `latitude` and `longitude` in the request body - these are automatically retrieved from the mobile session

### 3. Music
- **Endpoint**: `/api/mobile/music/`
- **Method**: GET
- **Description**: Access music content for mobile applications
- **Features**: Mobile-optimized music streaming and metadata

### 4. Documents
- **Endpoint**: `/api/mobile/documents/`
- **Method**: GET
- **Description**: Access documents optimized for mobile viewing
- **Features**: Mobile-friendly document formats and metadata

### 5. Sessions
- **Endpoint**: `/api/mobile/sessions/`
- **Method**: POST
- **Description**: Create new mobile device sessions
- **Features**: Device tracking, location updates, session management

### 6. Session End
- **Endpoint**: `/api/mobile/sessions/end/`
- **Method**: POST
- **Description**: End mobile device sessions
- **Features**: Clean session termination, device cleanup

### 7. Contact Interaction (NEW)
- **Endpoint**: `/api/mobile/contact-interaction/`
- **Method**: POST
- **Description**: Track contact interactions from mobile devices
- **Features**: Mobile-optimized analytics, device tracking, location awareness

## Contact Interaction API Details

### Purpose
The Contact Interaction API has been moved to the mobile API section to provide mobile applications with a dedicated endpoint for tracking user interactions with facility contacts.

### Request Format
```json
{
  "contact_id": 123,
  "device_id": "mobile_device_abc123",
  "is_helpful": true
}
```

**Note**: `device_id` is required in the request body to identify the mobile session, and location data is automatically retrieved from the mobile session.

### Required Fields
- `contact_id`: The ID of the facility contact being interacted with
- `device_id`: Unique identifier for the mobile device (identifies the mobile session)

### Optional Fields
- `is_helpful`: Boolean indicating if the contact was helpful
- **Location**: Automatically retrieved from mobile session (no need to provide)

### Response Format
```json
{
  "success": true,
  "message": "Contact interaction tracked successfully",
  "data": {
    "interaction_id": 456,
    "contact": {
      "id": 123,
      "type": "Phone",
      "value": "+254700000000"
    },
    "tracked_at": "2025-01-21T10:30:00Z",
    "helpful": true,
    "device_id": "mobile_device_abc123"
  }
}
```

### Authentication
- **Required**: Valid mobile session (device_id)
- **Method**: Mobile session validation
- **Permission**: Active mobile session required
- **Note**: No traditional user login required - mobile session acts as authentication

### Error Responses
- **400 Bad Request**: Missing required fields
- **401 Unauthorized**: Authentication required
- **404 Not Found**: Contact not found
- **500 Internal Server Error**: Server processing error

## Mobile Session Authentication Flow

### How It Works
1. **Session Creation**: Mobile app creates a session with device ID and location
2. **Session Validation**: All mobile API calls validate the device_id against active sessions
3. **Anonymous Access**: No user login required - mobile session acts as authentication
4. **Location Tracking**: GPS coordinates stored in session for location-based services
5. **Activity Monitoring**: Session tracks last activity and updates automatically

### Location Services
- **Automatic Location**: GPS coordinates are automatically retrieved from the mobile session
- **No Manual Input**: Users don't need to provide latitude/longitude in API requests
- **Real-time Updates**: Location is updated whenever the mobile app updates the session
- **Privacy First**: Location data stays within the mobile session and is not exposed in API requests

### Benefits of Mobile API Structure

1. **Anonymous Access**: No user registration or login required
2. **Device-Based Auth**: Mobile session acts as authentication mechanism
3. **Location Awareness**: GPS coordinates automatically available from session
4. **Device Tracking**: Built-in mobile device session management
5. **Performance**: Optimized queries and response formats
6. **User Privacy**: No personal information required for basic functionality

## Migration from General API

The contact interaction functionality was previously available at `/api/analytics/contact-interaction/` and is now also available at `/api/mobile/contact-interaction/` with mobile-specific optimizations:

- **Web Usage**: Continue using `/api/analytics/contact-interaction/`
- **Mobile Usage**: Use `/api/mobile/contact-interaction/` for better mobile integration

## Testing

### 1. Create Mobile Session First
```bash
curl -X POST http://localhost:8000/api/mobile/sessions/ \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_mobile_device_123",
    "latitude": -1.2921,
    "longitude": 36.8219,
    "location_permission_granted": true
  }'
```

### 2. Test Contact Interaction Endpoint
```bash
curl -X POST "http://localhost:8000/api/mobile/contact-interaction/" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 123,
    "device_id": "test_mobile_device_123",
    "is_helpful": true
  }'
```

### 3. Test Emergency SOS Endpoint
```bash
curl -X POST "http://localhost:8000/api/mobile/emergency-sos/" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_mobile_device_123",
    "emergency_type": "Medical",
    "radius_km": 5
  }'
```

**Note**: The `device_id` is required in the request body to identify the mobile session, and location data is automatically retrieved from the mobile session. No need to provide coordinates.

## Future Enhancements

The mobile API structure is designed to be extensible for future mobile-specific features:

- Push notifications
- Offline data synchronization
- Mobile-specific data formats
- Enhanced device management
- Mobile analytics and reporting

## Troubleshooting

### Common Error Messages

#### 1. "device_id is required"
**Cause**: Missing device_id in request
**Solution**: Include device_id in request body for POST requests or as query parameter for GET requests

#### 2. "Mobile session not found or inactive"
**Cause**: Invalid device_id or expired session
**Solution**: Create a new mobile session first using `/api/mobile/sessions/`

#### 3. "Location not available in mobile session"
**Cause**: Mobile session doesn't have GPS coordinates
**Solution**: Update mobile session with current location before using location-based features

#### 4. "latitude/longitude field is required" (Emergency SOS)
**Cause**: Old API version expected coordinates in request body
**Solution**: The API now automatically gets location from mobile session. Ensure your mobile session has valid GPS coordinates and only send `device_id` and `emergency_type` in the request body.

### Debug Steps

1. **Check Mobile Session**: Verify session exists and is active
2. **Validate device_id**: Ensure device_id matches an active session
3. **Check Location**: Verify session has valid GPS coordinates
4. **Review Request Format**: Ensure all required fields are provided

### Example Debug Request

```bash
# First, check if session exists
curl -X POST "http://localhost:8000/api/mobile/sessions/" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "debug_device_123",
    "latitude": -1.2921,
    "longitude": 36.8219
  }'

# Then test the endpoint
curl -X POST "http://localhost:8000/api/mobile/emergency-sos/" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "debug_device_123",
    "emergency_type": "Medical"
  }'
```
