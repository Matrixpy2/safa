from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.context_processors import request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer , SignUpSerializer , TeacherSerializer , AddStudentSerializer
from rest_framework import status
from .models import teacher
from rest_framework_simplejwt.tokens import RefreshToken , BlacklistedToken , OutstandingToken
from schools.models import classes
from students.models import Students
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
                'message':"send student's number_id and class_name",
            }
        )
    def post(self , request):
        ser = AddStudentSerializer(data=request.data)

        if ser.is_valid():
            number_id = ser.validated_data['number_id']
            class_name = ser.validated_data['title']
            new_std= Students.objects.get(number_id=number_id)
            
            
            




