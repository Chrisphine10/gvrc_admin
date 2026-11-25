# -*- encoding: utf-8 -*-
"""
Test settings.

The test suite must never depend on what a developer's .env points at. The
local .env used to aim dev settings at an AWS RDS host that no longer resolves,
so the whole suite errored before a single test ran. Tests now always run on a
throwaway SQLite database, with no network SMS and fast password hashing.
"""

from .dev import *  # noqa: F401,F403

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "hodi-tests",
    }
}

MAILERS = {"default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend"}}

# The suite must never text a real phone, whatever .env says.
SMS_NETWORK_ENABLED = False
SMS_SEND_IN_BACKGROUND = False

# The debug toolbar is only added when DEBUG is on in dev.py; make sure a
# DJANGO_DEBUG=true in the shell cannot drag it into the test run.
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]
MIDDLEWARE = [m for m in MIDDLEWARE if "debug_toolbar" not in m]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"null": {"class": "logging.NullHandler"}},
    "root": {"handlers": ["null"], "level": "CRITICAL"},
}
