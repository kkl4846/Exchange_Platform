from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Foreign)
class CustomIdeaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Post)
class CustomIdeaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CustomIdeaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FQuestion)
class CustomFQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FComment)
class CustomFCommentAdmin(admin.ModelAdmin):
    pass
