from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import teacher

class signupteacherForm(UserCreationForm):
    first_name=forms.CharField(max_length=25)
    last_name=forms.CharField(max_length=55)
    number_id=forms.CharField(max_length=10 , required=True  , label='کد ملی')
    class Meta:
        model=User
        fields=['username','first_name' , 'last_name' , 'number_id' , 'password1' , 'password2' ]

    def save(self , commit=True):
        user = super().save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']

        if commit:
            user.save()

            teacher.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                number_id=self.cleaned_data['number_id'],

            )
            print(teacher.objects.all().values())
        return user

class loginteacherForm(forms.Form):
    user_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs=
            {
                'class':'form-control',
                'placeholder':'enter username'
            }
        )
        ,
        label='نام کاربری'
    )
    password=forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs=
            {
                'class':'form-control',
                'placeholder':'enter password'
            }
        ),
        label='رمز عبور'
    )