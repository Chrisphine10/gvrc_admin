import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')   # where collectstatic will copy files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Trust the X-Forwarded-Proto header from the ELB
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Force HTTPS redirects
SECURE_SSL_REDIRECT = True

# Secure cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
