from django.urls import path
from .views import sign_up_teacher , loginteacherview , home
urlpatterns = [
    path('' , home , name='home' ),
    path('signup/' , sign_up_teacher ,name='sign'),
    path('login/' , loginteacherview , name='login'),

]