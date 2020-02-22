from django.shortcuts import render


def main(request):
    return render(request, 'main/main.html')


def explanation_page(request):
    return render(request, 'main/explanation_page.html')


def explanation_competition(request):
    return render(request, 'main/explanation_competition.html')


def explanation_faq(request):
    return render(request, 'main/explanation_faq.html')
