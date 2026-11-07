from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_room_view(request, room_name):
    return render(request, 'live_chats/room.html', {
        'room_name': room_name
    })