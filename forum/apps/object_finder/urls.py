# Import required Django modules and views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),                                                        # Homepage/index view
    path('form', views.form, name='form'),                                                      # Form for creating new posts
    path('profile/<int:user_id>/', views.profile_view, name='profile'),                         # User profile view
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),     # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),                            # Logout functionality
    path('signup/', views.signup_view, name='signup'),                                          # User registration
    path('search/', views.search_posts, name='search_posts'),                                   # Search posts functionality
    path('view_post/<int:post_id>', views.view_post, name='view_post'),                         # View single post
    path('post/<int:post_id>/<int:comment_id>/update_is_solved/',
         views.update_is_solved, name='update_is_solved'),                                      # Update solved status of comments
]
