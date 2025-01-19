from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Student, Group
from django.shortcuts import get_object_or_404
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        student_id = data['student_id']
        # group_id = data['group_id']
        
        # Use sync_to_async to fetch the student and create the message asynchronously
        student = await database_sync_to_async(self.get_object)('student', student_id)
        group = await database_sync_to_async(self.get_object)('group', self.group_name)
        print(student, group)
        await database_sync_to_async(Message.objects.create)(
            group=group,
            content=message,
            sender=student
        )
        
        # Broadcast message to group
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat_message',
            'message': message
        })

    # Create a separate synchronous method to get the student
    def get_object(self, object, lk_value):
        if object == 'student':
            return get_object_or_404(Student, pk=lk_value)
        elif object == 'group':
            return get_object_or_404(Group, group_name=lk_value)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))


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
        await self.send(text_data=json.dumps(event["message"]))

