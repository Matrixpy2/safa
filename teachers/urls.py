from django.urls import path
from .views import home , login , sign_in , Home_teacher , logout
urlpatterns = [
    path(''        , home.as_view()         , name='home'   ),
    path('signup/' , sign_in.as_view()      , name='signin' ),
    path('login/'  , login.as_view()        , name='login'  ),
    path('home/'   , Home_teacher.as_view() , name='Home'),
    path('logout/' , logout.as_view()       , name='logout')

]