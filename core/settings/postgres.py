from .base import *
DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "hodi.co.ke", "localhost", APP_DOMAIN, ".deploypro.dev", ".ngrok-free.app", "a3f602af5f2d.ngrok-free.app", "54.198.204.150", "172.31.47.58"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://localhost:5085", "http://127.0.0.1:8000", "http://127.0.0.1:5085", f"http://{APP_DOMAIN}", f"https://{APP_DOMAIN}", "https://*.deploypro.dev", "https://*.ngrok-free.app", "http://a3f602af5f2d.ngrok-free.app", "https://a3f602af5f2d.ngrok-free.app", "http://54.198.204.150:8000", "http://172.31.47.58:8000", "https://hodi.co.ke"]
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "hodi_db", "USER": "postgres", "PASSWORD": "postgres123#", "HOST": "hodi-db.cu7284ec0spr.us-east-1.rds.amazonaws.com", "PORT": "5432", "OPTIONS": {"connect_timeout": 60}}}
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
LOGGING = {'version': 1, 'disable_existing_loggers': False, 'formatters': {'verbose': {'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 'style': '{'}, 'simple': {'format': '{levelname} {message}', 'style': '{'}}, 'handlers': {'file': {'level': 'INFO', 'class': 'logging.FileHandler', 'filename': os.path.join(BASE_DIR, 'logs', 'django.log'), 'formatter': 'verbose'}, 'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'simple'}}, 'root': {'handlers': ['console', 'file'], 'level': 'INFO'}, 'loggers': {'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False}, 'apps': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False}}}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@hodi.co.ke')
CONN_MAX_AGE = 60
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
