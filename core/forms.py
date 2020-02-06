from django.contrib.auth.models import User
from django import forms
from .models import Profile
from allauth.account.forms import LoginForm

# 회원가입 폼
class SignupForm(forms.Form):
    class Meta:
        model = User

    image = forms.ImageField()
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)


    def signup(self, request, user):
        userProfile = Profile
        userProfile.user = user
        User.first_name = self.cleaned_data['first_name']
        User.last_name = self.cleaned_data['last_name']
        userProfile.image = self.cleaned_data['image']
        userProfile.email = self.cleaned_data['email']
        userProfile.save()
        user.save()
        return user

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'type': 'email'
        })


