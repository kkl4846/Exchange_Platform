from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, verbose_name='아이디', unique=True,
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    nickname = models.CharField(max_length=20, verbose_name='닉네임', unique=True)
    university = models.ForeignKey(
        'domestic.Domestic', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='소속 대학')
    email = models.EmailField(blank=True, verbose_name='이메일', unique=True)
    school_certificate = models.BooleanField(
        verbose_name='학교 인증 여부', default=False)
    USERNAME_FIELD = 'username'
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()
