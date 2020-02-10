from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


# 회원가입 폼
class SignupForm(forms.Form):
    username1 = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '유저의 닉네임은 무엇?'
        }))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control input-lg'
        }
    ))

    image = forms.ImageField()
    email1 = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '이메일 형태로 입력을 하세요!'
        }))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '이름은 무엇?'
        }))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '성은 무엇?'
        }))

    def signup(self, request, user):
        User.username = self.cleaned_data['username1']
        User.email = self.cleaned_data['email1']
        User.password = self.cleaned_data['password']
        userprofile = Profile
        userprofile.user = user
        User.first_name = self.cleaned_data['first_name']
        User.last_name = self.cleaned_data['last_name']
        userprofile.image = self.cleaned_data['image']
        userprofile.save()
        user.save()
        return user
