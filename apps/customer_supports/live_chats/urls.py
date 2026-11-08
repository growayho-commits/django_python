from django.urls import path
from apps.customer_supports.live_chats.views import chat_views

urlpatterns = [
    # ஒருவேளை லைவ் சாட் லேண்டிங் அல்லது ரூட் லிஸ்ட் வியூ இருந்தால்:
    path('', chat_views.chat_room_view, name='chat_home'), # அல்லது பொருத்தமான வியூ
    path('room/<str:room_name>/', chat_views.room_view, name='room'),
]