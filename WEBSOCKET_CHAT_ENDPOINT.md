# WebSocket Chat Endpoint Documentation

## Overview

A new WebSocket endpoint has been added to enable real-time chat functionality for mobile users. This endpoint uses `device_id` authentication instead of Django session authentication, making it perfect for mobile applications.

## Endpoint Details

### URL Format
```
ws://your-domain/ws/mobile/chat/{conversation_id}/?device_id=xxx
```

### Example
```
ws://hodi.co.ke/ws/mobile/chat/123/?device_id=abc123xyz
```

### For Production (HTTPS/WSS)
```
wss://hodi.co.ke/ws/mobile/chat/123/?device_id=abc123xyz
```

## Authentication

- **Method**: Query parameter `device_id`
- **Validation**: The `device_id` must correspond to an active `MobileSession`
- **No Django Authentication Required**: Mobile users don't need to be logged in via Django sessions

## Connection Flow

1. **Get Conversation ID**: First, use the REST API to start or retrieve a conversation:
   ```
   POST /mobile/chat/start/
   {
     "device_id": "abc123xyz",
     "subject": "Help needed"
   }
   ```

2. **Connect to WebSocket**: Use the `conversation_id` from the response:
   ```
   ws://host/ws/mobile/chat/{conversation_id}/?device_id=abc123xyz
   ```

3. **Receive Connection Confirmation**: Upon successful connection, you'll receive:
   ```json
   {
     "type": "connection_established",
     "conversation_id": 123,
     "device_id": "abc123xyz",
     "timestamp": "2024-01-01T12:00:00Z"
   }
   ```

## Message Types

### Sending Messages

**Send a chat message:**
```json
{
  "type": "chat_message",
  "content": "Hello, I need help!",
  "message_type": "text",
  "is_urgent": false,
  "metadata": {}
}
```

**Send with media:**
```json
{
  "type": "chat_message",
  "content": "Check this image",
  "message_type": "image",
  "media_url": "https://example.com/image.jpg",
  "is_urgent": false,
  "metadata": {}
}
```

### Receiving Messages

**Incoming message:**
```json
{
  "type": "chat_message",
  "message": {
    "message_id": 456,
    "content": "Hello, I need help!",
    "message_type": "text",
    "media_url": "",
    "is_urgent": false,
    "sender_type": "mobile",
    "sender_info": {
      "type": "mobile_user",
      "device_id": "abc123xyz"
    },
    "sent_at": "2024-01-01T12:00:00Z",
    "status": "sent"
  }
}
```

### Message Status Updates

**Update message status:**
```json
{
  "type": "message_status",
  "message_id": 456,
  "status": "delivered"
}
```

**Receive status update:**
```json
{
  "type": "message_status_update",
  "message_id": 456,
  "status": "read",
  "timestamp": "2024-01-01T12:00:01Z"
}
```

### Typing Indicators

**Send typing indicator:**
```json
{
  "type": "typing_indicator",
  "is_typing": true
}
```

**Receive typing indicator:**
```json
{
  "type": "typing_indicator",
  "device_id": "abc123xyz",
  "user_id": 1,
  "is_typing": true,
  "timestamp": "2024-01-01T12:00:02Z"
}
```

### Read Receipts

**Mark messages as read:**
```json
{
  "type": "read_receipt",
  "message_ids": [456, 457, 458]
}
```

**Receive read receipt:**
```json
{
  "type": "read_receipt",
  "device_id": "abc123xyz",
  "user_id": 1,
  "message_ids": [456, 457, 458],
  "timestamp": "2024-01-01T12:00:03Z"
}
```

### User Presence

**User joined notification:**
```json
{
  "type": "mobile_user_joined",
  "device_id": "abc123xyz",
  "timestamp": "2024-01-01T12:00:04Z"
}
```

**User left notification:**
```json
{
  "type": "mobile_user_left",
  "device_id": "abc123xyz",
  "timestamp": "2024-01-01T12:00:05Z"
}
```

## Error Handling

### Connection Errors

The WebSocket connection may be closed with custom close codes:

