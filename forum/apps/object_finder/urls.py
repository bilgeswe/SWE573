from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('form', views.form, name='form'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search_posts, name='search_posts'),
    path('view_post/<int:post_id>', views.view_post, name='view_post')
]
