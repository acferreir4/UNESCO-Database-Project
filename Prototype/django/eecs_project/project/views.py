from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Announcements
# Create your views here.

@login_required
def home(request):
	context = {
		'posts': Announcements.objects.all()
	}
	return render(request, 'project/home.html', context)

@login_required
def profiles(request):
	return render(request, 'project/profiles.html', {'title': 'Profiles'})
