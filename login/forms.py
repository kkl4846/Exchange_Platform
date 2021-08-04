# from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class SignupForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ('username', 'nickname', 'email')
