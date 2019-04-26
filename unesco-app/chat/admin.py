from django.contrib import admin
from .models import Message, RoomAccess, ChatRooms

# Register your models here.

# admin.site.register(Message)
# admin.site.register(ChatRooms)
# admin.site.register(RoomAccess)

class ChatRoomsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'display_line_1', 'display_line_2')
    ordering = ('category','name')
admin.site.register(ChatRooms, ChatRoomsAdmin)

class RoomAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'roomName')
admin.site.register(RoomAccess, RoomAccessAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'chatRoom')
admin.site.register(Message, MessageAdmin)