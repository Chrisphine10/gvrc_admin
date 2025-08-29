"""
Base settings for Django project
"""

import os
import logging.config
from pathlib import Path
from dotenv import load_dotenv

# Import legacy helpers for backward compatibility
try:
    from helpers.util import *
except ImportError:
    pass

load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "TODO_SET_SECRET_KEY")
APP_DOMAIN = os.getenv("APP_DOMAIN", "http://localhost:8000")

# Debug mode
DEBUG = True

# Hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Google Maps API Configuration
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyBYKU1YgvaJwUYkFUqYkfwdPuOG5EvA_Bk")
GOOGLE_PLACES_API_KEY = GOOGLE_MAPS_API_KEY  # Same key works for both Maps and Places

# Application definition
INSTALLED_APPS = [
    # Admin styling
    "admin_gradient.apps.AdminGradientConfig",

    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "django_extensions",
    "channels",  # Django Channels

    # Local apps
    "apps.home",
    "apps.authentication.apps.AuthenticationConfig",
    "apps.api",
    "apps.common",
    "apps.facilities",
    'apps.core.apps.CoreConfig',
    "apps.health",
    "apps.geography",
    "apps.lookups",
    "apps.documents",
    "apps.analytics",
    "apps.music",
    "apps.mobile_sessions",
    "apps.chat",
    "apps.mobile",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.authentication.backends.AuthenticationErrorMiddleware",
]

ROOT_URLCONF = "core.urls"

# Templates
HOME_TEMPLATES = os.path.join(BASE_DIR, "apps", "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [HOME_TEMPLATES],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"  # Channels entry point

# Database (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "myproject_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Session storage
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_COOKIE_SECURE = False  # Change to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "sessionid"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "apps", "static"),
)

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default PK field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"
AUTH_USER_MODEL = "authentication.User"
AUTHENTICATION_BACKENDS = [
    "apps.authentication.backends.CustomUserBackend",
    "django.contrib.auth.backends.ModelBackend",  # fallback
]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@gvrc-admin.com"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "apps.authentication.backends.CustomTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# Swagger (drf-yasg)
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "LOGIN_URL": "/login/",
    "LOGOUT_URL": "/logout/",
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Token authentication for mobile apps. Format: Token <your_token>",
        },
    },
    "DOC_EXPANSION": "none",
    "PERSIST_AUTH": True,
}

# Channels config
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # In-memory (dev only)
        # For production, use Redis:
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

# Chat System Configuration
CHAT_SETTINGS = {
    "MAX_MESSAGE_LENGTH": 1000,
    "MAX_MEDIA_SIZE": 10 * 1024 * 1024,  # 10MB
    "MESSAGE_RETENTION_DAYS": 365,
    "AUTO_ASSIGN_LIMIT": 5,
    "TYPING_INDICATOR_TIMEOUT": 5,  # seconds
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "errors.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "myproject": {
            "handlers": ["file", "console", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Ensure logs directory exists
os.makedirs(BASE_DIR / "logs", exist_ok=True)
