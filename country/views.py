import country
from django.shortcuts import render
from .models import Country
from jamo import h2j, j2hcj

# Create your views here.


def country_list(request):
    countries = Country.objects.all().order_by('country_name')
    countries_dict = {}
    last_cho = 'ㄱ'

    for c in countries:
        this_country = c.country_name
        country_cho = j2hcj(h2j(this_country[0]))[0]
        if last_cho != country_cho:     # 직전 초성과 다른 초성
            countries_dict[country_cho] = [this_country]
            last_cho = country_cho
        else:                           # 같은 초성
            countries_dict[country_cho].append(this_country)
    
    print(countries_dict)

    return render(request, 'country/country_list.html', {'countries_dict': countries_dict})
