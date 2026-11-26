# Swagger HTTPS Fix

## Problem
Swagger UI was generating API requests using HTTP instead of HTTPS, causing CORS errors when trying to test endpoints on `https://hodi.co.ke`.

**Error Message:**
```
Failed to fetch.
Possible Reasons:
- CORS
- Network Failure
- URL scheme must be "http" or "https" for CORS request.
```

## Solution
Created a custom `HTTPSchemaGenerator` class that:

1. **Detects HTTPS from the request** - Checks multiple methods:
   - `request.is_secure()`
   - `HTTP_X_FORWARDED_PROTO` header (for proxy/load balancer setups)
   - `HTTP_X_FORWARDED_SSL` header

2. **Falls back to settings** - If no request is available:
   - Checks `SECURE_SSL_REDIRECT` setting
   - Checks `DEBUG` mode (forces HTTPS in production)
   - Checks if `hodi.co.ke` is in `ALLOWED_HOSTS` (always use HTTPS)

3. **Sets the server URL in the OpenAPI schema** - Updates the `servers` field to use the correct scheme

## Changes Made

### File: `core/urls.py`

**Added:**
- Import for `OpenAPISchemaGenerator` from `drf_yasg.generators`
- Custom `HTTPSchemaGenerator` class
- Updated `schema_view` to use `generator_class=HTTPSchemaGenerator`

**Key Features:**
- Automatically detects HTTPS from request headers
- Forces HTTPS for `hodi.co.ke` domain
- Falls back gracefully to HTTP for local development
- Handles proxy/load balancer scenarios (AWS, Nginx, etc.)

## How It Works

1. When Swagger UI loads, it requests the OpenAPI schema
2. The custom generator intercepts the schema generation
3. It checks if the request is secure (HTTPS)
4. It sets the `servers` field in the schema to use `https://hodi.co.ke`
5. Swagger UI uses this server URL for all API requests

## Testing

After deploying this change:

1. Visit `https://hodi.co.ke/swagger/`
2. Open any endpoint (e.g., `POST /api/mobile/chat/start/`)
3. Click "Try it out"
4. The curl command should show `https://hodi.co.ke/api/mobile/chat/start/` (not `http://`)
5. The "Execute" button should work without CORS errors

## Production Considerations

- The fix automatically detects HTTPS in production
- Works with AWS Load Balancer (checks `HTTP_X_FORWARDED_PROTO`)
- Works with Nginx reverse proxy
- Falls back to HTTP only in local development (when `DEBUG=True`)

## Backward Compatibility

✅ **Fully backward compatible** - No breaking changes
- Local development still works (uses HTTP when appropriate)
- Production automatically uses HTTPS
- No changes needed to existing API endpoints

