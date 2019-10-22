from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_expired = models.DateField('Expiry Date (YYYY-MM-DD)')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    fileAttachment = models.FileField('File Attachment', upload_to='announcements/files', blank=True, null=True)
    imageAttachment = models.ImageField('Image Attachment',upload_to='announcements/images', blank=True, null=True)

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self):
        super().save()
        img = Image.open(self.imageAttachment.path)
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.imageAttachment.path)

