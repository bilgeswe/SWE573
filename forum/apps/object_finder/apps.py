from django.apps import AppConfig


class ObjectFinderConfig(AppConfig):
    """Configuration class for the object_finder app"""
    default_auto_field = 'django.db.models.BigAutoField'       # Specifies the primary key type
    name = 'apps.object_finder'                                # The Python package name of the app
