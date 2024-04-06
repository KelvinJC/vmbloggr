
from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.BlogPostList.as_view(), name='blog-posts-list'),
    path('blogs/<int:pk>/', views.BlogPostDetails.as_view(), name='blog-post-detail'),
    path('blogs/blog/', views.BlogPostCreateView.as_view(), name='blog-post-create'),
]
