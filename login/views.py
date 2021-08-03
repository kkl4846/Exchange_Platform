from django.conf import settings
# from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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


@login_required
def profile(request):
    return(request, 'login/profile.html')
