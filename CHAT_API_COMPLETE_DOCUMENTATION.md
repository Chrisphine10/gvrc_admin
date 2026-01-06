# Complete Chat API Documentation

## Overview

The Hodi Admin system provides comprehensive chat functionality through both REST APIs and WebSocket connections. This documentation covers all chat-related endpoints for mobile apps, web interfaces, and admin management.

## Base URLs

- **Mobile Chat APIs**: `/mobile/chat/`
- **Admin Chat APIs**: `/chat/admin/`
- **Web Chat Interface**: `/chat/`
- **WebSocket (Mobile)**: `ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx`
- **WebSocket (Web/Admin)**: `ws://host/ws/chat/{conversation_id}/`

---

## 1. Mobile Chat APIs (`/mobile/chat/`)

### Authentication
- **Method**: `device_id` query parameter or in request body
- **Requirement**: Active `MobileSession` with matching `device_id`
- **No Django Authentication**: Mobile users don't need to log in

---

### 1.1 Start/Retrieve Conversation

**Endpoint**: `POST /mobile/chat/start/`

**Description**: Start a new conversation or retrieve existing open conversation for the device.

**Request Body**:
```json
{
  "device_id": "mobile_device_abc123",
  "subject": "I need help with..."
}
```

**Query Parameters** (alternative):
- `device_id` (optional if in body)

**Response** (200 OK - Existing conversation):
```json
{
  "conversation_id": "123",
  "status": "active",
  "subject": "I need help with...",
  "created_at": "2024-01-01T12:00:00Z",
  "last_message_at": "2024-01-01T12:30:00Z",
  "mobile_session": {
    "device_id": "mobile_device_abc123"
  },
  "assigned_to": {
    "id": 1,
    "username": "admin_user"
  },
  "message_count": 5
}
```

**Response** (201 Created - New conversation):
```json
{
  "conversation_id": "124",
  "status": "new",
  "subject": "I need help with...",
  "created_at": "2024-01-01T13:00:00Z",
  "last_message_at": null,
  "mobile_session": {
    "device_id": "mobile_device_abc123"
  },
  "assigned_to": {
    "id": 1,
    "username": "admin_user"
  },
  "message_count": 0
}
```

**Error Responses**:
- `400 Bad Request`: Missing device_id or invalid data
- `400 Bad Request`: Invalid or inactive device ID

**Notes**:
- If an open conversation exists (status: 'new' or 'active'), it returns that conversation
- If no open conversation exists, creates a new one
- New conversations are automatically assigned to an available admin

---

### 1.2 List Conversations

**Endpoint**: `GET /mobile/chat/list/?device_id=xxx`

**Description**: List all conversations for a mobile device, with open conversations appearing first.

**Query Parameters**:
- `device_id` (required): Device identifier

**Response** (200 OK):
```json
[
  {
    "conversation_id": "123",
    "status": "active",
    "subject": "Current issue",
    "created_at": "2024-01-01T12:00:00Z",
    "last_message_at": "2024-01-01T12:30:00Z",
    "message_count": 5,
    "unread_count": 2
  },
  {
    "conversation_id": "122",
    "status": "closed",
    "subject": "Previous issue",
    "created_at": "2024-01-01T10:00:00Z",
    "last_message_at": "2024-01-01T11:00:00Z",
    "message_count": 10,
    "unread_count": 0
  }
]
```

**Ordering**:
- Open conversations (status: 'new', 'active') appear first
- Sorted by `last_message_at` (newest first)
- Closed conversations appear after open ones

**Error Responses**:
- `400 Bad Request`: Missing device_id parameter
- `400 Bad Request`: Invalid or inactive device ID

---

### 1.3 Get Conversation Detail

**Endpoint**: `GET /mobile/chat/{conversation_id}/detail/?device_id=xxx`

**Description**: Get full conversation details including all messages.

**URL Parameters**:
- `conversation_id`: Conversation identifier

**Query Parameters**:
- `device_id` (required): Device identifier

