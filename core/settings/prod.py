# -*- encoding: utf-8 -*-
"""
Production settings
"""

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

# base.py falls back to a placeholder so local tools work without a .env.
# In production that would sign sessions and reset links with a key anyone can
# read in the repository, so refuse to start instead.
if not SECRET_KEY or SECRET_KEY == "TODO_SET_SECRET_KEY" or len(SECRET_KEY) < 32:
    raise ImproperlyConfigured("Set a long random SECRET_KEY in the environment (.env) for production.")

def _env_list(name):
    return [v.strip() for v in os.getenv(name, "").split(",") if v.strip()]


# HOSTs List. The server's .env ALLOWED_HOSTS is honoured (it used to be
# ignored here, so switching the server to these settings would have answered
# every request to hodi-admin.co.ke with 400 Bad Request).
ALLOWED_HOSTS = list(dict.fromkeys(
    [h for h in _env_list("ALLOWED_HOSTS") if h != "*"]
    + [APP_DOMAIN, "hodi-admin.co.ke", "www.hodi-admin.co.ke", "hodi.co.ke", "localhost", "127.0.0.1"]
))

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Add here your deployment HOSTS
#
# The entry after 34.226.180.10:8000 was missing its comma, so Python
# concatenated the next line onto it and the list actually contained
# "http://34.226.180.10http://hodi.co.ke". Two origins that were meant to be
# trusted were not, and a nonsense one was.
CSRF_TRUSTED_ORIGINS = [
    f"https://{APP_DOMAIN}",
    "https://hodi-admin.co.ke",
    "https://www.hodi-admin.co.ke",
    "https://hodi.co.ke",
    "https://*.deploypro.dev",
] + [o for o in _env_list("CSRF_TRUSTED_ORIGINS") if o.startswith("https://")]  # never trust plain http

# Database
DB_ENGINE = os.getenv("DB_ENGINE", None)
DB_USERNAME = os.getenv("DB_USERNAME", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_PORT = os.getenv("DB_PORT", None)
DB_NAME = os.getenv("DB_NAME", None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends." + DB_ENGINE,
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
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS. The site has been served over TLS for a while; these were still
# commented out, so the session and CSRF cookies were being set without the
# Secure flag and browsers were never told to refuse plaintext.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Not preloading. Preload is effectively irreversible - you cannot get a domain
# out of the browser list quickly - and it would commit every current and future
# subdomain of hodi-admin.co.ke to HTTPS. Turn it on deliberately, not as part
# of a security sweep.
SECURE_HSTS_PRELOAD = False

# SECURE_SSL_REDIRECT stays off on purpose. nginx already answers plain HTTP
# with a 301 to https, so Django would only be doing it a second time - and if
# the proxy ever stops sending X-Forwarded-Proto, Django would consider every
# request insecure and redirect it to itself forever, taking the site down.
# Redirect at the edge, where the protocol is actually known.
SECURE_SSL_REDIRECT = False

# Both are deliberate (see the two comments above): nginx does the HTTPS
# redirect, and HSTS preload is a one-way door. Silenced so that
# `check --deploy` reports only real problems.
SILENCED_SYSTEM_CHECKS = ["security.W008", "security.W021"]

# Static files configuration for production
# STATICFILES_STORAGE was removed in Django 5.1; STORAGES replaces it.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "core.storage.HodiStaticFilesStorage"},
}

# Logging configuration
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
        # Rotating: the old plain FileHandler let logs/ grow past 300 MB.
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('DJANGO_LOG_FILE', str(BASE_DIR / 'logs' / 'django.log')),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gvrc_admin': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache configuration (Redis recommended for production)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# For production with Redis, uncomment and configure:
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

# Email configuration for production
# No mail account configured on the server (EMAIL_HOST empty, as on
# hodi-admin.co.ke in Nov 2026): discard mail instead of failing on every send.
# The console backend would print password reset links into the service log.
# Reset links also go by SMS, so resets still work.
MAILERS = smtp_mailers_from_env() if os.getenv("EMAIL_HOST", "").strip() else {
    "default": {"BACKEND": "django.core.mail.backends.dummy.EmailBackend"},
}
if not os.getenv("EMAIL_HOST", "").strip():
    # Deliberate while no mail account exists; `manage.py check_data` keeps
    # reporting it as a warning so it is not forgotten.
    SILENCED_SYSTEM_CHECKS = SILENCED_SYSTEM_CHECKS + ["mail.E001"]
# The SMTP account usually only sends as itself, so default to it.
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL') or os.getenv('EMAIL_HOST_USER') or 'noreply@hodi.co.ke'

# Performance optimizations
CONN_MAX_AGE = 60  # Database connection pooling
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Security middleware settings
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Trusted proxy settings (for Nginx)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')