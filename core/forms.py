from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import resolve_url

from .models import Profile


# django-allauth 의 SignupForm을 상속받음. 이유는 아래와 같다.
# 그냥 새로 폼을 만드니 allauth 의 signupform 이 우선으로 적용되어 username, email, password 가 커스텀이 불가능함.
# 그래서 상속을 받아서 사용했으며, 상속한 뒤의 사용 방법은 아래와 같다.
# 1) super : 공식문서를 보니 이렇게 시작을 한다더라.
# 2) 각 폼의 html 에서 적용되는 속성은 attrs 으로 줄 수 있다.
# 3) 다만 username, email 의 경우 기본적으로 적용된 widget이 있기에 딕셔너리의 update 메소드를 사용하였고
# 그 아래 애들은 기본으로 존재하는 폼이 없기에 새로 폼을 설정해주었다
# def init 안에 저렇게 self.fields 로써 만들어야 폼이 적용됨. 클래스 아래에 직접 속성을 주면 super 가 없기에 폼 적용 안됨.

class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['username'].widget.attrs.update({
            'class': 'form-control input-lg',
            'placeholder': ''
        })
        self.fields['email'].label = "이메일 (선택)"
        self.fields['email'].widget.attrs.update({
            'class': 'form-control input-lg',
            'placeholder': ''
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control input-lg',
            'placeholder': ''
        })
        self.fields['password2'].label = "비밀번호 확인"
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control input-lg',
            'placeholder': ''
        })
        self.fields['last_name'] = forms.CharField(max_length=20, label='성', widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
            }))
        self.fields['first_name'] = forms.CharField(max_length=20, label='이름', widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
            }))
    # 만약에 user 모델에서 뭔가 추가되어서 새로 폼에서 받으려면 이 아래에 추가하면 된다.
    # 지금은 그냥 기본으로 존재하는 first_name, last_name 밖에 없어서 이렇게 함.
    # cleaned_data 라는건 폼을 거친 뒤의 값이다. 원래는 request.POST['first_name'] 이건데 얘는 완전 날것의 자료.
    # 완전 날것이기에 폼을 거친 뒤 어떻게 변할지 모르니 폼을 거친 뒤의 값인 cleaned_data 를 쓰는 것.

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        return user


# 클래스 기반 뷰 : 모델폼을 사용했고, 여기와 view 에 저런식으로 추가해줘야한다.

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'organization']

    phone_number = forms.CharField(max_length=11, label='핸드폰', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
        }))

    image = forms.ImageField(label='프로필 사진')

    organization = forms.CharField(max_length=50, label='소속', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
        }))


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'type': 'email'
        })

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return resolve_url(next_url)


'''
# 기존에 사용했던 회원가입 폼. allauth 상에서 커스텀을 어떻게 하는지 몰라서 아래처럼 상속받음. 
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
        User.password = self.cleaned_data['password1']
        userprofile = Profile
        userprofile.user = user
        User.first_name = self.cleaned_data['first_name']
        User.last_name = self.cleaned_data['last_name']
        userprofile.image = self.cleaned_data['image']
        userprofile.save()
        user.save()
        return user
'''
