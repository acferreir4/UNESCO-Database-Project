from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
	Name = models.CharField(max_length=200)
		
class Countries(models.Model):
	Name = models.CharField(max_length=200)
	Population = models.IntegerField(default=0)
	PercentIndigenous = models.FloatField()
	PercentGdpOnEducation = models.FloatField()
	Definition = models.TextField()
	AverageEducation = models.TextField()
	Strategy = models.TextField()
	Continent = models.TextField()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	regionID = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
	Countrty = models.ForeignKey(Countries, null=True, on_delete=models.SET_NULL)
		
def __str__(self):
	return f'{self.user.username} Profile'