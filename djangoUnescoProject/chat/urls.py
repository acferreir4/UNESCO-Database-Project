from django.urls import path, re_path
from .views import index, room
from . import views

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^(?P<room_name>[^/]+)/download/$', views.downloadChat, name='download-chat'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]