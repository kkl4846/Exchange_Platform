from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Question)
class CustomQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CustomCommentAdmin(admin.ModelAdmin):
    pass
