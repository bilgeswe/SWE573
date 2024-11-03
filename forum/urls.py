from django.urls import path                                 # Function to define URL patterns
from .views import register, user_login, home, create_object_post  # Import the view functions for registration, login, and creating a post
                                                            # Define URL patterns for the application
urlpatterns = [
    path('', home, name='home'),                            # The default home page
    path('register/', register, name='register'),           # URL pattern for the registration view
    path('login/', user_login, name='login'),               # URL pattern for the login view
    path('create-post/', create_object_post, name='create_post'),  # URL pattern for the create post view
]
