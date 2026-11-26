/**
 * Real-time notification system for chat conversations
 * Handles WebSocket connections and AJAX updates for unread messages
 */

class NotificationManager {
    constructor() {
        this.websocket = null;
        this.updateInterval = null;
        this.isConnected = false;
        this.retryCount = 0;
        this.maxRetries = 5;
        this.retryDelay = 3000; // 3 seconds
        this.everConnected = false;
        // Production runs plain WSGI (no /ws/ endpoint). After the first failed
        // attempt we remember that for a while and only poll, instead of trying
        // (and logging errors) five times on every page load.
        this.WS_SKIP_KEY = 'hodiWsUnavailableUntil';
        this.WS_SKIP_MS = 10 * 60 * 1000;
        
        this.init();
    }

    init() {
        this.setupWebSocket();
        this.setupPeriodicUpdate();
        this.setupEventListeners();
    }

    wsKnownUnavailable() {
        try {
            return Number(sessionStorage.getItem(this.WS_SKIP_KEY) || 0) > Date.now();
        } catch (e) {
            return false;
        }
    }

    markWsUnavailable() {
        try {
            sessionStorage.setItem(this.WS_SKIP_KEY, String(Date.now() + this.WS_SKIP_MS));
        } catch (e) { /* private mode: just poll this time */ }
    }

    setupWebSocket() {
        if (this.wsKnownUnavailable()) {
            return; // polling (set up in init) covers it
        }
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                this.isConnected = true;
                this.everConnected = true;
                this.retryCount = 0;
                try { sessionStorage.removeItem(this.WS_SKIP_KEY); } catch (e) { /* ignore */ }
            };
            
            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleWebSocketMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            this.websocket.onclose = () => {
                this.isConnected = false;
                if (!this.everConnected) {
                    // The server has no WebSocket endpoint: poll quietly.
                    this.markWsUnavailable();
                    return;
                }
                this.scheduleReconnect();
            };
            
