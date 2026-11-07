from django.urls import path
from apps.customer_supports.live_chats.views.chat_views import chat_room_view

urlpatterns = [
    path('room/<str:room_name>/', chat_room_view, name='chat_room'),
]