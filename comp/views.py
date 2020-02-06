from django.shortcuts import render, get_object_or_404

from comp.models import Comp

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
