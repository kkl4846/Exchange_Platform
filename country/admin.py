from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass
