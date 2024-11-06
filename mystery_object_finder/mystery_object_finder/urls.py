from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),   # Admin interface URLs
    path('', include('forum.urls')),   # Include your forum URLs
]