**Response** (200 OK):
```json
{
  "conversation_id": "123",
  "status": "active",
  "subject": "I need help",
  "created_at": "2024-01-01T12:00:00Z",
  "last_message_at": "2024-01-01T12:30:00Z",
  "mobile_session": {
    "device_id": "mobile_device_abc123",
    "latitude": -1.2921,
    "longitude": 36.8219
  },
  "assigned_to": {
    "id": 1,
    "username": "admin_user",
    "full_name": "Admin User"
  },
  "messages": [
    {
      "message_id": "456",
      "content": "Hello, I need help",
      "message_type": "text",
      "sender_type": "mobile",
      "created_at": "2024-01-01T12:00:00Z",
      "status": "delivered",
      "is_urgent": false
    },
    {
      "message_id": "457",
      "content": "How can I assist you?",
      "message_type": "text",
      "sender_type": "admin",
      "created_at": "2024-01-01T12:05:00Z",
      "status": "read",
      "is_urgent": false,
      "sender": {
        "id": 1,
        "username": "admin_user"
      }
    }
  ],
  "message_count": 2
}
```

**Error Responses**:
- `400 Bad Request`: Missing device_id
- `403 Forbidden`: Access denied (conversation doesn't belong to device)
- `404 Not Found`: Conversation not found

---

### 1.4 Send Message (REST API)

**Endpoint**: `POST /mobile/chat/{conversation_id}/send-message/?device_id=xxx`

**Description**: Send a message in a conversation via REST API. For real-time messaging, use WebSocket instead.

**URL Parameters**:
- `conversation_id`: Conversation identifier

**Query Parameters**:
- `device_id` (required): Device identifier

**Request Body** (JSON):
```json
{
  "content": "This is my message",
  "message_type": "text",
  "is_urgent": false,
  "metadata": {}
}
```

**Request Body** (Multipart Form Data - for file uploads):
```
content: "Check this image"
message_type: "image"
media_file: [binary file]
is_urgent: false
```

**Message Types**:
- `text`: Plain text message
- `image`: Image file (auto-detected from file content type)
- `voice`: Audio file (auto-detected from file content type)
- `file`: Other file types (auto-detected from file content type)

**Response** (201 Created):
```json
{
  "message_id": "789",
  "content": "This is my message",
  "message_type": "text",
  "sender_type": "mobile",
  "conversation": "123",
  "created_at": "2024-01-01T13:00:00Z",
  "status": "sent",
  "is_urgent": false,
  "media_file_url": null,
  "media_url": null,
  "metadata": {}
}
```

**Error Responses**:
- `400 Bad Request`: Missing device_id or invalid data
- `403 Forbidden`: Access denied
- `404 Not Found`: Conversation not found

**Notes**:
- For real-time messaging, use WebSocket endpoint instead
- File uploads are supported via multipart/form-data
- Message type is auto-detected from file content type if not specified

---

### 1.5 Update Message Status

**Endpoint**: `PUT /mobile/chat/messages/{message_id}/status/?device_id=xxx`

**Description**: Update message delivery or read status.

**URL Parameters**:
- `message_id`: Message identifier

**Query Parameters**:
- `device_id` (required): Device identifier

**Request Body**:
```json
{
  "status": "delivered"
}
```

**Status Values**:
- `delivered`: Message was delivered to recipient
- `read`: Message was read by recipient

**Response** (200 OK):
```json
{
  "message_id": "789",
  "content": "This is my message",
  "status": "delivered",
  "delivered_at": "2024-01-01T13:01:00Z",
  "read_at": null
}
```

**Error Responses**:
- `400 Bad Request`: Missing device_id or invalid status
- `403 Forbidden`: Access denied
- `404 Not Found`: Message not found

---

### 1.6 Close Conversation

**Endpoint**: `POST /mobile/chat/{conversation_id}/close/?device_id=xxx`

**Description**: Close a conversation when the user is done.

**URL Parameters**:
- `conversation_id`: Conversation identifier

**Query Parameters**:
- `device_id` (required): Device identifier

**Response** (200 OK):
```json
{
  "message": "Conversation closed successfully",
  "conversation": {
    "conversation_id": "123",
    "status": "closed",
    "subject": "I need help",
    "created_at": "2024-01-01T12:00:00Z",
    "last_message_at": "2024-01-01T13:00:00Z"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Missing device_id
- `400 Bad Request`: Conversation already closed
- `403 Forbidden`: Access denied
- `404 Not Found`: Conversation not found

---

### 1.7 Get WebSocket Connection Info

**Endpoint**: `GET /mobile/chat/websocket-info/?device_id=xxx`

**Description**: Get WebSocket connection information and documentation.

**Response** (200 OK):
```json
{
  "websocket_url": "ws://host/ws/mobile/chat/{conversation_id}/?device_id={device_id}",
  "websocket_url_production": "wss://host/ws/mobile/chat/{conversation_id}/?device_id={device_id}",
  "authentication": "device_id query parameter (must correspond to active MobileSession)",
  "features": [
    "real-time bidirectional messaging",
    "typing indicators",
    "read receipts",
    "message status updates (sent, delivered, read)",
    "user presence notifications",
    "media support (images, files)",
    "urgent message flagging"
  ],
  "message_types": {
    "chat_message": "Send and receive chat messages in real-time",
    "message_status": "Update message delivery/read status",
    "typing_indicator": "Show when user is typing",
    "read_receipt": "Mark messages as read"
  },
  "connection_flow": [
    "1. Call POST /mobile/chat/start/ with device_id to get conversation_id",
    "2. Connect to WebSocket: ws://host/ws/mobile/chat/{conversation_id}/?device_id={device_id}",
    "3. Wait for connection_established message",
    "4. Start sending/receiving messages in real-time",
    "5. Use REST API endpoints for conversation management (list, close, etc.)"
  ]
}
```

---

## 2. WebSocket Chat Endpoint (Mobile)

### 2.1 Connection

**URL Format**: `ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx`

**Production URL**: `wss://host/ws/mobile/chat/{conversation_id}/?device_id=xxx`

**Authentication**: `device_id` query parameter (must match active MobileSession)

**Connection Flow**:
1. Get `conversation_id` from `POST /mobile/chat/start/`
2. Connect to WebSocket with `device_id` in query string
3. Wait for `connection_established` message
4. Start sending/receiving messages

---

### 2.2 Message Types (WebSocket)

#### Send Chat Message
```json
{
  "type": "chat_message",
  "content": "Hello, I need help!",
  "message_type": "text",
  "is_urgent": false,
  "metadata": {}
}
```

#### Send Image Message
```json
{
  "type": "chat_message",
  "content": "Check this image",
  "message_type": "image",
  "media_url": "https://example.com/image.jpg",
  "is_urgent": false,
  "metadata": {
    "file_name": "photo.jpg",
    "file_size": 1024000
  }
}
```

#### Update Message Status
```json
{
  "type": "message_status",
  "message_id": "789",
  "status": "delivered"
}
```

#### Send Typing Indicator
```json
{
  "type": "typing_indicator",
  "is_typing": true
}
```

#### Send Read Receipt
```json
{
  "type": "read_receipt",
  "message_id": "789"
}
```

---

### 2.3 Receive Messages (WebSocket)

#### Incoming Chat Message
```json
{
  "type": "chat_message",
  "message": {
    "message_id": "790",
    "content": "How can I help you?",
    "message_type": "text",
    "sender_type": "admin",
    "created_at": "2024-01-01T13:05:00Z",
    "status": "sent",
    "is_urgent": false,
    "sender": {
      "id": 1,
      "username": "admin_user",
      "full_name": "Admin User"
    }
  }
}
```

#### Connection Established
```json
{
  "type": "connection_established",
  "conversation_id": "123",
  "device_id": "mobile_device_abc123",
  "timestamp": "2024-01-01T13:00:00Z"
}
```

#### Typing Indicator
```json
{
  "type": "typing_indicator",
  "user_id": 1,
  "username": "admin_user",
  "is_typing": true
}
```

#### User Presence
```json
{
  "type": "user_presence",
  "user_id": 1,
  "username": "admin_user",
  "is_online": true
}
```

#### Error Message
```json
{
  "type": "error",
  "code": "4001",
  "message": "Missing device_id parameter"
}
```

**Error Codes**:
- `4001`: Missing device_id parameter
- `4002`: Invalid or inactive device_id
- `4003`: Conversation not found
- `4004`: Access denied (conversation doesn't belong to device)

---

## 3. Admin Chat APIs (`/chat/admin/`)

### Authentication
- **Method**: Django session authentication or API token
- **Requirement**: Staff user authentication required
- **Access**: Admin users only

---

### 3.1 List All Conversations (Admin)

**Endpoint**: `GET /chat/admin/conversations/`

**Description**: Get all conversations for admin management.

**Query Parameters**:
- `status`: Filter by status (new, active, closed)
- `assigned_to`: Filter by assigned admin user ID
- `search`: Search in subject or messages
- `ordering`: Order by field (default: -last_message_at)

**Response** (200 OK):
```json
{
  "count": 150,
  "next": "http://host/chat/admin/conversations/?page=2",
  "previous": null,
  "results": [
    {
      "conversation_id": "123",
      "status": "active",
      "subject": "User needs help",
      "created_at": "2024-01-01T12:00:00Z",
      "last_message_at": "2024-01-01T13:00:00Z",
      "mobile_session": {
        "device_id": "mobile_device_abc123"
      },
      "assigned_to": {
        "id": 1,
        "username": "admin_user"
      },
      "message_count": 10,
      "unread_count": 3
    }
  ]
}
```

---

### 3.2 Get Conversation Detail (Admin)

**Endpoint**: `GET /chat/admin/conversations/{conversation_id}/`

**Description**: Get full conversation details with all messages.

**Response**: Same format as mobile conversation detail, but includes admin-only fields.

---

### 3.3 Send Admin Message

**Endpoint**: `POST /chat/admin/conversations/{conversation_id}/send_message/`

**Description**: Send a message as an admin user.

**Request Body**:
```json
{
  "content": "Admin response",
  "message_type": "text",
  "is_urgent": false,
  "metadata": {}
}
```

**Response**: Message object with admin sender information.

---

### 3.4 Assign Conversation

**Endpoint**: `POST /chat/admin/conversations/{conversation_id}/assign/`

**Description**: Assign conversation to an admin user.

**Request Body**:
```json
{
  "assigned_to": 1
}
```

**Response** (200 OK):
```json
{
  "message": "Conversation assigned successfully",
  "conversation": {
    "conversation_id": "123",
    "assigned_to": {
      "id": 1,
      "username": "admin_user"
    }
  }
}
```

---

### 3.5 Update Conversation Status

**Endpoint**: `PATCH /chat/admin/conversations/{conversation_id}/`

**Description**: Update conversation status.

**Request Body**:
```json
{
  "status": "closed"
}
```

**Status Values**: `new`, `active`, `closed`, `resolved`

---

### 3.6 Get Notifications

**Endpoint**: `GET /chat/admin/notifications/`

**Description**: Get real-time notifications for admin users.

**Query Parameters**:
- `unread_only`: Filter unread notifications only
- `limit`: Number of notifications to return

**Response** (200 OK):
```json
{
  "count": 5,
  "unread_count": 2,
  "notifications": [
    {
      "id": 1,
      "type": "new_conversation",
      "message": "New conversation started",
      "conversation_id": "123",
      "created_at": "2024-01-01T13:00:00Z",
      "is_read": false
    }
  ]
}
```

---

## 4. Web Chat Interface APIs

### 4.1 List Conversations (Web)

**Endpoint**: `GET /chat/`

**Description**: Web interface for listing conversations (requires staff login).

**Access**: Staff users only via web browser.

---

### 4.2 Conversation Detail (Web)

**Endpoint**: `GET /chat/conversation/{conversation_id}/`

**Description**: Web interface for viewing conversation details.

**Features**:
- Real-time message updates via WebSocket
- File upload support
- Message status indicators
- Typing indicators

---

### 4.3 Assign Conversation (Web)

**Endpoint**: `POST /chat/conversation/{conversation_id}/assign/`

**Description**: Assign conversation to current user or another admin.

**Request Body**:
```json
{
  "assigned_to": 1
}
```

---

### 4.4 Update Conversation Status (Web)

**Endpoint**: `POST /chat/conversation/{conversation_id}/status/`

**Description**: Update conversation status from web interface.

**Request Body**:
```json
{
  "status": "closed"
}
```

---

## 5. WebSocket Chat Endpoint (Web/Admin)

### 5.1 Connection

**URL Format**: `ws://host/ws/chat/{conversation_id}/`

**Production URL**: `wss://host/ws/chat/{conversation_id}/`

**Authentication**: Django session authentication (automatic via cookies)

**Connection Flow**:
1. User must be logged in as staff user
2. Connect to WebSocket (session cookie automatically sent)
3. Wait for `connection_established` message
4. Start sending/receiving messages

---

### 5.2 Message Types

Same message types as mobile WebSocket, but uses Django session authentication instead of device_id.

---

## 6. Complete API Summary

### Mobile Chat APIs (No Authentication Required)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mobile/chat/start/` | POST | Start/retrieve conversation |
| `/mobile/chat/list/` | GET | List conversations |
| `/mobile/chat/{id}/detail/` | GET | Get conversation details |
| `/mobile/chat/{id}/send-message/` | POST | Send message (REST) |
| `/mobile/chat/{id}/close/` | POST | Close conversation |
| `/mobile/chat/messages/{id}/status/` | PUT | Update message status |
| `/mobile/chat/websocket-info/` | GET | Get WebSocket info |

### Admin Chat APIs (Staff Authentication Required)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat/admin/conversations/` | GET | List all conversations |
| `/chat/admin/conversations/{id}/` | GET | Get conversation detail |
| `/chat/admin/conversations/{id}/send_message/` | POST | Send admin message |
| `/chat/admin/conversations/{id}/assign/` | POST | Assign conversation |
| `/chat/admin/conversations/{id}/` | PATCH | Update conversation |
| `/chat/admin/notifications/` | GET | Get notifications |

### WebSocket Endpoints
| Endpoint | Authentication | Use Case |
|----------|---------------|----------|
| `ws://host/ws/mobile/chat/{id}/?device_id=xxx` | device_id | Mobile real-time chat |
| `ws://host/ws/chat/{id}/` | Django session | Web/admin real-time chat |

---

## 7. Best Practices

### For Mobile Apps:
1. **Use WebSocket for real-time messaging**: Better performance and user experience
2. **Use REST API for conversation management**: List, start, close conversations
3. **Update message status**: Mark messages as delivered/read for better UX
4. **Handle connection errors**: Implement reconnection logic for WebSocket
5. **Pagination**: Use pagination for large conversation lists

### For Web/Admin:
1. **Use WebSocket for active conversations**: Real-time updates
2. **Use REST API for management**: Assign, update status, export
3. **Monitor notifications**: Check for new conversations regularly
4. **Handle file uploads**: Support multipart/form-data for media

---

## 8. Error Handling

### Common Error Responses

**400 Bad Request**:
```json
{
  "error": "device_id is required for mobile users"
}
```

**403 Forbidden**:
```json
{
  "error": "Access denied to this conversation"
}
```

**404 Not Found**:
```json
{
  "error": "Conversation not found"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Failed to create message: [error details]"
}
```

---

## 9. Rate Limiting

Currently, there are no rate limits on chat APIs. However, best practices:
- Mobile apps: Limit message sending to reasonable frequency
- WebSocket: Maintain single connection per conversation
- REST API: Use pagination for large data sets

---

## 10. Testing

### Test Mobile Chat API:
```bash
# 1. Create mobile session
curl -X POST http://host/mobile/sessions/create/ \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device-123"}'

# 2. Start conversation
curl -X POST http://host/mobile/chat/start/ \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device-123", "subject": "Test"}'

# 3. List conversations
curl "http://host/mobile/chat/list/?device_id=test-device-123"

# 4. Send message
curl -X POST "http://host/mobile/chat/123/send-message/?device_id=test-device-123" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello", "message_type": "text"}'
```

---

## Support

For issues or questions:
- Check WebSocket connection info: `GET /mobile/chat/websocket-info/`
- Review error messages in API responses
- Check mobile session is active: `GET /mobile/sessions/?device_id=xxx`


