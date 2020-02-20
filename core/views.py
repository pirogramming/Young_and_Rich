from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import ProfileForm
from .models import Profile, Comp


# Create your views here.

def sign_in(request):
    next = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # request.user = None
            auth.login(request, user)
            # request.user = user
            return redirect(request.POST.get('next') or 'profile')  # change to main page
        else:
            return render(request, 'account/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'account/login.html')


@login_required
def profile(request):

    stars = Comp.objects.filter(star=request.user)



    data = {
        'stars': stars
    }
    return render(request, 'account/profile.html', data)


# LoginRequiredMixin : @login_required 의 클래스 기반 뷰 버전이다. 저걸 넣으면 @login_required 랑 같은 기능함.
# UpdateView 는 원래 pk 값을 지정받아서 뽑아내줘야하는데, 여기서는 그런거 안쓰잖아? 그래서 get_object 쓰는 것.
#
class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile


profile_edit = ProfileUpdateView.as_view()


def show_user_rank(request):
    #  request: 복잡한 객체.

    user_list = User.objects.all().order_by('profile__rank')
    # foreign 으로 연결되어 있는 애로 정렬을 하려면 저렇게 언더바 2개 넣은 형태로 기준을 주면 된다.
    paginator = Paginator(user_list, 2)  # 한 페이지에 보일 user 수
    page = request.GET.get('page')
    # GET 방식의 request 은 딕셔너리이다. 이 딕셔너리에서 'page'라는 키의 value 를 받아오자는 것.
    posts = paginator.get_page(page)
    # get_page 메소드는 페이지 번호 받아서 해당 페이지 리턴함.

    return render(request, 'core/userrank.html', {
        'user': request.user, 'posts': posts})
