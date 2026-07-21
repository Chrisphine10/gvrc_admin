/**
 * Professional Toast Notification Manager
 * Provides smooth, non-intrusive notifications with proper UX
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.toasts = new Map();
        this.init();
    }

    init() {
        // Create toast container if it doesn't exist
        if (!document.getElementById('toast-container-global')) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container-global';
            this.container.className = 'toast-container-global';
            this.container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 12px;
                max-width: 400px;
                pointer-events: none;
            `;
            document.body.appendChild(this.container);
        } else {
            this.container = document.getElementById('toast-container-global');
        }
    }

    /**
     * Show a toast notification
     * @param {string} message - Message to display
     * @param {string} type - Type: 'success', 'error', 'info', 'warning'
     * @param {number} duration - Duration in milliseconds (0 = persistent)
     */
    show(message, type = 'info', duration = 4000) {
        const toastId = 'toast-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
        
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast-notification toast-${type}`;
        
        // Icon mapping
        const icons = {
            success: '<i class="ni ni-check-bold"></i>',
            error: '<i class="ni ni-fat-remove"></i>',
            warning: '<i class="ni ni-notification-70"></i>',
            info: '<i class="ni ni-info"></i>'
        };

        // Color mapping
        const colors = {
            success: { bg: '#2dce89', border: '#28a745' },
            error: { bg: '#f5365c', border: '#dc3545' },
            warning: { bg: '#fb6340', border: '#ff9800' },
            info: { bg: '#5e72e4', border: '#4c63d2' }
        };

        const color = colors[type] || colors.info;
        const icon = icons[type] || icons.info;

        toast.style.cssText = `
            background: ${color.bg};
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            line-height: 1.5;
            border-left: 4px solid ${color.border};
            pointer-events: auto;
            transform: translateX(400px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            max-width: 100%;
            word-wrap: break-word;
        `;

        toast.innerHTML = `
            <div style="flex-shrink: 0; font-size: 20px;">${icon}</div>
            <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 500; margin-bottom: 4px;">${this.getTitle(type)}</div>
                <div style="opacity: 0.95; font-size: 13px;">${message}</div>
            </div>
            <button class="toast-close" style="
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0.8;
                transition: opacity 0.2s;
                flex-shrink: 0;
            " onclick="window.toastManager.remove('${toastId}')" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">
                ×
            </button>
        `;

        this.container.appendChild(toast);
        this.toasts.set(toastId, toast);

        // Animate in
        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
            toast.style.opacity = '1';
        });

        // Auto-remove if duration is set (0 means persistent)
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toastId);
            }, duration);
        } else {
            // For persistent toasts (duration = 0), ensure they stay visible
            // Store reference to prevent accidental removal
            toast.dataset.persistent = 'true';
        }

        return toastId;
    }

    /**
     * Remove a toast
     */
    remove(toastId) {
        const toast = this.toasts.get(toastId);
        if (!toast) return;

        toast.style.transform = 'translateX(400px)';
        toast.style.opacity = '0';

        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            this.toasts.delete(toastId);
        }, 300);
    }

    /**
     * Get title for toast type
     */
    getTitle(type) {
        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Information'
        };
        return titles[type] || 'Notification';
    }

    // Convenience methods
    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// Initialize global toast manager
if (typeof window !== 'undefined') {
    window.toastManager = new ToastManager();
}

