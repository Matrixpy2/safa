from http.client import HTTPResponse

from django.shortcuts import render , redirect
from .forms import signupteacherForm

# Create your views here.

def sign_up_teacher(request):
    #
    # form=signupteacherForm()

    if request.method =='POST':

        form=signupteacherForm(request.POST)
        if form.is_valid():
            form.save()
            # print(form.cleaned_data)
            return redirect('')

        else:
            print(form.cleaned_data)

            form=signupteacherForm()
    return render(request , 'sign_up_teacher.html' , {"form" : form} )

