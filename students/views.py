from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken , BlacklistedToken , OutstandingToken
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSerializer , LoginSerializer
from rest_framework import status
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
        ser = LoginSerializer(request.data)

        if ser.is_valid():
            data = ser.validated_data
            username = data.get('username')
            user = User.objects.get(username=username)
            token=RefreshToken.for_user(user)
            return Response(
                {
                    'message' : f'welcome {user.first_name} {user.last_name}',
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