            this.websocket.onerror = () => {
                this.isConnected = false;
            };
        } catch (error) {
            this.markWsUnavailable();
        }
    }

    scheduleReconnect() {
        if (this.retryCount < this.maxRetries) {
            this.retryCount++;
            setTimeout(() => {
                this.setupWebSocket();
            }, this.retryDelay);
        } else {
            this.markWsUnavailable(); // polling is already running
        }
    }

    setupPeriodicUpdate() {
        // One 30-second poll for when the WebSocket is not connected. Guarded so
        // repeated fallbacks cannot stack several timers.
        if (this.updateInterval) {
            return;
        }
        this.updateInterval = setInterval(() => {
            if (!this.isConnected) {
                this.updateNotifications();
            }
        }, 30000);
    }

    setupEventListeners() {
        // Update notifications when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.updateNotifications();
            }
        });

        // Update notifications when user focuses on the window
        window.addEventListener('focus', () => {
            this.updateNotifications();
        });

        // Handle notification clicks
        document.addEventListener('click', (event) => {
            if (event.target.closest('.notification-item')) {
                const conversationId = event.target.closest('.notification-item').dataset.conversationId;
                this.markConversationAsRead(conversationId);
            }
        });
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'new_message':
                this.handleNewMessage(data);
                break;
            case 'conversation_updated':
                this.handleConversationUpdate(data);
                break;
            case 'notification_update':
                this.updateNotifications();
                break;
            default:
                console.log('Unknown WebSocket message type:', data.type);
        }
    }

    handleNewMessage(data) {
        console.log('New message received:', data);
        this.updateNotifications();
        this.showNotification(data);
    }

    handleConversationUpdate(data) {
        console.log('Conversation updated:', data);
        this.updateNotifications();
    }

    async updateNotifications() {
        try {
            const response = await fetch('/api/chat/admin/notifications/unread-conversations/', {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });

            if (response.ok) {
                const data = await response.json();
                this.updateNotificationUI(data);
            } else {
                console.error('Failed to fetch notifications:', response.status);
            }
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    }

    updateNotificationUI(data) {
        const { unread_conversations, total_unread_count, unread_conversations_count } = data;
        
        // Update notification badge
        this.updateNotificationBadge(total_unread_count);
        
        // Update notification count text
        this.updateNotificationCount(total_unread_count);
        
        // Update notification list
        this.updateNotificationList(unread_conversations);
    }

    updateNotificationBadge(count) {
        const badge = document.getElementById('notification-badge');
        if (count > 0) {
            if (badge) {
                badge.textContent = count;
                badge.style.display = 'inline';
            } else {
                // Create badge if it doesn't exist
                const bellIcon = document.querySelector('.nav-link i.ni-bell-55');
                if (bellIcon && bellIcon.parentElement) {
                    const newBadge = document.createElement('span');
                    newBadge.id = 'notification-badge';
                    newBadge.className = 'badge badge-danger badge-dot badge-dot-lg';
                    newBadge.textContent = count;
                    newBadge.style.display = 'inline';
                    bellIcon.parentElement.appendChild(newBadge);
                }
            }
        } else {
            if (badge) {
                badge.style.display = 'none';
            }
        }
    }

    updateNotificationCount(count) {
        const countElement = document.getElementById('notification-count');
        if (countElement) {
            countElement.textContent = count;
        }
        
        const headerText = document.querySelector('.px-3.py-3 h6');
        if (headerText) {
            if (count > 0) {
                headerText.innerHTML = `You have <strong class="text-primary">${count}</strong> unread message${count !== 1 ? 's' : ''}.`;
            } else {
                headerText.textContent = 'No unread messages.';
            }
        }
    }

    updateNotificationList(conversations) {
        const listContainer = document.getElementById('notification-list');
        if (!listContainer) return;

        if (conversations.length === 0) {
            listContainer.innerHTML = `
                <div class="list-group-item text-center text-muted py-4">
                    <i class="ni ni-chat-round ni-3x mb-2"></i>
                    <p class="mb-0">No unread conversations</p>
                </div>
            `;
            return;
        }

        const conversationsHTML = conversations.map(conv => {
            const priorityClass = this.getPriorityClass(conv.priority);
            const timeAgo = this.formatTimeAgo(conv.last_message_at);
            const subject = conv.subject ? conv.subject.substring(0, 30) + (conv.subject.length > 30 ? '...' : '') : 'Emergency Chat';
            const lastMessage = conv.last_message ? conv.last_message.substring(0, 50) + (conv.last_message.length > 50 ? '...' : '') : 'New conversation started';
            const deviceId = conv.device_id ? conv.device_id.substring(0, 15) + (conv.device_id.length > 15 ? '...' : '') : 'Unknown';
            
            return `
                <a href="${conv.conversation_url}" class="list-group-item list-group-item-action notification-item" data-conversation-id="${conv.conversation_id}">
                    <div class="row align-items-center">
                        <div class="col-auto">
                            <div class="avatar rounded-circle ${priorityClass} text-white d-flex align-items-center justify-content-center">
                                <i class="ni ni-chat-round"></i>
                            </div>
                        </div>
                        <div class="col ml--2">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h4 class="mb-0 text-sm">
                                        ${subject}
                                        ${conv.unread_count_admin > 1 ? `<span class="badge badge-primary badge-sm">${conv.unread_count_admin}</span>` : ''}
                                    </h4>
                                </div>
                                <div class="text-right text-muted">
                                    <small class="time-ago">${timeAgo}</small>
                                </div>
                            </div>
                            <p class="text-sm mb-0">${lastMessage}</p>
                            <div class="d-flex justify-content-between align-items-center mt-1">
                                <small class="text-muted">Device: ${deviceId}</small>
                                <small class="text-${this.getPriorityTextClass(conv.priority)}">${conv.priority_display}</small>
                            </div>
                        </div>
                    </div>
                </a>
            `;
        }).join('');

        listContainer.innerHTML = conversationsHTML;
    }

    getPriorityClass(priority) {
        switch (priority) {
            case 'urgent': return 'bg-gradient-danger';
            case 'high': return 'bg-gradient-warning';
            default: return 'bg-gradient-primary';
        }
    }

    getPriorityTextClass(priority) {
        switch (priority) {
            case 'urgent': return 'danger';
            case 'high': return 'warning';
            default: return 'info';
        }
    }

    formatTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        return `${Math.floor(diffInSeconds / 86400)}d ago`;
    }

    async markConversationAsRead(conversationId) {
        try {
            const response = await fetch(`/api/chat/admin/conversations/${conversationId}/messages/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });

            if (response.ok) {
                // Update notifications after marking as read
                setTimeout(() => this.updateNotifications(), 500);
            }
        } catch (error) {
            console.error('Error marking conversation as read:', error);
        }
    }

    showNotification(data) {
        // Show browser notification if permission is granted
        if (Notification.permission === 'granted') {
            const notification = new Notification(data.title || 'New Chat Message', {
                body: data.body || 'You have a new message',
                icon: '/static/assets/img/brand/hodi app logo.png',
                tag: 'chat-notification'
            });

            notification.onclick = () => {
                window.focus();
                if (data.conversation_id) {
                    window.location.href = `/chat/conversations/${data.conversation_id}/`;
                }
                notification.close();
            };

            // Auto-close after 5 seconds
            setTimeout(() => notification.close(), 5000);
        }
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    destroy() {
        if (this.websocket) {
            this.websocket.close();
        }
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Initialize notification manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.notificationManager = new NotificationManager();
    
    // Request notification permission
    window.notificationManager.requestNotificationPermission();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.notificationManager) {
        window.notificationManager.destroy();
    }
});
