import foreign

import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import *

# Create your views here.

def univ_list(request):
    unives = Foreign.objects.all().order_by('away_name')
    univ_dict = {}
    last_alpha = 'A'
    univ_dict[last_alpha] = []

    for univ in unives:
        u = univ.away_name
        this_alpha = u[0]
        if last_alpha != this_alpha:
            univ_dict[this_alpha] = []
            univ_dict[this_alpha].append(u)
            last_alpha = this_alpha
        else:
            univ_dict[this_alpha].append(u)


    return render(request, 'templates/foreign/univ_list', {
        'univ_dict': univ_dict
    })