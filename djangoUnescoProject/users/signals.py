from django.db.models.signals import post_save
#from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User, Profile
from chat.models import RoomAccess, ChatRooms

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        room = ChatRooms.objects.create(name=instance.username, 
        	category='P', display_line_1=instance.get_full_name())
        RoomAccess.objects.create(user=instance,roomName=room)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
