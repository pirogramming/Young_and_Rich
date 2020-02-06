from django.shortcuts import render, get_object_or_404

from comp.models import Comp, ComPost, ComComment
from comp.models import Comp


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


def comp_detail_overview(request, pk):
    o = Comp.objects.get(pk=pk)
    data = {
        "o": o,
    }
    return render(request, "comp/comp_detail_overview.html", data)


def comp_detail_overview_description(request, pk):
    d = Comp.objects.get(pk=pk)
    data = {
        "d": d,
    }
    return render(request, "comp/comp_detail_overview_description.html", data)


def comp_detail_overview_evaluation(request, pk):
    e = Comp.objects.get(pk=pk)
    data = {
        "e": e,
    }
    return render(request, "comp/comp_detail_overview_evaluation.html", data)


def comp_detail_overview_timeline(request, pk):
    t = Comp.objects.get(pk=pk)
    data = {
        "t": t,
    }
    return render(request, "comp/comp_detail_overview_timeline.html", data)


def comp_detail_overview_prizes(request, pk):
    p = Comp.objects.get(pk=pk)
    data = {
        "p": p,
    }
    return render(request, "comp/comp_detail_overview_prizes.html", data)


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


from datetime import datetime

from django.utils.dateformat import DateFormat


def progressbar(request, pk):
    comp = get_object_or_404(Comp, pk=pk)

    today = int(DateFormat(datetime.now()).format('Ymd'))

    created_date = int(DateFormat(comp.created_at).format('Ymd'))
    dead_date = int(DateFormat(comp.deadline.date()).format('Ymd'))
    total = dead_date - created_date

    context = {
        'comp': comp
    }
    return render(request, 'comp/progressbar.html', context)
