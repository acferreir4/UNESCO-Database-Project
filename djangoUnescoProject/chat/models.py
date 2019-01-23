from users.models import User
from django.db import models


# Create your models here.

class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('timestamp').all()
        # load all messages
        # return Message.objects.order_by('timestamp').all()
        # example for filtering
        # msg = Message.objects.filter(content='ok')
        # return msg.order_by('timestamp').all()
        