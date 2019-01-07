from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Announcements(models.Model):
		Title = models.CharField(max_length=200)
		Content = models.TextField()
		CreationTime = models.DateTimeField(auto_now=True)
		IsActive = models.BooleanField(default=True)
		HasAttachment = models.BooleanField(default=False)
		Attachment_ID = models.IntegerField(default=0)


