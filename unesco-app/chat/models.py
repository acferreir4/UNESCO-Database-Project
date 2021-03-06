from users.models import User
from django.db import models
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z\d\-_]*$', 'Only alphanumeric characters, _ and -  are allowed. No Space.')

class ChatRooms(models.Model):
    name = models.CharField(max_length=50,validators=[alphanumeric])
    category = models.CharField(max_length=1,choices=(("G", "Group Room"),("P", "Personal Room")))
    display_line_1 = models.CharField(max_length=50, null=True)
    display_line_2 = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Chat Rooms"

    def __str__(self):
        return self.name


class RoomAccess(models.Model):
    user = models.ForeignKey(User, related_name='user_RoomAccess', on_delete=models.CASCADE)
    roomName = models.ForeignKey(ChatRooms, related_name='roomName_RoomAccess', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Room Access"

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
        last_100 = Message.objects.filter(chatRoom=rm).order_by('-timestamp')[:100]
        return reversed(last_100)
        # load all messages
        # return Message.objects.order_by('timestamp').all()
        # example for filtering
        # msg = Message.objects.filter(content='ok')
        # return msg.order_by('timestamp').all()