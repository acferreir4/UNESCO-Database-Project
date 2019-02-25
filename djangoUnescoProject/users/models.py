from django.db import models
from django.contrib.auth.models import AbstractUser
#from institutions.models import Institution
from PIL import Image

class User(AbstractUser):
    role = models.CharField(max_length=150, default='Researcher', blank=True, null=True)
    institution = models.ForeignKey('institutions.Institution', on_delete=models.PROTECT)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
