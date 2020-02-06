from django.shortcuts import render

from comp.models import Comp, ComPost, ComComment


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