from django.urls import path
from .views import Sign_up , Login , My_classes , My_class , My_homework
urlpatterns=[
    path('signin/' , Sign_up.as_view()  , name='sign_up' ),
    path('login/'  , Login.as_view()    , name='login'),
    path('my_classes/' , My_classes.as_view() , name='my_classes'),
    path('my_classes/<int:class_id>/' , My_class.as_view() , name='my_class_detail'),
    path('my_homework/' , My_homework.as_view() , name='my_homework')

]