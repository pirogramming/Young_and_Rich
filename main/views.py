from django.shortcuts import render
from .utils import *
from comp.models import Comp


def main(request):
    prize = count_prize()
    user = count_user()
    company = count_company()
    competition = count_competition()

    ctx = {
        'user': user,
        'prize': prize,
        'company': company,
        'competition': competition,
    }

    return render(request, 'main/main.html', ctx)


def explanation(request):
    return render(request, 'main/explanation.html')


def explanation_page(request):
    return render(request, 'main/explanation_page.html')


def explanation_competition(request):
    return render(request, 'main/explanation_competition.html')


def explanation_faq(request):
    return render(request, 'main/explanation_faq.html')

