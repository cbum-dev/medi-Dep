from rest_framework import serializers
from .models import Blog,BlogLike
from Accounts.models import CustomUser



class CustomUserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email']
class BlogLikeSerializer(serializers.ModelSerializer):
    # user = CustomUserSerialiser()
    class Meta:
        model = BlogLike
        exclude = ['user','blog']
class BlogSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = CustomUserSerialiser()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'body', 'author','likes_count']

    def get_likes_count(self, obj):
        return obj.likes_count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check a condition (e.g., show_full_content parameter in the context)
        show_full_content = self.context.get('show_full_content', False)
        
        if not show_full_content:
            representation['body'] = ' '.join(representation['body'].split()[:50])
            
        return representation
class BlogCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = ['title','body']
class BlogUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = ['id','title','body']
class FullBlogSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = CustomUserSerialiser()
    class Meta:
        model = Blog
        fields = ['id','title','body','author','likes_count']
    def get_likes_count(self, obj):
        return obj.likes_count()


from rest_framework import serializers
from .models import HelpCenter, HelpCenterComments,ChatRoom,Message

class HelpCenterSerializer(serializers.ModelSerializer):
    user = CustomUserSerialiser()

    class Meta:
        model = HelpCenter
        fields = ['prob_id', 'user', 'problem', 'date']
        read_only_fields = ['prob_id', 'user', 'date']
class HelpCenterViewCreateSerializer(serializers.ModelSerializer):
    user = CustomUserSerialiser()
    class Meta:
        model = HelpCenter
        fields = ['prob_id', 'user', 'problem', 'date']
        extra_kwargs = {
            'user': {'read_only': True},
            'date': {'read_only': True},
        }
class HelpCenterCreateSerializer(serializers.ModelSerializer):
    # user = CustomUserSerialiser()
    class Meta:
        model = HelpCenter
        fields = ['prob_id', 'user', 'problem', 'date']
        extra_kwargs = {
            'user': {'read_only': True},
            'date': {'read_only': True},
        }
class HelpCenterCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerialiser()
    class Meta:
        model = HelpCenterComments
        fields = ['id','user', 'problem', 'comment','date']
        read_only_fields = ['user','date']
class HelpCenterCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpCenterComments
        fields = ['id','user', 'problem', 'comment','date']
        read_only_fields = ['user','date','problem']


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('id', 'name')

class MessageViewSerializer(serializers.ModelSerializer):
    user = CustomUserSerialiser()
    chat_room = ChatRoomSerializer()
    class Meta:
        model = Message
        fields = ('id', 'user', 'chat_room', 'content', 'timestamp')
class MessageCreateSerializer(serializers.ModelSerializer):
    # chat_room = ChatRoomSerializer()
    class Meta:
        model = Message
        fields = ('id', 'user', 'chat_room', 'content', 'timestamp')
        read_only_fields = ['id','user','timestamp','chat_room']