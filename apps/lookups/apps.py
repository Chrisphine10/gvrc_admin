# -*- encoding: utf-8 -*-
"""
Lookups app configuration
"""

from django.apps import AppConfig


class LookupsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lookups'
    verbose_name = 'Master Data / Lookups'