# Import required models and admin module
from .models import Tag, Post
from django.contrib import admin


# Register models for admin interface
admin.site.register(Tag)  # Enable Tag model management in admin
admin.site.register(Post) # Enable Post model management in admin
