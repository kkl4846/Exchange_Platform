import country
from django.shortcuts import get_object_or_404, redirect, render
from jamo import h2j, j2hcj
from .models import Country
from .forms import *

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
    country = get_object_or_404(Country, pk=pk)
    return render(request, 'country/country_wiki.html', {
        'country': country
    })


# wiki 1번 항목

def wiki_edit_visa(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'btn': 1,
    })


def wiki_edit_lifestyle(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'btn': 2,
    })


def wiki_edit_money(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'btn': 3,
    })


def wiki_edit_culture(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'btn': 4,
    })


def wiki_edit_covid_info(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'btn': 5,
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
