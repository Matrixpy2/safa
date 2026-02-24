from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser ,User
from .models import ChatRoom , Message
import json

class ChatRoomConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat {self.room_id}'

        user = self.scope['user']
        if isinstance(user ,AnonymousUser):
            await self.close()
            return
        is_member = await self.user_in_room(user.id , self.room_id)
        if not is_member:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name , self.channel_name)
        await self.accept()
    async def disconnect(self, close_code):
        self.channel_layer.group_discard(self.room_groupe_name , self.channel_name)
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        text = data.get('text','')
        user = self.scope['user']
        msg = self.create_message(user.id , self.room_id , text)

        payload={
            'id':msg['id'],
            'text' : msg['text'],
            'sender':msg['sender'],
            'date' : msg['date'],
        }
        await self.group_send(
            self.room_group_name,
            {
                'type':'chat.message',
                'message':payload
            }
        )
    async def chat_message(self , event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def user_in_room(self , user_id , room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return False
        return room.teacher.user_id == user_id or room.student.user_id == user_id
    
    @database_sync_to_async
    def create_message(self , user_id , room_id , text):
        room = ChatRoom.objects.get(id = room_id)
        user = User.objects.get(id=user_id)
        msg = Message.objects.create(
            room=room,
            sender=user,
            text=text
        )
        return { "id": msg.id, 
                "text": msg.text, 
                "sender": msg.sender.username, 
                "date": msg.date.isoformat(),
                }