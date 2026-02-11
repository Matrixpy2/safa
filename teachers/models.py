from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class teacher(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)

    first_name=models.CharField(max_length=35)
    last_name=models.CharField(max_length=55)
    number_id=models.CharField(max_length=10)

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'
