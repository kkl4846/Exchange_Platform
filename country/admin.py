from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CQuestion)
class CustomCQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CComment)
class CustomCCommentAdmin(admin.ModelAdmin):
    pass
