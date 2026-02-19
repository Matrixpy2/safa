from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class teacher(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)

    first_name=models.CharField(max_length=35 , verbose_name='نام')
    last_name=models.CharField(max_length=55 , verbose_name='نام خانوادگی')
    number_id=models.CharField(max_length=10 , verbose_name='کد ملی')

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'


