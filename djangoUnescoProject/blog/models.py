from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    fileAttachment = models.FileField(upload_to='announcements/files', blank=True, null=True)
    imageAttachment = models.ImageField(upload_to='announcements/images', blank=True, null=True)

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

