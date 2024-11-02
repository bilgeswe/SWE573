from django.urls import path                        # Function to define URL patterns
from .views import register, user_login             # Import the view functions for registration and login

# Define URL patterns for the application
urlpatterns = [
    path('register/', register, name='register'),   # URL pattern for the registration view
    path('login/', user_login, name='login'),       # URL pattern for the login view
]
