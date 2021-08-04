# from django.contrib.auth import login as auth_login
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models, forms
from django.contrib import auth


def user_main(request):
    ctx = {"user_main": user_main}
    return render(request, 'login/main.html', context=ctx)


def signup(request):
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            new_user = models.User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'], nickname=request.POST['nickname'], email=request.POST['email'])
            auth.login(request, new_user)
            return redirect('login:user_main')
    else:
        form = forms.SignupForm()
        return render(request, 'login/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('login:user_main')
        else:
            return render(request, 'login/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'login/login.html')


@login_required
def profile(request):
    return render(request, 'login/user_main.html')
