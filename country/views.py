import country
from django.shortcuts import render
from .models import Country, Foreign

# Create your views here.


def country_list(request):
    countries = Country.objects.all().order_by('country_name')
    
