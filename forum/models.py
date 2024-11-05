from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)             # Link to the User model
    bio = models.TextField(blank=True)                                      # Optional bio field
    profession = models.CharField(max_length=100, blank=True)               # Optional profession field
    top_contributor = models.BooleanField(default=False)                    # Status indicator

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name                                                    # Return a string representation for easier debugging

class ObjectPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')                                # Related name for easy reverse lookup
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='posts')   # Link to UserProfile
    created_at = models.DateTimeField(default=timezone.now)                                 # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)                                        # Timestamp when updated

    def __str__(self):
        return self.title                                                                   # Return title for easier debugging
