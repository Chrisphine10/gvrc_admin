# -*- encoding: utf-8 -*-
"""
Emergency Chat System App Configuration
"""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'
    verbose_name = 'Emergency Chat System'
    
    def ready(self):
        """App initialization when Django starts"""
        try:
            import apps.chat.signals  # noqa
        except ImportError:
            pass
