from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='project-home'),
    path('profiles', views.profiles, name='project-profiles'),
]
