import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from .models import ChatRooms, RoomAccess
from .models import Message
import json

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):

	valid = False;
	for valid_rooms in RoomAccess.objects.filter(user=request.user):
		if valid_rooms.roomName.name == room_name:
			valid = True;

	if request.user.is_staff:
		valid = True;

	if valid:
		return render(request, 'chat/room.html', {
	        'room_name_json': mark_safe(json.dumps(room_name)),
	        'username': mark_safe(json.dumps(request.user.username)),
	        'chatRooms': ChatRooms.objects.order_by('category').all(),
	        'roomAccess': RoomAccess.objects.all(),
	    })
	else:
		return render(request, 'chat/accessDenied.html')
# def list(request):
#     context = {
#         'chatRooms': ChatRooms.objects.all()
#     }
#     return render(request, 'chat/room.html', context)

def downloadChat(request, room_name):
    if not request.user.is_staff:
        return render(request, 'chat/accessDenied.html')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chat-transcript.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Author', 
        'Timestamp', 
        'Content',
        ])

    rm = ChatRooms.objects.filter(name=room_name).first()
    for msg in Message.objects.filter(chatRoom=rm).order_by('timestamp'):
        writer.writerow([
            msg.author, 
            msg.timestamp, 
            msg.content,
            ])

    return response
