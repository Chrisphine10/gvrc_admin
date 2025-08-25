# 🚨 Emergency Chat System - GVRC Admin

A comprehensive real-time emergency chat system built with Django + DRF + Channels, designed for mobile users to communicate with admin staff in real-time.

## 🏗️ System Architecture

### Core Components
- **Django 4.2+** - Web framework
- **Django REST Framework** - API endpoints
- **Django Channels** - Real-time WebSocket communication
- **PostgreSQL** - Database backend
- **Redis** - Channel layer backend (production)
- **Swagger/OpenAPI** - API documentation

### System Flow
```
Mobile User → WebSocket/REST API → Django Channels → Admin Dashboard
     ↓              ↓                    ↓              ↓
  Session ID    Message Store      Real-time Sync   Live Chat
```

## 🚀 Features

### Mobile Users (Anonymous)
- ✅ Start conversations without registration
- ✅ Send text, image, voice, and file messages
- ✅ Real-time message delivery
- ✅ Message status tracking (sent/delivered/read)
- ✅ Location sharing capabilities
- ✅ Urgent message flagging

### Admin Staff
- ✅ Real-time conversation monitoring
- ✅ Auto-assignment of conversations
- ✅ Live chat interface
- ✅ Message history and search
- ✅ Conversation status management
- ✅ Priority-based conversation handling
- ✅ Notification system

### System Features
- ✅ Scalable WebSocket architecture
- ✅ REST API for mobile apps
- ✅ Comprehensive admin interface
- ✅ Message encryption and security
- ✅ Multi-media support
- ✅ Real-time notifications

## 📱 API Endpoints

### Mobile API (`/chat/mobile/`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/conversations/start/` | POST | Start/retrieve conversation |
| `/conversations/list/` | GET | List user conversations |
| `/conversations/{id}/detail/` | GET | Get conversation details |
| `/conversations/{id}/send-message/` | POST | Send message |
| `/messages/{id}/status/` | PUT | Update message status |

### Admin API (`/chat/admin/`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/conversations/list/` | GET | List all conversations |
| `/conversations/{id}/detail/` | GET | Get conversation details |
| `/conversations/{id}/assign/` | POST | Assign conversation |
| `/conversations/{id}/send-message/` | POST | Send admin message |
| `/conversations/{id}/status/` | PUT | Update conversation status |
| `/conversations/{id}/resolve/` | POST | Mark as resolved |
| `/conversations/stats/` | GET | Get conversation statistics |
| `/notifications/unread/` | GET | Get unread notifications |

## 🔌 WebSocket Endpoints

### Chat WebSocket
```
ws://yourdomain.com/ws/chat/{conversation_id}/
```

**Message Types:**
- `chat_message` - Send/receive messages
- `message_status` - Update delivery status
- `typing_indicator` - Show typing status
- `read_receipt` - Mark messages as read

### Notification WebSocket
```
ws://yourdomain.com/ws/notifications/
```

**Message Types:**
- `notification_update` - New notification
- `conversation_assigned` - Assignment notification
- `urgent_message` - Urgent message alert

## 🗄️ Database Models

### Conversation
- Links mobile session to admin
- Tracks status, priority, and metadata
- Auto-assignment logic
- Unread message counts

### Message
- Text, image, voice, file support
- Delivery status tracking
- Metadata storage
- Urgent flagging

### ChatNotification
- Admin notification system
- Multiple notification types
- Read/unread tracking

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations chat
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
# HTTP Server
python manage.py runserver

# ASGI Server (for WebSockets)
python manage.py runserver --noreload
```

## 🔧 Configuration

### Django Settings
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    "channels",
    "apps.chat",
]

# Django Channels Configuration
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"  # Development
        # "BACKEND": "channels_redis.core.RedisChannelLayer",  # Production
    },
}
```

### Environment Variables
```bash
# Required
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@host:port/db

# Optional
REDIS_URL=redis://localhost:6379/0
CHAT_MAX_MESSAGE_LENGTH=1000
CHAT_MAX_MEDIA_SIZE=10485760
```

## 🚀 Production Deployment

