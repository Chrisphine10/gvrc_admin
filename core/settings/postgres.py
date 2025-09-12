"""
PostgreSQL-specific settings for GVRC Admin
"""
from .base import *

# Override database configuration for PostgreSQL

# Database configuration for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gvrc_admin_postgres',
        'USER': 'gvrc_user',
        'PASSWORD': 'gvrc_password',  # No password for local development
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {},
    }
}

# PostgreSQL-specific optimizations
DATABASES['default']['CONN_MAX_AGE'] = 60

# Enable PostgreSQL-specific features
USE_TZ = True
TIME_ZONE = 'Africa/Nairobi'

# Ensure we have the required settings
SECRET_KEY = 'your-secret-key-here'  # This should be set properly
DEBUG = True
ALLOWED_HOSTS = ['*']

# Logging configuration for PostgreSQL
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/postgres_migration.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
            'propagate': False,
        },
        'apps.data_architecture': {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
            'propagate': False,
        },
    },
}

# Ensure we're using PostgreSQL-specific features
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Enable PostgreSQL JSON field support
USE_JSONFIELD = True

print("🐘 PostgreSQL settings loaded successfully!")
