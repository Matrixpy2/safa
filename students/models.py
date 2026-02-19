from django.db import models
from teachers.models import teacher
from django.contrib.auth.models import User

# Create your models here.
class Students(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='دانش آموز'
    )
    first_name = models.CharField(max_length=255 , verbose_name='نام')
    last_name = models.CharField(max_length=255 , verbose_name= 'نام خانوادگی')
    number_id = models.CharField(max_length=10 , verbose_name='کد ملی')
    def __str__(self):
        return f'{self.first_name} {self.last_name} '
    
