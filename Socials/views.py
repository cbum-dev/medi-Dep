from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from Accounts.permissions import IsOwner
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Blog,BlogLike
from .serializer import BlogCreateSerializer,BlogSerializer,BlogLikeSerializer,BlogUpdateSerializer,FullBlogSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,BasePermission
class BlogCreate(generics.CreateAPIView):
    serializer_class = BlogCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

class BlogUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()                                                                                           
    serializer_class = BlogUpdateSerializer
    permission_classes = [IsAuthenticated,IsOwner]

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write permissions are only allowed to the owner of the blog.
        return obj.author == request.user

class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Set the author of the blog post to the current user
        serializer.save(author=self.request.user)

class BlogLikeViewSet(viewsets.ModelViewSet):
    queryset = BlogLike.objects.all()
    serializer_class = BlogLikeSerializer


class FullBlog(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = FullBlogSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BlogLike(generics.CreateAPIView):
    serializer_class = BlogLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user from the JWT
        serializer.save(user=self.request.user, blog_id=self.kwargs['blog_id'])