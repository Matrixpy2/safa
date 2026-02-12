from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login
from .forms import signupteacherForm , loginteacherForm

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return HttpResponse('به صفحه معلمان خوش آمدید')
    else:
        return redirect('login')

def sign_up_teacher(request):
    #
    # form=signupteacherForm()

    if request.method =='POST':

        form=signupteacherForm(request.POST)
        if form.is_valid():

            form.save()
            print('form was saved')
            return redirect('login')

        else:
            print('this is cleaned data ' , form.cleaned_data)
            print(form.errors.values())

    else:
         form=signupteacherForm()
    return render(request , 'sign_up_teacher.html' , {"form" : form} )


def loginteacherview(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = loginteacherForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data['user_name']
            password=form.cleaned_data['password']

            user = authenticate(request , username=user_name, password=password)

            if user is not None:
                login(request , user)
                return redirect('home')
            else:
                form.add_error(None , 'invalid username or password')
        else:
            form.add_error(None , 'has error')

    else:
        form = loginteacherForm()

    return render(request , 'login_teacher.html' , context={'form': form})


