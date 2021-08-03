from django.shortcuts import get_object_or_404, render, redirect
from . import models
from . import forms
def univ_list(request):
    all_univ=models.Foreign.objects.all()
    return render(request,'templates/foreign/univ_list',{
        'all_univ':all_univ,
    })


def wiki(request,pk):
    univ=models.Foreign.objects.get(pk=pk)
    ctx={
        'univ':univ,
    }
    return render(request,'foreign/wiki.html',ctx)

def wiki_edit_apply(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        form.language_score=foreign.language_score              
        # form.course_enroll=foreign.course_enroll
        # form.accommodation=foreign.accommodation
        # form.atmosphere=foreign.atmosphere
        # form.club=foreign.club
        # form.away_scholarship=foreign.away_scholarship
        if form.is_valid():
            foreign.language_score=form.language_score
            foreign.save()
            # foreign=form.save()                                 #왜 save하면 위에 form.language_score...이 저장이 안될까... 클린코드해보자..
            # foreign.language_score=form.language_score
            # foreign.course_enroll=form.course_enroll
            # foreign.accommodation=form.accommodation
            # foreign.atmosphere=form.atmosphere
            # foreign.club=form.club
            # foreign.away_scholarship=form.away_scholarship
            # foreign.save()
            # print(foreign.language_score)
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit_apply.html',{
        'form':form,
        'univ':foreign,
    })

def wiki_edit_language_score(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        form.away_apply=foreign.away_apply
        # form.course_enroll=foreign.course_enroll
        # form.accommodation=foreign.accommodation
        # form.atmosphere=foreign.atmosphere
        # form.club=foreign.club
        # form.away_scholarship=foreign.away_scholarship
        if form.is_valid():
            foreign.away_apply=form.away_apply
            foreign.save()
            # foreign.away_apply=form.away_apply
            # foreign.course_enroll=form.course_enroll
            # foreign.accommodation=form.accommodation
            # foreign.atmosphere=form.atmosphere
            # foreign.club=form.club
            # foreign.away_scholarship=form.away_scholarship
            # foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit_language_score.html',{
        'form':form,
        'univ':foreign,
    })

