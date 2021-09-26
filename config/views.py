from django.shortcuts import render


def ads(request):
    return render(request, 'ads.txt')
