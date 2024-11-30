from .models import Tag, AttributeName, AttributeValue, Post
from django.contrib import admin


admin.site.register(Tag)
admin.site.register(AttributeName)
admin.site.register(AttributeValue)
admin.site.register(Post)
