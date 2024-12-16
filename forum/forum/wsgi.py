
import os

from django.core.wsgi import get_wsgi_application

# Set Django settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum.settings')

# Initialize WSGI application
application = get_wsgi_application()
