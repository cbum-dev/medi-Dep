from django.contrib import admin
from .models import Blog,BlogLike,HelpCenterComments,HelpCenter,ChatRoom,Message
admin.site.register(Blog)
admin.site.register(BlogLike)
admin.site.register(HelpCenter)
admin.site.register(HelpCenterComments)
admin.site.register(Message)
admin.site.register(ChatRoom)
# Register your models here.


