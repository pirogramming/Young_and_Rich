from django.shortcuts import render


def main(request):
    return render(request, 'main/main.html')
