import country
from django.shortcuts import get_object_or_404, redirect, render
from .models import Country
from jamo import h2j, j2hcj

# Create your views here.


def country_list(request):
    countries = Country.objects.all().order_by('country_name')
    countries_dict = {}
    last_cho = 'ㄱ'
    countries_dict[last_cho] = []

    for c in countries:
        this_country = c.country_name
        country_cho = j2hcj(h2j(this_country[0]))[0]
        if last_cho != country_cho:     # 직전 초성과 다른 초성   
            countries_dict[country_cho] = []
            countries_dict[country_cho].append(c)
            last_cho = country_cho
        else:                           # 같은 초성
            countries_dict[country_cho].append(c)
    g_cho = 'ㄱ'
    if len(countries_dict[g_cho]) == 0:
        del(countries_dict[g_cho])
    # print(countries_dict)

    return render(request, 'country/country_list.html', {'countries_dict': countries_dict})


def country_wiki(request, pk):
    return render(request, 'country/country_wiki.html', {
        
    })



def country_univ(request, pk):      # 각국의 대학 목록
    country = get_object_or_404(Country, pk=pk)
    unives = country.foriegn_set.all()

    return render(request, 'country/country_univ.html', {
        'unives': unives
    })


def country_qna(request, pk):
    return render(request, 'country/country_qna.html', {
        
    })
