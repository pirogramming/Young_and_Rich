import csv
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from comp.forms import ComPostForm, ComCommentForm, CompForm, FileFieldForm, CodePostForm, CodeCommentForm
from comp.models import Comp, ComPost, ComComment, CodePost, CodeComment, Comp_File, Answer  # Answer

from datetime import date
from comp.utils import *


# comp code 추가시 comp.team_number +1


def comp_list(request):
    qs = Comp.objects.all()
    qs_continue = Comp.objects.filter(continue_complete=0)
    qs_complete = Comp.objects.filter(continue_complete=1)
    q = request.GET.get("q", "")
    star_list = []

    if q:
        qs = Comp.objects.filter(title__icontains=q)

    qs_number = len(qs)

    comp_deadline_dict = {}
    for comp in qs:
        percent = date_percent(comp)
        comp_deadline_dict[comp.pk] = percent

        if comp.star.filter(id=request.user.id).exists():
            star_list.append(comp.id)

    ctx = {
        "comp_list": qs,
        "continue_comp_list": qs_continue,
        "complete_comp_list": qs_complete,
        "q": q,
        "comp_number": qs_number,
        "comp_deadline_dict": comp_deadline_dict,
        "star_list": star_list

    }
    return render(request, "comp/comp_list.html", ctx)


