from django.db import models

class UserProfile(models.Model):
    bio = models.TextField()
    profession = models.CharField(max_length=100)
    top_contributor = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=50)

class ObjectPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)  # Use ManyToMany for multiple tags
