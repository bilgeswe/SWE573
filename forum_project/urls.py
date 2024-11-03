from django.contrib import admin            # Import the admin module to access Django's built-in admin site
from django.urls import path, include       # Import functions to define URL patterns and include other URL configurations
from django.shortcuts import redirect       # Import redirect to use for the root URL

urlpatterns = [                             # Define the URL patterns for the project
    path('admin/', admin.site.urls),        # URL pattern for the Django admin site, accessible at /admin/
    path('', lambda request: redirect('register/')),  # Redirect root URL to 'register' page
    path('', include('forum.urls')),        # Route to include URLs from 'forum' app
]