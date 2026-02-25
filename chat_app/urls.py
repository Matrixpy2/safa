from django.urls import path
from .views import ChatApi

urlpatterns =[
    path('chat/<int:student_id>/' , ChatApi.as_view())
]