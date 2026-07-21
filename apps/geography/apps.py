# -*- encoding: utf-8 -*-
"""
Geography app configuration
"""

from django.apps import AppConfig


class GeographyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.geography'
    verbose_name = 'Geographic Divisions'