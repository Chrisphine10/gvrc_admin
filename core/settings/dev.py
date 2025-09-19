# -*- encoding: utf-8 -*-
"""
Development settings
"""

from .base import *

DEBUG = True

# HOSTs List
ALLOWED_HOSTS = ["127.0.0.1", "hodi.co.ke", "localhost", APP_DOMAIN, ".deploypro.dev", ".ngrok-free.app", "a3f602af5f2d.ngrok-free.app", "54.198.204.150", "172.31.47.58"]

# Add here your deployment HOSTS
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5085",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5085",
    f"http://{APP_DOMAIN}",
    f"https://{APP_DOMAIN}",
    "https://*.deploypro.dev",
    "https://*.ngrok-free.app",
    "http://a3f602af5f2d.ngrok-free.app",
    "https://a3f602af5f2d.ngrok-free.app",
    "http://54.198.204.150:8000",
    "http://172.31.47.58:8000",
    "https://hodi.co.ke",    
]

# Database
DB_ENGINE = os.getenv("DB_ENGINE", None)
DB_USERNAME = os.getenv("DB_USERNAME", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_PORT = os.getenv("DB_PORT", None)
DB_NAME = os.getenv("DB_NAME", None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    # Clean up DB_ENGINE to prevent double prefixing
    if DB_ENGINE.startswith("django.db.backends."):
        # Remove the prefix if it's already there
        clean_engine = DB_ENGINE.replace("django.db.backends.", "")
    else:
        clean_engine = DB_ENGINE
    
    # Build the correct engine path
    engine = f"django.db.backends.{clean_engine}"
    
    DATABASES = {
        "default": {
            "ENGINE": engine,
            "NAME": DB_NAME,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASS,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }

# Logging configuration for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'auth_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/authentication.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'apps.home': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'apps.authentication': {
            'handlers': ['console', 'file', 'auth_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file', 'auth_file'],
            'level': 'WARNING',
        },
    },
}