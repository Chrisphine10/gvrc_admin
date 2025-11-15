# Mobile App APIs

This app consolidates all mobile API endpoints for the GVRC mobile application.

## API Structure

All mobile APIs are now organized under the `/mobile/` URL prefix with clear separation from admin/management APIs.

### Available Mobile API Endpoints

#### 1. Mobile Chat API (`/mobile/chat/`)
- `POST /mobile/chat/start/` - Start or retrieve a conversation for the device
- `GET /mobile/chat/list/` - List all conversations for the device (open first)
- `GET /mobile/chat/{id}/detail/` - Fetch a single conversation with its messages
- `POST /mobile/chat/{id}/send-message/` - Send a new message within the conversation
- `POST /mobile/chat/{id}/close/` - Close the conversation when the user is done
- `PUT /mobile/chat/messages/{message_id}/status/` - Update delivery/read status for a message

#### 2. Mobile Facility API (`/mobile/facilities/`)
- `GET /mobile/facilities/list/` - List facilities (optimized for mobile)
- `GET /mobile/facilities/{id}/detail/` - Get facility details

#### 3. Mobile Session API (`/mobile/sessions/`)
- `POST /mobile/sessions/create/` - Create mobile session
- `POST /mobile/sessions/end/` - End mobile session

#### 4. Mobile Music API (`/mobile/music/`)
- `GET /mobile/music/list/` - List music tracks

#### 5. Mobile Document API (`/mobile/documents/`)
- `GET /mobile/documents/list/` - List documents

#### 6. Mobile Emergency API (`/mobile/emergency/`)
- `POST /mobile/emergency/sos/` - Send emergency SOS

#### 7. Mobile Lookup API (`/mobile/lookups/`)
- `GET /mobile/lookups/data/` - Get lookup data

#### 8. Mobile Analytics API (`/mobile/analytics/`)
- `POST /mobile/analytics/contact-interaction/` - Track contact interaction

## Authentication

- **Mobile Session APIs**: No authentication required (for session creation)
- **All Other Mobile APIs**: Require valid mobile session via `device_id` parameter

## Permission System

All mobile APIs use the `MobileSessionPermission` class which:
- Validates `device_id` from request
- Checks if mobile session exists and is active
- Stores session in `request.mobile_session` for use in views

## Benefits of This Organization

1. **Clear Separation**: Mobile APIs are completely separate from admin/management APIs
2. **Consolidated**: All mobile endpoints are in one place instead of scattered across apps
3. **Consistent**: All mobile APIs use the same permission and authentication system
4. **Maintainable**: Easier to manage and update mobile-specific functionality
5. **Documentation**: Better Swagger/OpenAPI documentation with proper tagging

## URL Structure

```
/mobile/                    # Mobile app root
├── chat/                   # Chat functionality
├── facilities/             # Facility information
├── sessions/               # Session management
├── music/                  # Music content
├── documents/              # Document access
├── emergency/              # Emergency services
├── lookups/                # Reference data
└── analytics/              # Usage tracking
```

## Migration Notes

- Mobile chat endpoints moved from `/chat/mobile/` to `/mobile/chat/`
- Mobile facility endpoints moved from `/api/mobile/facilities/` to `/mobile/facilities/`
- All mobile endpoints now use consistent permission and authentication patterns
- Admin/management endpoints remain under `/api/` and `/chat/admin/`
