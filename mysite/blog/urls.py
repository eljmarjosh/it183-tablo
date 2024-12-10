from django.urls import path
from .views import blog_list, blog_detail, blog_delete, blog_create, blog_update
from . import views

urlpatterns = [
    path('', blog_list, name='home'),  # Home Page
    path('create/', blog_create, name='blog_create'),  # Create Blog
    path('<id>/update/', blog_update, name='blog_update'),  # Update Blog
    path('<id>/detail', blog_detail, name='blog_detail'),  # Blog Details
    path('<id>/delete/', blog_delete, name='blog_delete'),  # Delete Blog
    path('login/', views.user_login, name='login'),  # User Login
    path('logout/', views.user_logout, name='logout'),  # User Logout
    path('register/', views.register, name='register'),  # User Registration
]
