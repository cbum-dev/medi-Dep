from django.db import models
from Accounts.models import CustomUser
from ckeditor.fields import RichTextField
class Blog(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # content = models.TextField()
    body = RichTextField(default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
    def likes_count(self):
        return self.bloglike_set.count()
    
class BlogLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.blog.title}"

    class Meta:
        unique_together = ('user', 'blog')  # Ensures a user can like a blog only once


class HelpCenter(models.Model):
    prob_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    problem = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class HelpCenterComments(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    problem = models.ForeignKey(HelpCenter,on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.comment

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) :
        return self.name
class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField(default = "")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.content