from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comp.forms import ComPostForm, ComCommentForm
from comp.models import Comp, ComPost, ComComment, CodePost, CodeComment  # Answer

from datetime import date


# comp code 추가시 comp.team_number +1
def comp_list(request):
    qs = Comp.objects.all()
    q = request.GET.get("q", "")
    if q:
        qs = Comp.objects.filter(title__icontains=q)

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
    o = Comp.objects.get(pk=pk)
    data = {
        "o": o,
    }
    return render(request, "comp/comp_detail_overview_description.html", data)


def comp_detail_overview_evaluation(request, pk):
    o = Comp.objects.get(pk=pk)
    data = {
        "o": o,
    }
    return render(request, "comp/comp_detail_overview_evaluation.html", data)


def comp_detail_overview_timeline(request, pk):
    o = Comp.objects.get(pk=pk)
    data = {
        "o": o,
    }
    return render(request, "comp/comp_detail_overview_timeline.html", data)


def comp_detail_overview_prizes(request, pk):
    o = Comp.objects.get(pk=pk)
    data = {
        "o": o,
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


# ===========================코드===================================


def comp_detail_code_list(request, pk):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp)

    q = request.GET.get("q", "")  # 검색
    if q:
        codepost = codepost.filter(title__icontains=q)

    codepost_number = len(codepost)

    ctx = {
        "comp": comp,
        "code_list": codepost,
        "codepost_number": codepost_number,
    }
    return render(request, "comp/comp_detail_code_list.html", ctx)


def comp_detail_code_detail(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)

    list = CodeComment.objects.filter(codepost=codepost)
    comment_list = []
    commcomment_list = []
    for comment in list:
        if not comment.commcomment:
            comment_list.append(comment)
        else:
            commcomment_list.append(comment)

    count_comment = len(comment_list) + len(commcomment_list)
    is_post_user = 1

    if codepost.user == request.user:
        is_post_user = 0

    ctx = {
        "comp": comp,
        "codepost": codepost,
        "comment_list": comment_list,
        "commcomment_list": commcomment_list,
        "count_comment": count_comment,
        "is_post_user": is_post_user,
    }
    return render(request, "comp/comp_detail_code_detail.html", ctx)


# -----------------------포스트-------------------------


def comp_detail_code_post_create(request, pk):
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


def comp_detail_code_post_update(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        form = ComPostForm(request.POST, instance=codepost)
        if form.is_valid():
            form.save()
        return redirect("comp:comp_community_detail", pk, pk2)

    else:
        form = ComPostForm(instance=codepost)
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_community_post_create.html", ctx)


def comp_detail_code_post_delete(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = ComPost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        codepost.delete()
        return redirect("comp:comp_code_detail", pk, pk2)

    return redirect("comp:comp_code_detail", pk, pk2)


# ------------------댓글---------------------


def comp_detail_code_comment_create(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        form = ComCommentForm(request.POST)
        if form.is_valid():
            comcomment = form.save(commit=False)
            comcomment.user = request.user
            comcomment.compost = codepost
            comcomment.save()
            return redirect("comp:comp_code_detail", pk, pk2)
    else:
        form = ComCommentForm()
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_code_comment_create.html", ctx)


def comp_detail_code_comment_update(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    codepost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = ComComment.objects.filter(codepost=codepost).get(pk=pk3)

    if request.method == "POST":
        form = ComCommentForm(request.POST, instance=codecomment)
        if form.is_valid():
            form.save()
        return redirect("comp:comp_community_detail", pk, pk2)

    else:
        form = ComCommentForm(instance=codecomment)
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_code_comment_create.html", ctx)


def comp_detail_code_comment_delete(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    codepost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = ComComment.objects.filter(codepost=codepost).get(pk=pk3)

    if request.method == "POST":
        codecomment.delete()
        return redirect("comp:comp_community_detail", pk, pk2)

    return redirect("comp:comp_community_detail", pk, pk2)


# ----------------대댓글--------------------


def comp_detail_code_commcomment_create(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    codepost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = ComComment.objects.filter(compost=codepost).get(pk=pk3)  # 대댓글 남길 댓글

    if request.method == "POST":
        form = ComCommentForm(request.POST)
        if form.is_valid():
            comcommcomment = form.save(commit=False)
            comcommcomment.user = request.user
            comcommcomment.compost = codepost
            comcommcomment.commcomment = codecomment
            comcommcomment.save()
            return redirect("comp:comp_community_detail", pk, codepost.pk)
    else:
        form = ComCommentForm()
        ctx = {
            "form": form,
        }
        return render(request, "comp/comp_detail_code_comment_create.html", ctx)


def comp_detail_code_commcomment_delete(request, pk, pk2, pk3, pk4):
    comp = Comp.objects.get(pk=pk)
    codepost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = ComComment.objects.filter(codepost=codepost).get(pk=pk3)
    codecommcomment = ComComment.objects.filter(commcomment=codecomment).get(pk=pk4)

    if request.method == "POST":
        codecommcomment.delete()
        return redirect("comp:comp_community_detail", pk, pk2)

    return redirect("comp:comp_community_detail", pk, pk2)




















# 대회 deadline 날짜가 되면 대회를 완료 대회로 바꾸고, 순위에 따라 user 에게 메달을 부여한다.
# 1. if문으로 deadline날짜 판별
# 2. deadline == today 이면 대회를 완료 상태로 내리기
# + comp의 answer의 rank로 필터를 걸어서 해당 user 가져온다
# + 그 후, 해당 유저의 메달 리스트에 추가


# def comp_submit_answer(request, pk):
#     if request.method == 'POST':
#
#         if 1:  # valid 파악
#             answer = Answer()
#             # answer.accuracy=
#             # answer.rank=
#             answer.user = request.user
#             answer.comp = Comp.objects.get(pk=pk)
#             answer.file = request.FILES.get('')
#             answer.save()
#
#         return redirect(reverse('comp_answerlist', kwargs={'pk': pk}))
#     return render(request, 'comp/comp_submit_answer.html', )
#
#
# def comp_answerlist(request, pk):
#     ctx = {
#         'answer_list': Answer.objects.filter(user=request.user)
#     }
#     return render(request, 'comp/comp_answerlist.html', ctx)


def comp_explanation(request):
    return render(request, 'comp/explanation.html')
