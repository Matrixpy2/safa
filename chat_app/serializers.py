from rest_framework import serializers
from .models import Message , ChatRoom
from students.models import Students
from teachers.models import teacher

class SendMessageSerializer(serializers.Serializer):
    class Meta:
        model=Message
        fields = ['text']
    
    def create(self, validated_data):
        request = self.context['request']
        student_id = self.context['student_id']

        student = Students.objects.get(id=student_id)
        Teacher = teacher.objects.get(user = request.user)
        room , created = ChatRoom.objects.get_or_create(student=student , teacher=Teacher)
        msg = Message.objects.create(
            room = room,
            sender=request.user,
            text=validated_data['text'],
        )
        return msg
