from django.urls import path
from . import views
urlpatterns = [
    path(''        , views.home.as_view()         , name='home'   ),
    path('signup/' , views.sign_in.as_view()      , name='signin' ),
    path('login/'  , views.login.as_view()        , name='login'  ),
    path('home/'   , views.Home_teacher.as_view() , name='Home'),
    path('logout/' , views.logout.as_view()       , name='logout'),
    path('add-student/' , views.AddStudent.as_view() , name='add-student'),
    path('add-news/' , views.AddNews.as_view() , name='add-news'),
    path('add-homework/' , views.AddHomework.as_view() , name='add-homework'),
    path('chat/' , views.chat_list.as_view() , name='chat-list'),
    path('chat/<int:student_id>/' , views.SendMessage.as_view() , name='send message')

]