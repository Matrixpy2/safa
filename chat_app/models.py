from django.db import models
from django.contrib.auth.models import User
from teachers.models import teacher
from students.models import Students
# Create your models here.

class ChatRoom(models.Model):
    teacher = models.ForeignKey(teacher  , on_delete=models.CASCADE , verbose_name='معلم')
    student = models.ForeignKey(Students , on_delete=models.CASCADE , verbose_name='دانش آموز')

    def __str__(self):
        return f"{self.teacher.first_name} , {self.student.first_name} ChatRoom"
    
class Message(models.Model):
    room   = models.ForeignKey(ChatRoom   , on_delete=models.CASCADE , verbose_name= 'چت روم')
    sender = models.ForeignKey(User       , on_delete=models.CASCADE , verbose_name= 'فرستنده پیام') 
    text   = models.TextField(blank=False , null=False , verbose_name='متن پیام')
    date   = models.DateField(auto_now_add=True , verbose_name='تاریخ ارسال پیام')
