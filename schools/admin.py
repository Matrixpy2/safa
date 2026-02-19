from django.contrib import admin
from .models import School , Teacher , classes , lesson
# Register your models here.

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name' , 'address' , 'manager' ]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher']

@admin.register(classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ['title' , 'teacher' , 'school']

@admin.register(lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']