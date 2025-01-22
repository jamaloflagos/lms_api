from channels.generic.websocket import AsyncWebsocketConsumer
from school.models import Group, GroupMessage, User
from asgiref.sync import sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # if self.user.is_authenticated:
        #     await self.channel_layer.group_add(self.group_name, self.channel_name)
        #     await self.accept()
        # else:
        #     self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        message = data.get('message')
        student_id = data.get('student_id')
        group_id = data.get('group_id')

        if not all([message, student_id, group_id]):
            await self.send(text_data=json.dumps({"error": "Missing required fields"}))
            return

        sender = await sync_to_async(self.get_object)('student', student_id)
        group = await sync_to_async(self.get_object)('group', group_id)

        if not sender or not group:
            await self.send(text_data=json.dumps({"error": "Invalid student or group"}))
            return

        new_message = await sync_to_async(GroupMessage.objects.create)(
            group=group,
            sender=sender,
            content=message
        )

        serialized_message = {
            "id": new_message.id,
            "content": new_message.content,
            "sender": sender.id,
            "created_at": new_message.created_at.isoformat()
        }

        await self.channel_layer.group_send(
            group.group_name,
            {
                "type": "chat_message",
                "payload": serialized_message
            }
        )

    def get_object(self, obj_type, lk_value):
        if obj_type == 'student':
            return User.objects.filter(id=lk_value).first()
        elif obj_type == 'group':
            return Group.objects.filter(id=lk_value).first()
        return None
    

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

