from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_room_view(request):
    """
    Renders the live chat room dashboard or main list.
    """
    return render(request, 'live_chats/room.html')

@login_required
def room_view(request, room_name):
    """
    Renders a specific live chat room based on the room name.
    """
    return render(request, 'live_chats/room.html', {
        'room_name': room_name
    })