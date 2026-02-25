from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser ,User
from .models import ChatRoom , Message
import json

class ChatRoomConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

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

    # async def receive(self, text_data, bytes_data=None):
    #     print("RAW:", repr(text_data))

    #     if not text_data or text_data.strip() == "":
    #         print("EMPTY FRAME")
    #         return

    #     try:
    #         data = json.loads(text_data)
    #         print("JSON:", data)
    #     except Exception as e:
    #         print("INVALID JSON:", text_data, e)
    #         return

    #     text = data.get("text")
    #     if not text:
    #         print("NO TEXT FIELD")
    #         return

    #     user = self.scope["user"]
    #     msg = await self.create_message(user.id, self.room_id, text)

        # payload = {
        #     "id": msg["id"],
        #     "text": msg["text"],
        #     "sender": msg["sender"],
        #     "date": msg["date"],
        # }

    #     print("PAYLOAD:", payload)

    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             "type": "chat_message",
    #             "message": payload
    #         }
    #     )

    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event['message']))

    # @database_sync_to_async
    # def user_in_room(self, user_id, room_id):
    #     try:
    #         room = ChatRoom.objects.get(id=room_id)
    #     except ChatRoom.DoesNotExist:
    #         return False
    #     return room.teacher.user_id == user_id or room.student.user_id == user_id

    # @database_sync_to_async
    # def create_message(self, user_id, room_id, text):
    #     room = ChatRoom.objects.get(id=room_id)
    #     user = User.objects.get(id=user_id)
    #     msg = Message.objects.create(
    #         room=room,
    #         sender=user,
    #         text=text
    #     )
    #     return {
    #         "id": msg.id,
    #         "text": msg.text,
    #         "sender": msg.sender.username,
    #         "date": msg.date.isoformat(),
    #     }
