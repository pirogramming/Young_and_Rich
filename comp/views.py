from django.shortcuts import render, get_object_or_404

from comp.models import Comp, ComPost, ComComment, Answer

from datetime import date


# comp code 추가시 comp.team_number +1

def comp_list(request):
    qs = Comp.objects.all()
    q = request.GET.get("q", "")
    if q:
        qs = qs.filter(title__icontains=q)

    ctx = {
        "comp_list": qs,
        "q": q,
    }
    return render(request, "comp/comp_list.html", ctx)


def comp_detail_overview(request):
    return render(request, "comp/comp_detail_overview.html")


def comp_detail_data(request, pk):
    comp = Comp.objects.get(pk=pk)
    ctx = {
        "comp": comp,
    }
    return render(request, "comp/comp_detail_data.html", ctx)


def comp_detail_community_list(request, pk):
    qs = ComPost.objects.filter(comp=Comp.objects.get(pk=pk))
    q = request.GET.get("q", "")
    if q:
        qs = qs.filter(title__icontains=q)

    dict = {}
    for compost in qs:
        comment = ComComment.objects.filter(com_post=compost)
        dict[compost.id] = len(comment)

    ctx = {
        "compost_list": qs,
        "q": q,
        "dict": dict,
    }
    return render(request, "comp/comp_detail_community.html", ctx)


def progressbar(request, pk):
    comp = get_object_or_404(Comp, pk=pk)
    today = date.today()

    created_date = comp.created_at
    dead_date = comp.deadline.date()
    total = (dead_date - created_date).days
    interval = (today - created_date).days
    percent = round(interval / total, 2) * 100

    context = {
        'comp': comp,
        'percent': percent
    }
    return render(request, 'comp/progressbar.html', context)


def comp_ranking(request, pk):
    comp = Comp.objects.get(pk=pk)
    answers = comp.answer.order_by('rank')
    context = {
        "answers": answers
    }
    return render(request, 'comp/comp_ranking.html', context)

# 대회 deadline 날짜가 되면 대회를 완료 대회로 바꾸고, 순위에 따라 user 에게 메달을 부여한다.
# 1. if문으로 deadline날짜 판별
# 2. deadline == today 이면 대회를 완료 상태로 내리기
# + comp의 answer의 rank로 필터를 걸어서 해당 user 가져온다
# + 그 후, 해당 유저의 메달 리스트에 추가
