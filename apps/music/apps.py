# -*- encoding: utf-8 -*-
"""
Music app configuration
"""

from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.music'
    verbose_name = 'Music Management'
