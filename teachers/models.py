from django.db import models
from django.contrib.auth.models import User
# from students.models import Students
# from schools.models import classes 
# Create your models here.



class teacher(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)

    first_name=models.CharField(max_length=35 , verbose_name='نام')
    last_name=models.CharField(max_length=55 , verbose_name='نام خانوادگی')
    number_id=models.CharField(max_length=10 , verbose_name='کد ملی')

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'
    
class News(models.Model):
    author = models.ForeignKey(teacher ,on_delete=models.CASCADE , verbose_name='نویسنده خبر')
    classes = models.ForeignKey('schools.classes' , on_delete=models.CASCADE , verbose_name='کلاس مربوطه' , null=True)

    title = models.CharField(max_length=255 , verbose_name='عنوان خبر')
    content = models.TextField(verbose_name='متن خبر')

    def __str__(self):
        return self.title

class Homework(models.Model):
    author = models.ForeignKey(teacher ,on_delete=models.CASCADE , verbose_name='طراح سوال')
    classes = models.ForeignKey('schools.classes' , on_delete=models.CASCADE , verbose_name='کلاس مربوطه' , null=True)
    title = models.CharField(max_length=255 , verbose_name='عنوان تکلیف')
    content = models.TextField(verbose_name='متن تکلیف')
    date = models.DateField(verbose_name='تاریخ تحویل تکلیف' , null=True )

    def __str__(self):
        return self.title


