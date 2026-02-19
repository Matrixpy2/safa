from django.urls import path
from .views import Sign_up , Login
urlpatterns=[
    path('signin/' , Sign_up.as_view()  , name='sign_up' ),
    path('login/'  , Login.as_view()    , name='sign_up')

]