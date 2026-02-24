from django.urls import path
from . import consumers
websocket_urlpatterns = [
    path('teacher/chat/<int:student_id>/', consumers.ChatConsumer.as_asgi() ),
]