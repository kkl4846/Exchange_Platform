from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
app_name = 'user'


class User(AbstractBaseUser):
    nickname = models.CharField(max_length=20)
    university = models.ForeignKey(
        'domestic.Domestic', on_delete=models.SET_NULL, null=True, blank=True)
    user_email = models.EmailField(blank=True)
