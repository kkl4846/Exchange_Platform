from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
app_name = 'user'


class User(AbstractBaseUser):
    nickname = models.CharField(max_length=20, verbose_name='닉네임')
    university = models.ForeignKey(
        'domestic.Domestic', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='소속 대학')
    user_email = models.EmailField(blank=True, verbose_name='이메일')
