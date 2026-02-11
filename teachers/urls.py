from django.urls import path
from .views import sign_up_teacher
urlpatterns = [
    path('signup/' , sign_up_teacher)
]