### 1. Redis Setup
```bash
# Install Redis
sudo apt-get install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
# Set bind 127.0.0.1 and requirepass

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis
```

### 2. Channel Layer Configuration
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
            "password": "your_redis_password",
        },
    },
}
```

### 3. Nginx Configuration
```nginx
# WebSocket support
location /ws/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 4. Gunicorn + Uvicorn
```bash
# Install
pip install gunicorn uvicorn

# Run
gunicorn core.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
```

## 📱 Mobile App Integration

### Starting a Conversation
```javascript
// Connect to WebSocket
const ws = new WebSocket(`ws://yourdomain.com/ws/chat/${conversationId}/`);

// Send message
ws.send(JSON.stringify({
    type: 'chat_message',
    content: 'Hello, I need help!',
    message_type: 'text',
    is_urgent: false
}));

// Listen for messages
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'chat_message') {
        displayMessage(data.message);
    }
};
```

### REST API Usage
```javascript
// Start conversation
const response = await fetch('/chat/mobile/conversations/start/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        device_id: 'device-uuid-123',
        subject: 'Emergency assistance needed'
    })
});

// Send message via REST
const messageResponse = await fetch(`/chat/mobile/conversations/${conversationId}/send-message/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        content: 'I am in danger!',
        is_urgent: true
    })
});
```

## 🔒 Security Features

### Authentication & Authorization
- Mobile users: Anonymous (device ID based)
- Admin users: Django authentication
- Staff-only admin endpoints
- Session-based security

### Data Protection
- HTTPS enforcement
- Message sanitization
- File upload restrictions
- Rate limiting (configurable)

### Privacy
- No persistent user data for mobile users
- Admin access logging
- Message encryption (configurable)
- GDPR compliance features

## 📊 Monitoring & Analytics

### Built-in Metrics
- Conversation counts by status
- Message delivery rates
- Admin response times
- System performance metrics

### Logging
```python
# Chat system logs
import logging
logger = logging.getLogger('chat')

logger.info(f"New conversation started: {conversation_id}")
logger.warning(f"Admin assignment failed: {conversation_id}")
logger.error(f"Message delivery failed: {message_id}")
```

## 🧪 Testing

### Unit Tests
```bash
python manage.py test apps.chat.tests
```

### API Testing
```bash
# Test mobile endpoints
curl -X POST http://localhost:8000/chat/mobile/conversations/start/ \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device-123", "subject": "Test"}'

# Test admin endpoints (with authentication)
curl -X GET http://localhost:8000/chat/admin/conversations/list/ \
  -H "Authorization: Token your_token_here"
```

### WebSocket Testing
```bash
# Install wscat
npm install -g wscat

# Test WebSocket connection
wscat -c ws://localhost:8000/ws/chat/1/
```

## 🔄 Future Enhancements

### Planned Features
- [ ] AI-powered message triage
- [ ] Multi-language support
- [ ] Voice-to-text conversion
- [ ] Advanced analytics dashboard
- [ ] Mobile push notifications
- [ ] Integration with external services

### Scalability Improvements
- [ ] Message queuing (Celery)
- [ ] Load balancing
- [ ] Microservices architecture
- [ ] CDN integration
- [ ] Database sharding

## 📚 API Documentation

### Swagger UI
Access the interactive API documentation at:
```
http://yourdomain.com/swagger/
```

### ReDoc
Alternative documentation format:
```
http://yourdomain.com/redoc/
```

## 🆘 Support & Troubleshooting

### Common Issues

#### WebSocket Connection Failed
```bash
# Check ASGI configuration
python manage.py check

# Verify channel layers
python manage.py shell
>>> from channels.layers import get_channel_layer
>>> channel_layer = get_channel_layer()
```

#### Database Errors
```bash
# Reset migrations
python manage.py migrate chat zero
python manage.py makemigrations chat
python manage.py migrate
```

#### Redis Connection Issues
```bash
# Test Redis connection
redis-cli ping

# Check Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'chat': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Contact

For support or questions about the Emergency Chat System:
- Email: admin@hodi.ke
- Project: [GitHub Repository](https://github.com/your-org/gvrc_dmin)

---

**Built with ❤️ for GVRC Emergency Response Team**
