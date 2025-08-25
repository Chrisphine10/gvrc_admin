# API Organization - GVRC Admin System

## Overview

The API structure has been reorganized to provide clear separation between mobile and admin/management endpoints, making the system more maintainable and easier to understand.

## New API Structure

### 1. Mobile APIs (`/mobile/`)
**Purpose**: All mobile app endpoints consolidated in one place
**Authentication**: Mobile session-based (device_id)
**Access**: Public (no admin authentication required)

```
/mobile/
├── chat/                   # Chat functionality
│   ├── start/             # Start/retrieve conversation
│   ├── list/              # List conversations
│   ├── {id}/detail/       # Conversation details
│   ├── {id}/send-message/ # Send message
│   └── messages/{id}/status # Update message status
├── facilities/             # Facility information
│   ├── list/              # List facilities (mobile-optimized)
│   └── {id}/detail/       # Facility details
├── sessions/               # Session management
│   ├── create/            # Create mobile session
│   └── end/               # End mobile session
├── music/                  # Music content
│   └── list/              # List music tracks
├── documents/              # Document access
│   └── list/              # List documents
├── emergency/              # Emergency services
│   └── sos/               # Send emergency SOS
├── lookups/                # Reference data
│   └── data/              # Get lookup data
└── analytics/              # Usage tracking
    └── contact-interaction # Track contact interaction
```

### 2. Admin/Management APIs (`/api/`)
**Purpose**: Administrative and management functions
**Authentication**: Staff user authentication required
**Access**: Admin users only

```
/api/
├── facilities/             # Facility management
├── analytics/              # Analytics and reporting
├── statistics/             # System statistics
├── lookups/                # Lookup data management
├── geography/              # Geographic data
├── auth/token/            # Authentication
└── status/                # System status
```

### 3. Web Interface APIs (`/chat/admin/`)
**Purpose**: Web-based chat administration
**Authentication**: Staff user authentication required
**Access**: Admin users only

```
/chat/admin/
├── conversations/          # Conversation management
│   ├── list/              # List all conversations
│   ├── {id}/detail/       # Conversation details
│   ├── {id}/assign/       # Assign conversation
│   ├── {id}/status/       # Update status
│   ├── {id}/send-message/ # Send admin message
│   ├── {id}/resolve/      # Mark resolved
│   └── stats/             # Conversation statistics
└── notifications/          # Notification management
    ├── unread/            # List unread notifications
    ├── {id}/mark-read/    # Mark notification read
    └── mark-all-read/     # Mark all notifications read
```

### 4. Web Interface Pages (`/chat/`, `/facilities/`, etc.)
**Purpose**: HTML-based web interfaces
**Authentication**: Staff user authentication required
**Access**: Admin users only

```
/chat/                     # Chat web interface
/facilities/               # Facilities web interface
/music/                    # Music web interface
/documents/                # Documents web interface
```

## Benefits of New Organization

### 1. Clear Separation of Concerns
- **Mobile APIs**: Optimized for mobile app consumption
- **Admin APIs**: Administrative and management functions
- **Web APIs**: Web interface backend functionality
- **Web Pages**: HTML-based user interfaces

### 2. Consistent Authentication Patterns
- **Mobile**: Session-based authentication via device_id
- **Admin/Web**: Staff user authentication via Django auth

### 3. Better Maintainability
- All mobile endpoints in one app (`apps.mobile`)
- Admin endpoints remain in respective apps
- Clear URL structure and routing

### 4. Improved Documentation
- Better Swagger/OpenAPI organization
- Proper tagging for different API types
- Clearer endpoint grouping

## Migration Notes

### What Changed
1. **Mobile chat endpoints**: `/chat/mobile/` → `/mobile/chat/`
2. **Mobile facility endpoints**: `/api/mobile/facilities/` → `/mobile/facilities/`
3. **Mobile session endpoints**: `/api/mobile/sessions/` → `/mobile/sessions/`
4. **Mobile music endpoints**: `/api/mobile/music/` → `/mobile/music/`
5. **Mobile document endpoints**: `/api/mobile/documents/` → `/mobile/documents/`
6. **Mobile emergency endpoints**: `/api/mobile/emergency-sos/` → `/mobile/emergency/sos/`
7. **Mobile lookup endpoints**: `/api/mobile/lookups/` → `/mobile/lookups/data/`
8. **Mobile analytics endpoints**: `/api/mobile/contact-interaction/` → `/mobile/analytics/contact-interaction/`

### What Remains the Same
1. **Admin APIs**: Still under `/api/` for facility management, analytics, etc.
2. **Web chat admin**: Still under `/chat/admin/` for conversation management
3. **Web interfaces**: Still under `/chat/`, `/facilities/`, etc. for HTML pages

## Testing the New Structure

### Mobile API Endpoints
```bash
# Test mobile session creation
curl -X POST http://localhost:8000/mobile/sessions/create/ \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device-123"}'

# Test mobile facilities list
curl "http://localhost:8000/mobile/facilities/list/?device_id=test-device-123"

# Test mobile chat start
curl -X POST http://localhost:8000/mobile/chat/start/ \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device-123", "subject": "Test conversation"}'
```

### Admin API Endpoints
```bash
# Test admin facilities list (requires authentication)
curl -H "Authorization: Token YOUR_ADMIN_TOKEN" \
  http://localhost:8000/api/facilities/

# Test admin chat conversations (requires authentication)
curl -H "Authorization: Token YOUR_ADMIN_TOKEN" \
  http://localhost:8000/chat/admin/conversations/list/
```

## Future Enhancements

1. **API Versioning**: Consider adding versioning (e.g., `/mobile/v1/`)
2. **Rate Limiting**: Implement rate limiting for mobile APIs
3. **Caching**: Add caching for frequently accessed mobile data
4. **Monitoring**: Enhanced monitoring and analytics for mobile API usage
