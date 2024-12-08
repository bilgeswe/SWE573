from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Image(models.Model):
    image = models.ImageField(upload_to='images', default='default.jpg')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, default=1)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_name = models.CharField(max_length=255, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        "Post", related_name='comments', on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        if self.author:
            return f'Comment by {self.author} on {self.post.title}'
        else:
            return f'Anonymous comment on {self.post.title}'

    objects = models.Manager()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    tag_id = models.CharField(max_length=100, unique=True)

    objects = models.Manager()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content_delta = models.JSONField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    attributes = JSONField(default=dict)

    objects = models.Manager()
