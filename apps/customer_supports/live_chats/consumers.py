import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SupportLiveChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # அறையில் இணைத்தல்
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # அறையிலிருந்து வெளியேறுதல்
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']

        # குழுவிற்கு செய்தியை அனுப்புதல்
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # WebSocket கிளையண்டிற்கு செய்தியை அனுப்புதல்
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))