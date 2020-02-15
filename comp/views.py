import csv

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comp.forms import ComPostForm, ComCommentForm, CompForm, FileFieldForm
from comp.models import Comp, ComPost, ComComment, CodePost, CodeComment, Comp_File, Answer  # Answer

from datetime import date


# comp code 추가시 comp.team_number +1
def comp_list(request):
    qs = Comp.objects.all()
    q = request.GET.get("q", "")
    if q:
        qs = Comp.objects.filter(title__icontains=q)

    qs_number = len(qs)

    today = date.today()
    comp_deadline_dict = {}
    for comp in qs:
        created_date = comp.created_at
        dead_date = comp.deadline
        total = (dead_date - created_date).days
        interval = (today - created_date).days
        percent = round(interval / total, 2) * 100

        comp_deadline_dict[comp.pk] = percent
    print(comp_deadline_dict)

    ctx = {
        "comp_list": qs,
        "q": q,
        "comp_number": qs_number,
        "comp_deadline_dict": comp_deadline_dict,
    }
    return render(request, "comp/comp_list.html", ctx)


def comp_detail_overview(request, pk):
    comp = Comp.objects.get(pk=pk)
    today = date.today()

    created_date = comp.created_at
    dead_date = comp.deadline
    total = (dead_date - created_date).days
    interval = (today - created_date).days
    percent = round(interval / total, 2) * 100
    print(percent)

    data = {
        "comp": comp,
        "percent": percent,
    }
    return render(request, "comp/comp_detail_overview.html", data)


def comp_detail_overview_evaluation(request, pk):
    comp = Comp.objects.get(pk=pk)
    today = date.today()

    created_date = comp.created_at
    dead_date = comp.deadline
    total = (dead_date - created_date).days
    interval = (today - created_date).days
    percent = round(interval / total, 2) * 100
    print(percent)

    data = {
        "comp": comp,
        "percent":percent,
    }
    return render(request, "comp/comp_detail_overview_evaluation.html", data)


def comp_detail_overview_timeline(request, pk):
    comp = Comp.objects.get(pk=pk)
    today = date.today()

    created_date = comp.created_at
    dead_date = comp.deadline
    total = (dead_date - created_date).days
    interval = (today - created_date).days
    percent = round(interval / total, 2) * 100
    print(percent)

    data = {
        "comp": comp,
        "percent": percent,
    }
    return render(request, "comp/comp_detail_overview_timeline.html", data)


def comp_detail_overview_prizes(request, pk):
    comp = Comp.objects.get(pk=pk)
    today = date.today()

    created_date = comp.created_at
    dead_date = comp.deadline
    total = (dead_date - created_date).days
    interval = (today - created_date).days
    percent = round(interval / total, 2) * 100
    print(percent)

    data = {
        "comp": comp,
        "percent": percent,
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
    dead_date = comp.deadline
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
                return redirect("comp:user_upload_csv")

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

            with open('answer_sheet.csv', 'r', encoding='UTF-8') as answer_sheet_file:
                # 여기서 오픈할 파일 경로를 정해주면 돼여! 이건 기업이 제출한거에 따라 달렸지
                readers = csv.reader(answer_sheet_file)
                reader = list(readers)
                answer_list = list(map(lambda x: x[1], reader))
                problem_list = list(map(lambda x: x[0], reader))
                # 인코딩 안하면 첫글자에서 에러가 나고, list 로 미리 선언을 해주지 않고 람다에서 선언을 해주면 reader 객체를 한번밖에 못씀

            # 답안 제출 형식(문제 번호가 일치하는지)이 제대로 되었는지 검사하는 과정
            for i, each_problem in enumerate(problem_list):
                if not each_problem == submit_problem_list[i]:
                    messages.error(request, '제출한 답안의 problem_set이 올바른지 확인하세요. 제출한 답안의 {}번째 열을 확인하세요'.format(i))
                    return redirect("comp:user_upload_csv")
            # 답안 제출 형식(답 개수가 일지하는지)이 제대로 되었는지 검사하는 과정
            if not len(answer_list) == len(submit_answer_list):
                messages.error(request, '제출한 답안의 수가 일치하지 않습니다. 답안은 총 {}열이어야 합니다.'.format(len(answer_list)))
                return redirect("comp:user_upload_csv")

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
            return render(request, "comp/comp_csv_upload.html")

        return render(request, "comp/comp_csv_result.html", {
            'accuracy': accuracy,
            'user': request.user,
            'answer_list': Answer.objects.filter(user=request.user, comp=Comp.objects.get(pk=pk)).order_by('created_at'),
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


def comp_explanation(request):
    return render(request, 'comp/explanation.html')


def comp_explanation_page(request):
    return render(request, 'comp/explanation_page.html')


def comp_explanation_competition(request):
    return render(request, 'comp/explanation_competition.html')


def comp_explanation_faq(request):
    return render(request, 'comp/explanation_faq.html')


def create_comp(request):
    if request.method == 'POST':
        fileform = FileFieldForm(request.POST, request.FILES)
        compform = CompForm(request.POST, request.FILES)

        if fileform.is_valid() and compform.is_valid():
            files = request.FILES.getlist('file_field')

            comp = compform.save
            comp.user = request.user
            comp.save

            for f in files:
                file = Comp_File()
                file.file = f
                file.comp = comp
                file.save()
            return HttpResponseRedirect('')
    else:
        fileform = FileFieldForm
        compform = CompForm
    return render(request, 'comp/create_comp.html', {'fileform': fileform, 'compform': compform})
