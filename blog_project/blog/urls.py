from django.urls import path
from . import views
from .views import *
from .views import BlogPostListCreateAPIView, BlogPostRetrieveUpdateDestroyAPIView
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from .views import BlogPostListAPIView, BlogPostDetailAPIView





urlpatterns = [
#     blogs
    path("", views.blogs, name="blogs"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("delete_blog_post/<str:slug>/", views.Delete_Blog_Post, name="delete_blog_post"),
    # path("search/", views.search, name="search"),
    path('api/posts/<int:pk>/', UpdatePostAPI.as_view(), name='update_post_api'),
    path('api/posts/', BlogPostListCreateAPIView.as_view(), name='blogpost-list-create'),
    path('api/posts/<int:pk>/', BlogPostRetrieveUpdateDestroyAPIView.as_view(), name='blogpost-retrieve-update-destroy'),
    path('api/token/', ObtainJSONWebToken.as_view(), name='api-token-obtain'),
    path('api/token/refresh/', RefreshJSONWebToken.as_view(), name='api-token-refresh'),
    path('api/token/verify/', VerifyJSONWebToken.as_view(), name='api-token-verify'),
    # path('delete/<slug:slug>/', delete_blog_post, name='delete_blog_post'),

    


    # path('blog-posts/', BlogPostListAPIView.as_view(), name='blog_post_list'),
    # path('blog-posts/<int:pk>/', BlogPostDetailAPIView.as_view(), name='blog_post_detail'),





    
#     profile
    # path("profile/", views.Profile, name="profile"),
    # path("edit_profile/", views.edit_profile, name="edit_profile"),
    # path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    
#    user authentication
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]