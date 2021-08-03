from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, verbose_name='아이디', unique=True,
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    nickname = models.CharField(max_length=20, verbose_name='닉네임', unique=True)
    university = models.ForeignKey(
        'domestic.Domestic', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='소속 대학')
    user_email = models.EmailField(blank=True, verbose_name='이메일', unique=True)
    USERNAME_FIELD = 'username'
