from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    phone_number = PhoneNumberField(
            'Phone number', 
            blank=True, 
            null=True, 
            unique=True
            )
    role = models.CharField(max_length=150, default='Researcher', blank=True, null=True)
    institution = models.ForeignKey('institutions.Institution', on_delete=models.PROTECT)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
