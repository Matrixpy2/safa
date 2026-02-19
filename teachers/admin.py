from django.contrib import admin
from .  import models
# Register your models here.

@admin.register(models.teacher)
class Teacher(admin.ModelAdmin):
    list_display = ['first_name' , 'last_name','number_id']