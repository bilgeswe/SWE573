from django.apps import AppConfig

class ForumConfig(AppConfig):
    name = 'forum'

    def ready(self):
        import forum.signals  # Import the signals here

