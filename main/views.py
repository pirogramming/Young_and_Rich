from django.shortcuts import render

from main.models import Notice


def main(request):
    return render(request, 'main/main.html')


def notice_list(request):
    notice_list= Notice.objects.all()
    ctx={
        'notice_list':notice_list,
    }
    return render(request,'main/notice_list.html',ctx)


def notice_detail(request, pk):
    notice = Notice.objects.get(pk=pk)
    notice.view_num+=1
    notice.save()
    ctx={'notice':notice,
         }
    return render(request, 'main/notice_detail.html',ctx)