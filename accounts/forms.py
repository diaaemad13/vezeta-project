from cProfile import label
from dataclasses import field
from socket import fromshare
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserCreationForms(UserCreationForm):
    username = forms.CharField(label='الاسم')
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='ايميل')
    password1 = forms.CharField(label='كلمة السر', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label='اعادة كلمة السر', widget=forms.PasswordInput(), min_length=8)
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1','password2')


class Login_Form(forms.ModelForm):
    username = forms.CharField(label='الاسم')
    password = forms.CharField(label='باسورد', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='ايميل')
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')


class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('name', 'subtitle','address','numberphone','workhour','waittime','who_i','price','image','spicialist','type_of_person','twiter','facebook','gmail')
    

