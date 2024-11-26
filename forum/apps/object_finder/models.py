from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField(upload_to='images', default='default.jpg')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, default=1)


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'


class Tag(models.Model):
    name = models.CharField(max_length=100)
    tag_id = models.CharField(max_length=100, unique=True)

    objects = models.Manager()


class AttributeName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"


class AttributeValue(models.Model):
    attribute_name = models.ForeignKey(
        AttributeName, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ('attribute_name', 'value')

    def __str__(self):
        return f"{self.attribute_name.name}: {self.value}"

    objects = models.Manager()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content_delta = models.JSONField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    attributes = models.ManyToManyField(AttributeValue, blank=True)

    def __str__(self):
        return self.title
