import os
from django.core.asgi import get_asgi_application

# Set Django settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum.settings')

# Initialize ASGI application
application = get_asgi_application()