- **4001**: Missing `device_id` parameter
- **4002**: Invalid or inactive `device_id`
- **4003**: Conversation not found
- **4004**: Access denied (conversation doesn't belong to this device)

### Message Errors

**Error response:**
```json
{
  "type": "error",
  "message": "Message content cannot be empty"
}
```

## Implementation Example (JavaScript)

```javascript
// Connect to WebSocket
const conversationId = 123;
const deviceId = 'abc123xyz';
const ws = new WebSocket(`wss://hodi.co.ke/ws/mobile/chat/${conversationId}/?device_id=${deviceId}`);

// Connection opened
ws.onopen = function(event) {
  console.log('WebSocket connected');
};

// Listen for messages
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'connection_established':
      console.log('Connection established:', data);
      break;
      
    case 'chat_message':
      console.log('New message:', data.message);
      // Display message in UI
      displayMessage(data.message);
      break;
      
    case 'message_status_update':
      console.log('Status update:', data);
      // Update message status in UI
      updateMessageStatus(data.message_id, data.status);
      break;
      
    case 'typing_indicator':
      console.log('User typing:', data);
      // Show typing indicator
      showTypingIndicator(data.device_id || data.user_id, data.is_typing);
      break;
      
    case 'error':
      console.error('Error:', data.message);
      break;
      
    default:
      console.log('Unknown message type:', data.type);
  }
};

// Send a message
function sendMessage(content) {
  ws.send(JSON.stringify({
    type: 'chat_message',
    content: content,
    message_type: 'text',
    is_urgent: false,
    metadata: {}
  }));
}

// Send typing indicator
function sendTypingIndicator(isTyping) {
  ws.send(JSON.stringify({
    type: 'typing_indicator',
    is_typing: isTyping
  }));
}

// Mark messages as read
function markAsRead(messageIds) {
  ws.send(JSON.stringify({
    type: 'read_receipt',
    message_ids: messageIds
  }));
}

// Connection closed
ws.onclose = function(event) {
  console.log('WebSocket closed:', event.code, event.reason);
  // Implement reconnection logic if needed
};

// Connection error
ws.onerror = function(error) {
  console.error('WebSocket error:', error);
};
```

## Implementation Example (Python)

```python
import asyncio
import websockets
import json

async def chat_websocket_client(conversation_id, device_id):
    uri = f"wss://hodi.co.ke/ws/mobile/chat/{conversation_id}/?device_id={device_id}"
    
    async with websockets.connect(uri) as websocket:
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'connection_established':
                print(f"Connected: {data}")
                
            elif data['type'] == 'chat_message':
                print(f"New message: {data['message']}")
                
            elif data['type'] == 'error':
                print(f"Error: {data['message']}")
        
        # Send a message
        await websocket.send(json.dumps({
            'type': 'chat_message',
            'content': 'Hello from Python!',
            'message_type': 'text',
            'is_urgent': False,
            'metadata': {}
        }))

# Run the client
asyncio.run(chat_websocket_client(123, 'abc123xyz'))
```

## Features

✅ **Real-time messaging**: Instant message delivery
✅ **Message status tracking**: Sent, delivered, read status
✅ **Typing indicators**: See when someone is typing
✅ **Read receipts**: Know when messages are read
✅ **User presence**: See when users join/leave
✅ **Media support**: Send images, files, etc.
✅ **Urgent messages**: Mark messages as urgent
✅ **Error handling**: Comprehensive error responses

## Security Considerations

1. **Device ID Validation**: Always validate `device_id` on the server side
2. **Conversation Access**: Users can only access conversations belonging to their device
3. **HTTPS/WSS**: Always use secure WebSocket (WSS) in production
4. **Rate Limiting**: Consider implementing rate limiting for WebSocket connections
5. **Connection Timeout**: Implement proper timeout and reconnection logic

## Integration with Existing REST API

The WebSocket endpoint works seamlessly with the existing REST API:

- Use REST API to start conversations, get conversation lists, etc.
- Use WebSocket for real-time messaging within active conversations
- Both can be used together for the best user experience

## Testing

You can test the WebSocket endpoint using:

1. **Browser Console**: Use the JavaScript example above
2. **WebSocket Client Tools**: 
   - Postman (WebSocket support)
   - wscat (command-line tool)
   - WebSocket King (Chrome extension)
3. **Python Script**: Use the Python example above

## Troubleshooting

### Connection Fails
- Verify `device_id` is valid and active
- Check that `conversation_id` exists
- Ensure the conversation belongs to the device
- Check network connectivity and firewall settings

### Messages Not Received
- Verify WebSocket connection is still active
- Check that you're connected to the correct conversation
- Ensure the message format is correct JSON

### Status Updates Not Working
- Verify `message_id` exists in the conversation
- Check that status values are valid ('delivered' or 'read')

## Related Endpoints

- `POST /mobile/chat/start/` - Start a new conversation
- `GET /mobile/chat/list/` - List conversations
- `GET /mobile/chat/{id}/detail/` - Get conversation details
- `POST /mobile/chat/{id}/send-message/` - Send message via REST (fallback)

