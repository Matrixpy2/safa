from django.urls import path
from . import consumers
websocket_urlpatterns = [
    path('ws/teacher/chat/<int:room_id>/', consumers.ChatRoom ),
]