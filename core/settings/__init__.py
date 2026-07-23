# -*- encoding: utf-8 -*-
"""
Selects the settings module for anything that imports ``core.settings``.

This mattered more than it looks. Gunicorn is launched with
DJANGO_SETTINGS_MODULE=core.settings.prod, but manage.py falls back to plain
``core.settings`` - which used to be an unconditional ``from .dev import *``.
So on the production host the web workers ran prod settings while every
management command (migrate, collectstatic, shell, any cron job) quietly ran
dev settings.

The dangerous part was the database. prod.py points SQLite at
``BASE_DIR / "db.sqlite3"``; dev.py points it at the relative ``"db.sqlite3"``.
Run from /var/www/hodi they happen to be the same file, so nobody noticed. Run
a migration from any other working directory and Django creates a brand new
empty database and migrates that instead - succeeding loudly while touching
nothing real.

Set DJANGO_ENV=prod on the server so management commands agree with the web
workers. The default stays dev, so local development is unchanged.
"""

import os

_env = os.getenv('DJANGO_ENV', 'dev').strip().lower()

if _env in ('prod', 'production'):
    from .prod import *  # noqa: F401,F403
elif _env in ('postgres', 'pg'):
    from .postgres import *  # noqa: F401,F403
else:
    from .dev import *  # noqa: F401,F403
