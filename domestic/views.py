from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *

# Create your views here.
def univ_list(request):
    return render(request, template_name='domestic/univ_list.html')


def wiki(request, pk):
    univ = models.Domestic.objects.get(pk=pk)
    ctx = {
        'univ': univ,
    }
    return render(request, 'domestic/wiki.html', ctx)

def wiki_edit_apply(request, pk):
    foreign = get_object_or_404(models.Domestic, pk=pk)
    if request.method == 'POST':
        form = forms.DomesticForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign = form.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = forms.ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 1,
    })

def wiki_edit_document(request, pk):
    foreign = get_object_or_404(models.Domestic, pk=pk)
    if request.method == 'POST':
        form = forms.DomesticForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign = form.save()
            return redirect('domestic:wiki', foreign.pk)
    else:
        form = forms.ForeignForm(instance=foreign)
    return render(request, 'domestic/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 1,
    })

def wiki_edit_semester(request, pk):
    foreign = get_object_or_404(models.Foreign, pk=pk)
    if request.method == 'POST':
        form = forms.ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = forms.ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 3,
    })

def wiki_edit_scholarship(request, pk):
    foreign = get_object_or_404(models.Foreign, pk=pk)
    if request.method == 'POST':
        form = forms.ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = forms.ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 2,
    })

def wiki_edit_insurance(request, pk):
    foreign = get_object_or_404(models.Foreign, pk=pk)
    if request.method == 'POST':
        form = forms.ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = forms.ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 4,
    })

def question_list(request):
    questions = DQuestion.objects.all()
    ctx = {'questions': questions}
    return render(request, template_name='domestic/question_list.html', context=ctx)


def question_detail(request, pk):
    question = DQuestion.objects.get(id=pk)
    comments = question.comment_set.all()
    ctx = {'question': question, 'comments': comments}
    return render(request, template_name='domestic/question_detail.html', context=ctx)


def question_create(request):
    if request.method == 'POST':
        form = DQuestionForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('domestic:question_detail', pk=post.pk)
    else:
        form = DQuestionForm()
        ctx = {'form': form}
        return render(request, template_name='domestic/question_form.html', context=ctx)


def question_edit(request, pk):
    question = get_object_or_404(DQuestion, id=pk)
    if request.method == 'POST':
        form = DQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('domestic:question_detail', pk)
    else:
        form = DQuestionForm(instance=question)
        ctx = {'form': form}
        return render(request, template_name='domestic/question_form.html', context=ctx)


def question_delete(request, pk):
    question = DQuestion.objects.get(id=pk)
    question.delete()
    return redirect('domestic:question_list')


# 답글댓글

def comment_create(request,pk):
    question = DQuestion.objects.get(id=pk)
    if request.method == 'POST':
        form = DCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question=question
            comment.save()
            return redirect('domestic:question_detail', pk)
    else:
        form = DCommentForm()
        ctx = {'form': form,
        'question':question}
        return render(request, template_name='domestic/comment_form.html', context=ctx)


def comment_edit(request, pk):
    comment = get_object_or_404(DComment, id=pk)
    if request.method == 'POST':
        form = DCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('domestic:question_detail', pk=comment.question.pk)
    else:
        form = DCommentForm(instance=comment)
        ctx = {'form': form,'question':comment.question}
        return render(request, template_name='domestic/comment_form.html', context=ctx)


def comment_delete(request, pk):
    comment = DComment.objects.get(id=pk)
    question = comment.question
    comment.delete()
    return redirect('domestic:question_detail', pk=question.pk)


def sister_list(request):
    return render(request, template_name='domestic/sister_list.html')

def credit_list(request):
    return render(request,template_name='domestic/credit_list.html')

def credit_create(request):
    if request.method == 'POST':
        form = DQuestionForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('domestic:credit_list', pk=post.pk)
    else:
        form = DQuestionForm()
        ctx = {'form': form}
        return render(request, template_name='domestic/credit_form.html', context=ctx)