from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.context_processors import request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (SendMessageSerializer,LoginSerializer , SignUpSerializer , NewsSerializer, AddStudentSerializer , HomeworkSerializer )
from rest_framework import status
from .models import teacher
from rest_framework_simplejwt.tokens import RefreshToken , BlacklistedToken , OutstandingToken
from schools.models import classes
from students.models import Students
from chat_app.models import ChatRoom , Message
# Create your views here.


class home(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    'message' : 'you are not login'
                }
            )
        return Response(
            {
                'message': f'welcome {user.first_name}'
            }
        )

class sign_in(APIView):
    def get(self , request):
        return Response(
            'enter username , first_name , last_name , number_id , password1 , password2'
        )

    def post(self , request):
        ser = SignUpSerializer(data=request.data)
        if ser.is_valid():
            data = ser.validated_data
            user = ser.save()

            return Response(
                {
                    'message' : f'user with username : {user.username} was created'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            ser.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class login(APIView):
    def get(self , request):
        user = request.user
        return Response(
            {
                'message' : 'login page '
                            'enter username and password'
            }
        )
    def post(self ,request):
        ser = LoginSerializer(data=request.data)

        if ser.is_valid():
            username = ser.validated_data['username']
            password = ser.validated_data['password']
            user = User.objects.get(username= username)


            token = RefreshToken.for_user(user=user)
            return Response(
                {
                    'message'     :     f'welcome {username} ',
                    'access token':     f'{token.access_token}'
                },
                status = status.HTTP_200_OK
            )
        return Response(
            {
                'message' : f'{ser.errors}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

        return Response(
            {
                'message' : f'{ser.errors}'
            }
        )

class Home_teacher(APIView):

    permission_classes = [IsAuthenticated]

    def get(self , request):
        profile = teacher.objects.get(user=request.user)
        return Response(
            {
                f'welcome {profile.first_name} {profile.last_name}',
                f'your number_id : {profile.number_id}'
            }
        )
    def post(self , request):
        pass

class logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        user = request.user
        token = OutstandingToken.objects.filter(user=user)
        for t in token:
            try:
                BlacklistedToken.objects.get_or_create(token=t)
            except Exception:
                pass

        return Response(
            {
                'message': f'you are logging out'
            } ,
            status=status.HTTP_205_RESET_CONTENT
        )

class AddStudent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        return Response(
            {
                'message':"send student's number_id and title of class",
            }
        )
    def post(self , request):
        ser = AddStudentSerializer(data=request.data)

        if ser.is_valid():
            number_id = ser.validated_data['number_id']
            class_name = ser.validated_data['title']
            new_std= Students.objects.get(number_id=number_id)
            new_cls = classes.objects.get(title=class_name)
            new_cls.students.add(new_std)
            return Response(
                {
                    'message' : f'student with number_id {number_id}() was added to class {class_name}'
                }
            )
        return Response(
            {
                'error' : f'{ser.errors}'
            },
        )


class AddNews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        return Response(
            {
                'message':"send title , content and class_name(title) of news",
            }
        )
    def post(self , request):
        ser = NewsSerializer(data=request.data)
        if ser.is_valid():
            news = ser.save(author=teacher.objects.get(user=request.user))
            return Response(
                {
                    'message' : f'news with title {news.title} was created , owned by {news.author.first_name} {news.author.last_name}'
                }
            )
        return Response(
            {
                'error' : f'{ser.errors}'
            },
        )


class AddHomework(APIView):
    def get(self , request):
        return Response(
            {
                'message':"send title , content and class_name(title) of homework",
            }
        )
    def post(self , request):
        ser = HomeworkSerializer(data=request.data)
        if ser.is_valid():
            title   = ser.validated_data['title']
            classes = ser.validated_data['classes']
            content = ser.validated_data['content']     

            homework    = ser.save(
                author  = teacher.objects.get(user=request.user),
                title   = title,
                classes = classes,
                content = content
            )
            return Response(
                {
                    'message' : f'homework with title {homework.title} was created , owned by {homework.author.first_name} {homework.author.last_name}'
                }
            )
        return Response(
            {
                'error' : f'{ser.errors}'
            },
        )


class chat_list(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        # print(classes.objects.filter(teacher__teacher__user=request.user))
        chats = classes.objects.filter(teacher__teacher__user=request.user)
        print(chats)
        data = []

        for c in chats:
            data.append(
                {
                    'class': c.title,
                    'lesson': c.lesson.title,
                    'teacher': f'{c.teacher.teacher.first_name} {c.teacher.teacher.last_name}',
                    'students': [
                        {
                            'id': s.id,
                            'name': f'{s.first_name} {s.last_name}'
                        }
                        for s in c.students.all()
                    ]
                }
            )

        return Response(
            {
                'message': 'for going to chat page send student id and text of message',
                'example': '/chat/1/',
                'data': data
            }
        )
    
class SendMessage(APIView):
    def get(self , request , student_id):
        student = Students.objects.get(id=student_id)
        Teacher = teacher.objects.get(user=request.user)

        if not ChatRoom.objects.filter(student=student , teacher=Teacher).exists():
            ChatRoom.objects.create(student=student , teacher=Teacher)
        chat_room = ChatRoom.objects.get(student=student , teacher=Teacher)
        messages = Message.objects.filter(room=chat_room).order_by('date')
        data = []
        for m in messages:
            data.append({
                'sender': m.sender.username,
                'text': m.text,
                'date' : m.date
            })
        return Response(
            {
                'message' : f'you are ins chat with {student.first_name}',
                'data' : data
            }
        )
    def post(self, request , student_id):
        ser = SendMessageSerializer(data=request.data ,
                                    context={
                                    'request': request ,
                                    'student_id': student_id
                                    }
                                    )
        if ser.is_valid():
            Message = ser.save()
            return Response(
                {
                    'text' : Message.text,
                    'reciever' : student_id,
                    'message' : 'message sent successfully'
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'message' : ser.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
            