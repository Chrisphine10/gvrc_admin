# -*- encoding: utf-8 -*-
"""
Gunicorn configuration for production deployment
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5005"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "gvrc_admin_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/gvrc_admin.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment if using HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Preload app for better performance
preload_app = True

# Capture output
capture_output = True
enable_stdio_inheritance = True

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=core.settings.prod',
]
