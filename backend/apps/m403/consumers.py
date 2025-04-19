import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ResultsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.round_id = self.scope['url_route']['kwargs']['round_id']
        self.room_group_name = f"results_{self.round_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_update',
                'message': text_data
            }
        )

    async def send_update(self, event):
        await self.send(text_data=event["message"])
