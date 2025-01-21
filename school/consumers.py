from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                f"user_{self.user.id}", self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))

