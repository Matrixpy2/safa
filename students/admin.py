from django.contrib import admin
from students.models import Students 
# Register your models here.

@admin.register(Students)
class Student(admin.ModelAdmin):
    list_display = ['first_name' , 'last_name' , 'number_id' ]
