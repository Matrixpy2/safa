# from django.urls import path
# from . import consumers
# websocket_urlpatterns = [
#     path('ws/chat/<int:room_id>/', consumers.ChatRoomConsumers.as_asgi()),
# ]
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('teacher/chat/<int:room_id>/', consumers.ChatRoomConsumers.as_asgi()),
]
