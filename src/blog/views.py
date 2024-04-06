from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostCreateSerializer
from .permissions import IsBlogPostAuthorOrReadOnly


class BlogPostCreateView(generics.CreateAPIView):
    serializer_class = BlogPostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogPostList(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated,]

class BlogPostDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated, IsBlogPostAuthorOrReadOnly]

