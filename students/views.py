from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken , BlacklistedToken , OutstandingToken
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSerializer , LoginSerializer
from rest_framework import status
from schools.models import classes
from .models import Students
from .permissions import Is_student
from teachers.models import Homework
# Create your views here.

class Sign_up(APIView):
    def get(self , request):
        return Response(
            {
                'message':'send username , first_name , last_name , number_id , password1 , password2'
            }
        )
    def post(self, request):
        data = request.data
        ser = SignUpSerializer(data=data)
        if ser.is_valid():
            data = ser.validated_data
            user = ser.save()
            return Response(
                {
                    'message' : f'user with username : {user.username}'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'error':f'{ser.errors}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class Login(APIView):
    def get(self , request):
        return Response(
            {
                'message':'send username , password'
            }
        )
    def post(self , request):
        ser = LoginSerializer(data=request.data)

        if ser.is_valid():
            ser.validated_data
            username = ser.validated_data['username']
            user = User.objects.get(username=username)
            print(user)
            token=RefreshToken.for_user(user)
            return Response(
                {
                    'message' : f'welcome {username}',
                    'token' : {
                        'access': str(token.access_token),
                    }
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'error':f'{ser.errors}'
            }
        )
    
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

class My_classes(APIView):
    permission_classes = [ IsAuthenticated ]
    def get(self , request):
        user = request.user
        my_classes = classes.objects.filter(students__user=user)
        data = []
        for c in my_classes:
            data.append(
                {
                    'title': c.title,
                    'teacher': f'{c.teacher.teacher.first_name} {c.teacher.teacher.last_name}',
                    'lesson' : c.lesson.title,
                    'class_id' : c.id
                }
            )
        return Response(
            {
                'message' : 'for going to class: /students/my_classes/class_id',
                'my_classes': data
            }
        )
    
class My_class(APIView):
    permission_classes = [ IsAuthenticated ]
    def get(self , request , class_id):
        user = request.user
        my_class = classes.objects.filter(students__user=user , id=class_id).first()
        if not my_class:
            return Response(
                {
                    'error' : 'class not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        students = my_class.students.all()
        
        
        return Response(
            {
                'title': my_class.title,
                'teacher': f'{my_class.teacher.teacher.first_name} {my_class.teacher.teacher.last_name}',
                'lesson' : my_class.lesson.title,
                
            }
        )
    

class My_homework(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        user = request.user
        My_homework = Homework.objects.filter(classes__students__user=user)
        data = []
        for h in My_homework:
            data.append({
                'title': h.title,
                'class' : h.classes.title,
                'lesson': h.classes.lesson.title,
                'homework': h.content if h.content else None,
                'date' : h.date if h.date else None,
            })
        return Response({
            'my_homework': data
        })