from django.db import models
from teachers.models import teacher
from students.models import Students
from django.contrib.auth.models import User
# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=100 , verbose_name='نام مدرسه')
    address = models.CharField(max_length=200 , verbose_name='آدرس مدرسه')
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )


    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher = models.ForeignKey(teacher , on_delete=models.CASCADE , verbose_name='معلم')
    
    def __str__(self):
        return f'{self.teacher.first_name} {self.teacher.last_name}'
    
class lesson(models.Model):
    title = models.CharField(max_length=100 , verbose_name='عنوان درس')

    def __str__(self):
        return self.title
    
class classes(models.Model):
    title = models.CharField(max_length=100 , verbose_name='عنوان کلاس')
    teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE , verbose_name='معلم کلاس')
    students = models.ManyToManyField(Students , verbose_name='دانش آموزان کلاس')
    school = models.ForeignKey(School , on_delete=models.CASCADE , verbose_name='مدرسه')
    lesson = models.ForeignKey(lesson , on_delete=models.CASCADE , verbose_name='درس کلاس')
    def __str__(self):
        return self.title