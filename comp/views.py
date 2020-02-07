from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.dateformat import DateFormat

from comp.forms import ComPostForm, ComCommentForm
from comp.models import Comp, ComPost, ComComment, Answer


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


# =========================커뮤니티===============================


def comp_detail_community_list(request, pk):
    comp = Comp.objects.get(pk=pk)
    qs = ComPost.objects.filter(comp=comp)
    q = request.GET.get("q", "")
    if q:
        qs = qs.filter(title__icontains=q)

    dict = {}
    for compost in qs:
        comment = ComComment.objects.filter(compost=compost)
        dict[compost.id] = len(comment)

    qs_number = len(qs)

    ctx = {
        "comp": comp,
        "compost_list": qs,
        "q": q,
        "dict": dict,
        "compost_number": qs_number,
    }
    return render(request, "comp/comp_detail_community_list.html", ctx)


def comp_detail_community_detail(request, pk, pk2):  # pk == comp 번호, pk2 == post 번호
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)

    list = ComComment.objects.filter(compost=compost)
    comment_list = []
    commcomment_list = []
    for comment in list:
        if not comment.commcomment:
            comment_list.append(comment)
        else:
            commcomment_list.append(comment)

    count_comment = len(comment_list) + len(commcomment_list)
    is_post_user = 1

    if compost.user == request.user:
        is_post_user = 0

    ctx = {
        "comp": comp,
        "compost": compost,
        "comment_list": comment_list,
        "commcomment_list": commcomment_list,
        "count_comment": count_comment,
        "is_post_user": is_post_user,
    }
    return render(request, "comp/comp_detail_community_detail.html", ctx)


# ----------------포스트--------------------


def comp_detail_community_post_create(request, pk):
    if request.method == "POST":
        form = ComPostForm(request.POST)
        if form.is_valid():
            compost = form.save(commit=False)
            compost.user = request.user
            compost.comp = Comp.objects.get(pk=pk)
            compost.save()
            return redirect("comp:comp_community_detail", pk, compost.pk)
    else:
        form = ComPostForm()
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_community_post_create.html", ctx)


def comp_detail_community_post_update(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        form = ComPostForm(request.POST, instance=compost)
        if form.is_valid():
            form.save()
        return redirect("comp:comp_community_detail", pk, pk2)

    else:
        form = ComPostForm(instance=compost)
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_community_post_create.html", ctx)


def comp_detail_community_post_delete(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        compost.delete()
        return redirect("comp:comp_community_detail", pk, pk2)

    return redirect("comp:comp_community_detail", pk, pk2)


# ----------------댓글---------------------


def comp_detail_community_comment_create(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        form = ComCommentForm(request.POST)
        if form.is_valid():
            comcomment = form.save(commit=False)
            comcomment.user = request.user
            comcomment.compost = compost
            comcomment.save()
            return redirect("comp:comp_community_detail", pk, pk2)
    else:
        form = ComCommentForm()
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_community_comment_create.html", ctx)


def comp_detail_community_comment_update(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    comcomment = ComComment.objects.filter(compost=compost).get(pk=pk3)

    if request.method == "POST":
        form = ComCommentForm(request.POST, instance=comcomment)
        if form.is_valid():
            form.save()
        return redirect("comp:comp_community_detail", pk, pk2)

    else:
        form = ComCommentForm(instance=comcomment)
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_community_comment_create.html", ctx)


def comp_detail_community_comment_delete(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    comcomment = ComComment.objects.filter(compost=compost).get(pk=pk3)

    if request.method == "POST":
        comcomment.delete()
        return redirect("comp:comp_community_detail", pk, pk2)

    return redirect("comp:comp_community_detail", pk, pk2)


# ----------------대댓글--------------------


def comp_detail_community_commcomment_create(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    comcomment = ComComment.objects.filter(compost=compost).get(pk=pk3)  # 대댓글 남길 댓글

    if request.method == "POST":
        form = ComCommentForm(request.POST)
        if form.is_valid():
            comcommcomment = form.save(commit=False)
            comcommcomment.user = request.user
            comcommcomment.compost = compost
            comcommcomment.commcomment = comcomment
            comcommcomment.save()
            return redirect("comp:comp_community_detail", pk, compost.pk)
    else:
        form = ComCommentForm()
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_community_comment_create.html", ctx)


def comp_detail_community_commcomment_delete(request, pk, pk2, pk3, pk4):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    comcomment = ComComment.objects.filter(compost=compost).get(pk=pk3)
    comcommcomment = ComComment.objects.filter(commcomment=comcomment).get(pk=pk4)

    if request.method == "POST":
        comcommcomment.delete()
        return redirect("comp:comp_community_detail", pk, pk2)

    return redirect("comp:comp_community_detail", pk, pk2)






def comp_ranking(request, pk):
    comp = Comp.objects.get(pk=pk)
    answers = comp.answer.order_by('rank')
    context = {
        "answers": answers
    }
    return render(request, 'comp/comp_ranking.html', context)


def comp_submit_answer(request, pk):
    if request.method == 'POST':

        if 1: #valid 파악


            answer = Answer()
            #answer.accuracy=
            #answer.rank=
            answer.user = request.user
            answer.comp = Comp.objects.get(pk=pk)
            answer.file = request.FILES.get('')
            answer.save()

        return redirect(reverse('comp_answerlist',kwargs={'pk': pk}))
    return render(request, 'comp/comp_submit_answer.html',)


def comp_answerlist(request,pk):

    ctx={
        'answer_list': Answer.objects.filter(user=request.user)
    }
    return render(request,'comp/comp_answerlist.html', ctx)