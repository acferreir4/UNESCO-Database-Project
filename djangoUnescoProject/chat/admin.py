from django.contrib import admin
from .models import Message, RoomAccess, ChatRooms

# Register your models here.

# admin.site.register(Message)
admin.site.register(ChatRooms)
admin.site.register(RoomAccess)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'chatRoom')
admin.site.register(Message, MessageAdmin)