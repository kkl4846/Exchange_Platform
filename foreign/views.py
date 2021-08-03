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
        form.away_name=foreign.away_name
        print(form.errors)
        if form.is_valid():
            foreign=form.save()
            return redirect('foreign:wiki',foreign.pk)
    else:
        form=forms.ForeignForm(instance=foreign)
    return render(request,'foreign/wiki_edit_apply.html',{
        'form':form,
    })