from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions
from .models import ChatRoom , Message
from students.models import Students
from teachers.models import teacher
from .serializers import SendMessageSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

class ChatApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self , request , student_id):
        student = Students.objects.get(id=student_id)
        Teacher = teacher.objects.get(user=request.user)
        room , created = ChatRoom.objects.get_or_create(
            teacher = Teacher,
            student = student
        )
        message = Message.objects.filter(room=room).order_by('date')
        data =[]
        for m in message:
            data.append(
                {
                    'sender':m.sender.username,
                    'text': m.text,
                    'date':m.date
                }
            )
        return Response(
            {
                'message':f'chat with {student.first_name} {student.last_name}',
                'room_id' : room.id,
                'data':data
            }
        )

    def post(self , request , student_id):
        ser = SendMessageSerializer(
            data=request.data,
            context={
                'request':request,
                'student_id':student_id
            }
        )
        if ser.is_valid():
            message =ser.save()
            student = Students.objects.get(id = student_id)
            Teacher = teacher.objects.get(user = request.user)
            room , created = ChatRoom.objects.get_or_create(
                student = student,
                teacher = Teacher,
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{room.id}',
                {
                    "type": "chat.message",
                    "message": {
                        "id": message.id,
                        "text": message.text,
                        "sender": message.sender.username,
                        "date": str(message.date),
                    }
                }
            )

            return Response(
                {
                    'text':message.text,
                    'reciever' : student_id,
                    'room_id' : room.id,
                    'message' : 'message was sent'
                }
            )
        return Response(
            {
                'message' : ser.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


