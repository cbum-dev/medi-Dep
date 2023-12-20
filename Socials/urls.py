from django.urls import path,include
from .views import BlogCreate,BlogView,FullBlog,BlogLike
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()
router.register(r'blogs', BlogView, basename='blog')
urlpatterns = [
    path('blogs/create/',BlogCreate.as_view(),name="blogs") ,
    path('', include(router.urls)),
    path('full/<int:pk>/',FullBlog.as_view()),
    path('like/<int:blog_id>/',BlogLike.as_view()),

    # path('full/<int:pk>/',BlogDetailView.as_view())        #Feature
    path('help-center/', views.HelpCenterListCreateView.as_view(), name='help-center-list-create'),
    path('help-center/<int:pk>/', views.HelpCenterDetailView.as_view(), name='help-center-detail'),
    path('help-center/<int:help_center_id>/comments/', views.HelpCenterCommentListCreateView.as_view(), name='help-center-comment-list-create'),
    path('help-center/comments/<int:pk>/', views.HelpCenterCommentDetailView.as_view(), name='help-center-comment-detail'),     

    path('chat-rooms/', views.ChatRoomList.as_view(), name='chat-room-list'),
    path('messages/<int:chatroom_id>/', views.MessageList.as_view(), name='message-list'),
    path('messages-create/<int:chatroom_id>/', views.MessageDetail.as_view(), name='message-detail'),
    path('messages-del/<int:pk>/', views.MessageDelete.as_view(), name='message-delete'),
]