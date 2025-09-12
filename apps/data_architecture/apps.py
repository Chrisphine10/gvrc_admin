from django.apps import AppConfig


class DataArchitectureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_architecture'
    verbose_name = 'Data Architecture'
    
    def ready(self):
        """Initialize data architecture components when app is ready"""
        from . import signals  # Import signals to register them

