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
from .models import Profile, Comp, Answer
import json


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
            return render(request, 'account/login.html', {'error': '비밀번호가 일치하지 않습니다'})
    else:
        return render(request, 'account/login.html')


@login_required
def profile(request):
    # 이 유저가 참여한 comp
    # comp_rank를 바탕으로 하는 메달들 수 계산하기
    answer = Answer.objects.filter(user=request.user).order_by('-accuracy')
    comp_lst = list()
    comp_all = Comp.objects.all()

    try:
        comp = Comp.objects.filter(id=answer[0].comp.id).get(continue_complete=-1)
        comp_lst.append(comp)

    except:
        pass

    for i in range(len(answer) - 1):
        try:
            if answer[i].comp.id != answer[i + 1].comp.id:
                comp = Comp.objects.filter(id=answer[i + 1].comp.id).get(continue_complete=-1)
                comp_lst.append(comp)
        except:
            pass

    medal_dict = request.user.profile.get_medal_list()
    my_comp_ranking = json.loads(request.user.profile.comp_rank)

    stars = Comp.objects.filter(star=request.user)
    data = {
        'my_comp_ranking': my_comp_ranking,  # 참여한 comp의 ranking
        'comp_list': comp_lst,  # 이 유저가 참여한 comp
        'stars': stars,
        'medal_dict': medal_dict,  # {'gold': 0,'silver': 0, 'bronze': 0, 'badge': 0} 형식
        "comp_all": comp_all,
    }
    return render(request, 'account/profile.html', data)


def profile_view(request, username):
    user = User.objects.get(username=username)
    stars = user.profile.star.all()
    data = {
        'stars': stars,
        'user': user
    }
    return render(request, 'account/profile_view.html', data)


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
