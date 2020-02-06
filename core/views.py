from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('core:profile')  # change to main page
        else:
            return render(request, 'account/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'account/login.html')

def profile(request):
    return render(request, 'account/profile.html')
