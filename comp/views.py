from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import DateFormat

from comp.models import Comp, ComPost, ComComment, ComCommComment, Answer


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
        comment = ComComment.objects.filter(compost=compost)
        dict[compost.id] = len(comment)

    ctx = {
        "compost_list": qs,
        "q": q,
        "dict": dict,
    }
    return render(request, "comp/comp_detail_community_list.html", ctx)


def comp_detail_community_detail(request, pk, pk2):
    post = ComPost.objects.filter(comp=Comp.objects.get(pk=pk)).get(pk=pk2)
    comment_list = ComComment.objects.filter(compost=ComPost.objects.get(pk=pk2))

    dict = {}
    for comment in comment_list:
        commcomment = ComComment.objects.filter(comcomment=comment)

        dict[comment.id] = [c for c in commcomment]

    count_comment = len(comment_list) + len(dict)

    ctx = {
        "post": post,
        "comment_list": comment_list,
        "commcomment_dict": dict,
        "count_comment": count_comment,
    }
    return render(request, "comp/comp_detail_community_detail.html", ctx)


def comp_ranking(request, pk):
    comp = Comp.objects.get(pk=pk)
    answers = comp.answer.order_by('rank')
    context = {
        "answers": answers
    }
    return render(request, 'comp/comp_ranking.html', context)
