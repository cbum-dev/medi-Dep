from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from Accounts.permissions import IsOwner
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Blog,BlogLike,ChatRoom,Message
from .serializer import BlogCreateSerializer,BlogSerializer,BlogLikeSerializer,BlogUpdateSerializer,FullBlogSerializer,ChatRoomSerializer,MessageCreateSerializer,MessageViewSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,BasePermission
class BlogCreate(generics.CreateAPIView):
    serializer_class = BlogCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write permissions are only allowed to the owner of the blog.
        return obj.author == request.user

class IsOwnerOrReadOnlyForComments(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write permissions are only allowed to the owner of the blog.
        return obj.user == request.user

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

from rest_framework import generics
from .models import HelpCenter, HelpCenterComments
from .serializer import HelpCenterSerializer, HelpCenterCommentSerializer,HelpCenterViewCreateSerializer,HelpCenterCommentCreateSerializer
from rest_framework.permissions import IsAuthenticated

class HelpCenterListCreateView(generics.ListCreateAPIView):
    queryset = HelpCenter.objects.all()
    serializer_class = HelpCenterViewCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # print(self.request.user.id)
        serializer.save(user=self.request.user)

class HelpCenterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HelpCenter.objects.all()
    serializer_class = HelpCenterSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnlyForComments]

class HelpCenterCommentListCreateView(generics.ListCreateAPIView):

    serializer_class = HelpCenterCommentCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        help_center_id = self.kwargs['help_center_id']
        try:
            help_center = HelpCenter.objects.get(prob_id=help_center_id)
            return HelpCenterComments.objects.filter(problem=help_center).order_by('-id')
        except HelpCenter.DoesNotExist:
            return HelpCenterComments.objects.none()

    def perform_create(self, serializer):
        help_center_id = self.kwargs['help_center_id']
        try:
            help_center = HelpCenter.objects.get(prob_id=help_center_id)
            serializer.save(user=self.request.user, problem=help_center)
        except HelpCenter.DoesNotExist:
            pass  # Handle the case where the specified HelpCenter does not exist


class HelpCenterCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HelpCenterComments.objects.all()
    serializer_class = HelpCenterCommentSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnlyForComments]


class ChatRoomList(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        chatroom_id = self.kwargs.get('chatroom_id')

        if chatroom_id:
            # If chatroom_id is provided, return only the messages for that chat room
            return Message.objects.filter(chat_room_id=chatroom_id).order_by('-id')
        else:
            # If no chatroom_id is provided, return all messages
            return Message.objects.all()

class MessageDetail(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chatroom_id = self.kwargs.get('chatroom_id')
        user = self.request.user
        chat_room = ChatRoom.objects.get(pk=chatroom_id)
        serializer.save(chat_room=chat_room, user=user)


class MessageDelete(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageViewSerializer
    permission_classes = [IsOwnerOrReadOnlyForComments]