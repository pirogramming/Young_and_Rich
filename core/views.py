from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile


# Create your views here.

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('core:profile')  # change to main page
        else:
            return render(request, 'account/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'account/login.html')


def profile(request):
    user = get_object_or_404(User)
    stars = user.profile.star.all()
    data = {
        'stars': stars
    }
    return render(request, 'account/profile.html', data)


def show_user_rank(request):
    user = User.objects
    user_list = User.objects.all().order_by('profile__rank')
    # foreign 으로 연결되어 있는 애로 정렬을 하려면 저렇게 언더바 2개 넣은 형태로 기준을 주면 된다.
    pagenator = Paginator(user_list, 2)
    page = request.GET.get('page')
    # GET 방식의 request 은 딕셔너리이다. 이 딕셔너리에서 'page'라는 키의 value 를 받아오자는 것.
    posts = pagenator.get_page(page)
    # get_page 메소드는 페이지 번호 받아서 해당 페이지 리턴함.

    return render(request, 'core/userrank.html', {
        'user': user, 'posts': posts})