def comp_detail_overview(request, pk):
    comp = Comp.objects.get(pk=pk)
    percent = date_percent(comp)
    data = {
        "comp": comp,
        "percent": percent,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_overview.html", data)


def comp_detail_overview_evaluation(request, pk):
    comp = Comp.objects.get(pk=pk)
    percent = date_percent(comp)

    data = {
        "comp": comp,
        "percent": percent,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_overview_evaluation.html", data)


def comp_detail_overview_timeline(request, pk):
    comp = Comp.objects.get(pk=pk)
    percent = date_percent(comp)

    data = {
        "comp": comp,
        "percent": percent,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_overview_timeline.html", data)


def comp_detail_overview_prizes(request, pk):
    comp = Comp.objects.get(pk=pk)
    percent = date_percent(comp)

    data = {
        "comp": comp,
        "percent": percent,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_overview_prizes.html", data)


def comp_detail_data(request, pk):
    comp = Comp.objects.get(pk=pk)
    comp_filelist = Comp_File.objects.filter(comp=comp)
    ctx = {
        "comp": comp,
        "is_star": comp.is_star(request),
        "comp_filelist": comp_filelist,
    }
    return render(request, "comp/comp_detail_data.html", ctx)


# =========================커뮤니티===============================


def comp_detail_community_list(request, pk):
    comp = Comp.objects.get(pk=pk)
    qs = ComPost.objects.filter(comp=comp)
    q = request.GET.get("q", "")
    post_likelist = []
    if q:
        qs = qs.filter(title__icontains=q)

    comment_dict = {}
    for compost in qs:
        comment = ComComment.objects.filter(compost=compost)
        comment_dict[compost.id] = len(comment)

        if compost.like.filter(id=request.user.id).exists():
            post_likelist.append(compost.id)

    qs_number = len(qs)

    ctx = {
        "post_likelist": post_likelist,
        "comp": comp,
        "compost_list": qs,
        "q": q,
        "comment_dict": comment_dict,
        "compost_number": qs_number,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_community_list.html", ctx)


def comp_detail_community_detail(request, pk, pk2):  # pk == comp 번호, pk2 == post 번호
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.get(pk=pk2)
    comment_likelist = []

    if compost.like.filter(id=request.user.id).exists():
        is_liked = 1
    else:
        is_liked = 0

    list = ComComment.objects.filter(compost=compost)
    comment_list = []
    commcomment_list = []
    for comment in list:

        if comment.like.filter(id=request.user.id).exists():
            comment_likelist.append(comment.id)

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
        "is_liked": is_liked,
        "comment_likelist": comment_likelist,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_community_detail.html", ctx)


# ----------------포스트--------------------


def comp_detail_community_post_create(request, pk):
    comp = Comp.objects.get(pk=pk)
    if request.method == "POST":
        form = ComPostForm(request.POST)

        if form.is_valid():
            compost = form.save(commit=False)
            compost.user = request.user
            compost.comp = comp
            compost.save()
            return redirect("comp:comp_community_detail", pk, compost.pk)
    else:
        form = ComPostForm()
        ctx = {
            "form": form,
            "is_star": comp.is_star(request),
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
            "is_star": comp.is_star(request),
        }
        return render(request, "comp/comp_detail_community_post_create.html", ctx)


def comp_detail_community_post_delete(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    compost = ComPost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        compost.delete()
        return redirect("comp:comp_community_list", pk)

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
            "is_star": comp.is_star(request),
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
            "is_star": comp.is_star(request),
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
            "is_star": comp.is_star(request),
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
    answers = comp.answer.filter(is_selected=1).order_by('-accuracy')
    context = {
        "answers": answers,
        "is_star": comp.is_star(request),
    }
    return render(request, 'comp/comp_ranking.html', context)


# ===========================코드===================================


def comp_detail_code_list(request, pk):
    comp = Comp.objects.get(pk=pk)
    codepost_list = CodePost.objects.filter(comp=comp)
    post_likelist = []

    q = request.GET.get("q", "")  # 검색
    if q:
        codepost_list = codepost_list.filter(title__icontains=q)

    codepost_number = len(codepost_list)

    comment_dict = {}
    for codepost in codepost_list:
        comment = CodeComment.objects.filter(codepost=codepost)
        comment_dict[codepost.id] = len(comment)

        if codepost.like.filter(id=request.user.id).exists():
            post_likelist.append(codepost.id)

    ctx = {
        "comp": comp,
        "code_list": codepost_list,
        "codepost_number": codepost_number,
        "comment_dict": comment_dict,
        "post_likelist": post_likelist,
        "is_star": comp.is_star(request),
    }
    return render(request, "comp/comp_detail_code_list.html", ctx)


def comp_detail_code_detail(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.get(pk=pk2)

    comment_likelist = []

    if codepost.like.filter(id=request.user.id).exists():
        is_liked = 1
    else:
        is_liked = 0

    list = CodeComment.objects.filter(codepost=codepost)
    comment_list = []
    commcomment_list = []
    for comment in list:
        if not comment.commcomment:
            comment_list.append(comment)
        else:
            commcomment_list.append(comment)

        if comment.like.filter(id=request.user.id).exists():
            comment_likelist.append(comment.id)

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
        "is_liked": is_liked,
        "comment_likelist": comment_likelist,
        "is_star": comp.is_star(request),

    }
    return render(request, "comp/comp_detail_code_detail.html", ctx)


# -----------------------포스트-------------------------


def comp_detail_code_post_create(request, pk):
    comp = Comp.objects.get(pk=pk)
    if request.method == "POST":
        form = CodePostForm(request.POST)
        if form.is_valid():
            codepost = form.save(commit=False)
            codepost.user = request.user
            codepost.comp = comp
            codepost.save()
            return redirect("comp:comp_code_detail", pk, codepost.pk)
    else:
        form = CodePostForm()
        ctx = {
            "form": form,
            "is_star": comp.is_star(request),
        }
        return render(request, "comp/comp_detail_code_post_create.html", ctx)


def comp_detail_code_post_update(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        form = CodePostForm(request.POST, instance=codepost)
        if form.is_valid():
            form.save()
        return redirect("comp:comp_code_detail", pk, pk2)

    else:
        form = CodePostForm(instance=codepost)
        ctx = {
            "form": form,
            "is_star": comp.is_star(request),
        }
        return render(request, "comp/comp_detail_code_post_create.html", ctx)


def comp_detail_code_post_delete(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        codepost.delete()
        return redirect("comp:comp_code_list", pk)

    return redirect("comp:comp_code_detail", pk, pk2)


# ------------------댓글---------------------


def comp_detail_code_comment_create(request, pk, pk2):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)

    if request.method == "POST":
        form = CodeCommentForm(request.POST)
        if form.is_valid():
            codecomment = form.save(commit=False)
            codecomment.user = request.user
            codecomment.codepost = codepost
            codecomment.save()
            return redirect("comp:comp_code_detail", pk, pk2)
    else:
        form = ComCommentForm()
        ctx = {
            "form": form,
            "is_star": comp.is_star(request),
        }
        return render(request, "comp/comp_detail_code_comment_create.html", ctx)


def comp_detail_code_comment_update(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    codepost = ComPost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = ComComment.objects.filter(codepost=codepost).get(pk=pk3)

    if request.method == "POST":
        form = CodeCommentForm(request.POST, instance=codecomment)
        if form.is_valid():
            form.save()
        return redirect("comp:comp_community_detail", pk, pk2)

    else:
        form = CodeCommentForm(instance=codecomment)
        ctx = {
            "form": form,
            "is_star": comp.is_star(request),
        }
        return render(request, "comp/comp_detail_code_comment_create.html", ctx)


def comp_detail_code_comment_delete(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = ComComment.objects.filter(codepost=codepost).get(pk=pk3)

    if request.method == "POST":
        codecomment.delete()
        return redirect("comp:comp_code_detail", pk, pk2)

    return redirect("comp:comp_code_detail", pk, pk2)


# ----------------대댓글--------------------


def comp_detail_code_commcomment_create(request, pk, pk2, pk3):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = CodeComment.objects.filter(codepost=codepost).get(pk=pk3)  # 대댓글 남길 댓글

    if request.method == "POST":
        form = CodeCommentForm(request.POST)
        if form.is_valid():
            codecommcomment = form.save(commit=False)
            codecommcomment.user = request.user
            codecommcomment.codepost = codepost
            codecommcomment.commcomment = codecomment
            codecommcomment.save()
            return redirect("comp:comp_code_detail", pk, codepost.pk)
    else:
        form = CodeCommentForm()
        ctx = {
            "form": form,
            "is_star": comp.is_star(request),
        }
        return render(request, "comp/comp_detail_code_comment_create.html", ctx)


def comp_detail_code_commcomment_delete(request, pk, pk2, pk3, pk4):
    comp = Comp.objects.get(pk=pk)
    codepost = CodePost.objects.filter(comp=comp).get(pk=pk2)
    codecomment = CodeComment.objects.filter(codepost=codepost).get(pk=pk3)
    codecommcomment = CodeComment.objects.filter(commcomment=codecomment).get(pk=pk4)

    if request.method == "POST":
        codecommcomment.delete()
        return redirect("comp:comp_code_detail", pk, pk2)

    return redirect("comp:comp_code_detail", pk, pk2)


# ----------------답안제출 및 채점--------------------

def user_upload_csv(request, pk):
    accuracy = ''
    data = {
        'pk': pk
    }
    if request.method == 'GET':
        return render(request, "comp/comp_csv_upload.html", data)

    if request.method == 'POST':
        submit_answer_list = []
        submit_problem_list = []

        try:
            submit_answer = request.FILES["csv_file"]
            # csv 파일이 맞는지 검사하는 validation
            if not submit_answer.name.endswith('.csv'):
                messages.error(request, 'CSV파일이 아닙니다.')
                return redirect("comp:user_upload_csv", data)

            # # 파일이 너무 큰지 검사하는 과정
            # if submit_answer.multiple_chunks():
            #     messages.error(request, "파일이 너무 큽니다")
            #     return redirect("comp:user_upload_csv")

            submit_answer_data = submit_answer.read().decode("utf-8")
            lines = submit_answer_data.split("\n")[:-1]

            for line in lines:
                fields = line.split(",")
                submit_problem_list.append(fields[0].rstrip('\r'))
                submit_answer_list.append(fields[1].rstrip('\r'))

            with open(Comp.objects.get(pk=pk).comp_answer.url[1:], 'r', encoding='UTF-8') as answer_sheet_file:
                # open 함수에 [1:] 넣은 이유는 저 url 은 /media/ 로 시작을 하는 반면, open으로 읽을 때에는 맨 앞의 / 를 인식하지 않아서!
                readers = csv.reader(answer_sheet_file)
                reader = list(readers)
                answer_list = list(map(lambda x: x[1], reader))
                problem_list = list(map(lambda x: x[0], reader))
                # 인코딩 안하면 첫글자에서 에러가 나고, list 로 미리 선언을 해주지 않고 람다에서 선언을 해주면 reader 객체를 한번밖에 못씀

            # 답안 제출 형식(문제 번호가 일치하는지)이 제대로 되었는지 검사하는 과정
            for i, each_problem in enumerate(problem_list):
                if not each_problem == submit_problem_list[i]:
                    messages.error(request, '제출한 답안의 problem_set이 올바른지 확인하세요. 제출한 답안의 {}번째 열을 확인하세요'.format(i))
                    return redirect("comp:user_upload_csv", data)
            # 답안 제출 형식(답 개수가 일지하는지)이 제대로 되었는지 검사하는 과정
            if not len(answer_list) == len(submit_answer_list):
                messages.error(request, '제출한 답안의 수가 일치하지 않습니다. 답안은 총 {}열이어야 합니다.'.format(len(answer_list)))
                return redirect("comp:user_upload_csv", data)

            # 답안의 정답률을 계산하는 과정
            correct = 0
            for i, each_answer in enumerate(answer_list):
                if each_answer == submit_answer_list[i]:
                    correct += 1

            accuracy = correct / len(answer_list)

            answer = Answer()
            answer.accuracy = accuracy
            answer.rank = 153
            answer.user = request.user
            answer.comp = Comp.objects.get(pk=pk)
            answer.file = submit_answer
            answer.save()

        except Exception as e:
            messages.error(request, "파일을 업로드 할 수 없습니다. 다시 업로드해주세요!" + repr(e))
            return render(request, "comp/comp_csv_upload.html", data)

        return render(request, "comp/comp_csv_result.html", {
            'accuracy': accuracy,
            'user': request.user,
            'answer_list': Answer.objects.filter(user=request.user, comp=Comp.objects.get(pk=pk)).order_by(
                'created_at'),
            'pk': pk
        })


def show_csv_result(request, pk):
    return render(request, "comp/comp_csv_result.html", {
        'answer_list': Answer.objects.filter(comp=Comp.objects.get(pk=pk)).order_by('created_at'),
        "pk": pk,
    })


# 대회 deadline 날짜가 되면 대회를 완료 대회로 바꾸고, 순위에 따라 user 에게 메달을 부여한다.
# 1. if문으로 deadline날짜 판별
# 2. deadline == today 이면 대회를 완료 상태로 내리기
# + comp의 answer의 rank로 필터를 걸어서 해당 user 가져온다
# + 그 후, 해당 유저의 메달 리스트에 추가


# def create_comp(request):
#     if request.method == 'POST':
#         fileform = FileFieldForm(request.POST, request.FILES)
#         compform = CompForm(request.POST, request.FILES)
#
#         if fileform.is_valid() and compform.is_valid():
#             files = request.FILES.getlist('file_field')
#
#             comp = compform.save
#             comp.user = request.user
#             comp.save
#
#             for f in files:
#                 file = Comp_File()
#                 file.file = f
#                 file.comp = comp
#                 file.save()
#             return HttpResponseRedirect('')
#     else:
#         fileform = FileFieldForm
#         compform = CompForm
#     return render(request, 'comp/create_comp.html', {'fileform': fileform, 'compform': compform})


@require_POST
def like_upload(request):
    pk = request.POST.get('pk', None)
    liketype = request.POST.get('liketype', None)
    request.user  # 로그인여부확인
    if liketype == 'cop':
        target = get_object_or_404(ComPost, pk=pk)
    elif liketype == 'coc':
        target = get_object_or_404(ComComment, pk=pk)
    elif liketype == 'cdp':
        target = get_object_or_404(CodePost, pk=pk)
    elif liketype == 'cdc':
        target = get_object_or_404(CodeComment, pk=pk)

    if target.like.filter(id=request.user.id).exists():
        target.like.remove(request.user)

    else:
        target.like.add(request.user)

    ctx = {
        'like': target.like.count(),
    }

    return JsonResponse(ctx)


@require_POST
def star_upload(request):
    print('r')

    request.user  # 로그인확인
    pk = request.POST.get('pk', None)

    target = get_object_or_404(Comp, pk=pk)

    if target.star.filter(id=request.user.id).exists():
        target.star.remove(request.user)
    else:
        target.star.add(request.user)

    return JsonResponse({})


def comment_create_ajax(request):
    compost_pk = request.POST.get('compost_pk', None)
    comcomment_pk = request.POST.get('comcomment_pk', None)

    newcomcomment = ComComment()
    newcomcomment.compost = ComPost.objects.get(pk=compost_pk)
    newcomcomment.commcomment = ComComment.objects.get(pk=comcomment_pk)
    newcomcomment.user = request.user
    newcomcomment.context = request.POST.get('context')
    newcomcomment.save()

    ctx = {
        'context': newcomcomment.context,
    }
    return JsonResponse(ctx)


@require_POST
def answer_checkbox_upload(request):
    request.user

    pk=request.POST.get('pk',None)
    print(pk)
    target = get_object_or_404(Answer, pk=pk)

    if target.is_selected == 1:
        target.is_selected = 0
    else:
        target.is_selected = 1
    target.save()
    return JsonResponse({'is_selected': target.is_selected})


def comp_ranking(request, pk):
    comp = Comp.objects.get(pk=pk)
    user = User.objects.all()
    answer_lst = comp.answer.filter(is_selected=1).order_by('user_id', '-accuracy')
    answerdict = dict()
    sorted_answerdict = dict()

    try:
        answerdict[answer_lst[0].user_id] = answer_lst[0].accuracy
    except IndexError:
        pass

    else:
        for i in range(answer_lst.count() - 1):
            if answer_lst[i].user_id != answer_lst[i + 1].user_id:
                answerdict[answer_lst[i + 1].user_id] = answer_lst[i + 1].accuracy
        sorted_answerlst = sorted(answerdict.items(), key=operator.itemgetter(1))

        for j in sorted_answerlst:
            sorted_answerdict[j[0]] = j[1]

    context = {
        "answers": sorted_answerdict,
        "is_star": comp.is_star(request),
        "comp": comp,
        "user_list": user,
    }
    return render(request, 'comp/comp_ranking.html', context)

def codecomment_create_ajax(request):
    codepost_pk = request.POST.get('codepost_pk', None)
    codecomment_pk = request.POST.get('codecomment_pk', None)

    newcodecomment = CodeComment()
    newcodecomment.codepost = CodePost.objects.get(pk=codepost_pk)
    newcodecomment.commcomment = CodeComment.objects.get(pk=codecomment_pk)
    newcodecomment.user = request.user
    newcodecomment.context = request.POST.get('context')
    newcodecomment.save()

    ctx = {
        'context': newcodecomment.context,
    }
    return JsonResponse(ctx)
