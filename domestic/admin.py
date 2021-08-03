from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Domestic)
class CustomDomesticAdmin(admin.ModelAdmin):
    pass
