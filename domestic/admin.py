from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Domestic)
class CustomDomesticAdmin(admin.ModelAdmin):
    pass

@admin.register(models.DQuestion)
class CustomDQuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.DComment)
class CustomDCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Credit)
class CustomCreditAdmin(admin.ModelAdmin):
    pass