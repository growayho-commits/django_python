from django.urls import path
from .views.chat_views import chat_room_view, room_view

app_name = 'live_chats'

urlpatterns = [
    path('chat-room/', chat_room_view, name='chat_room'),
    path('room/', room_view, name='room'),
]
