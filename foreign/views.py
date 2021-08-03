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
        if form.is_valid():
            foreign=form.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':1,
    })

def wiki_edit_language_score(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        if form.is_valid():   
            foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':2,
    })

def wiki_edit_course_enroll(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        if form.is_valid():   
            foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':3,
    })


def wiki_edit_accommodation(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        if form.is_valid():   
            foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':4,
    })


def wiki_edit_atmosphere(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        if form.is_valid():   
            foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':5,
    })


def wiki_edit_club(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        if form.is_valid():   
            foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':6,
    })


def wiki_edit_away_scholarship(request,pk):
    foreign=get_object_or_404(models.Foreign,pk=pk)
    if request.method=='POST':
        form=forms.ForeignForm(request.POST,request.FILES,instance=foreign)
        if form.is_valid():   
            foreign.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit.html',{
        'form':form,
        'univ':foreign,
        'btn':7,
    })


