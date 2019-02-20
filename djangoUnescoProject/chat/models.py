from users.models import User
from django.db import models


# Create your models here.

class ChatRooms(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=1)
    display_line_1 = models.CharField(max_length=50, null=True)
    display_line_2 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class RoomAccess(models.Model):
    user = models.ForeignKey(User, related_name='user_RoomAccess', on_delete=models.CASCADE)
    roomName = models.ForeignKey(ChatRooms, related_name='roomName_RoomAccess', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatRoom = models.ForeignKey(
        ChatRooms, related_name='CharRoom_messages', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.author.username

    def last_10_messages(RName):
        rm = ChatRooms.objects.filter(name=RName).first()
        msg = Message.objects.filter(chatRoom=rm)
        return msg.order_by('timestamp').all()
        # load all messages
        # return Message.objects.order_by('timestamp').all()
        # example for filtering
        # msg = Message.objects.filter(content='ok')
        # return msg.order_by('timestamp').all()