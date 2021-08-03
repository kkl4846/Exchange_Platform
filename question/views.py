from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *


# Create your views here.

def question_list(request):
    questions = Question.objects.all()
    ctx = {'questions': questions}
    return render(request, template_name='question/question_list.html', context=ctx)


def question_detail(request, pk):
    question = Question.objects.get(id=pk)
    comments = question.comment_set.all()
    ctx = {'question': question, 'comments': comments}
    return render(request, template_name='question/question_detail.html', context=ctx)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('question:question_detail', pk=post.pk)
    else:
        form = QuestionForm()
        ctx = {'form': form}
        return render(request, template_name='question/question_form.html', context=ctx)


def question_edit(request, pk):
    question = get_object_or_404(Question, id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('question:question_detail', pk)
    else:
        form = QuestionForm(instance=question)
        ctx = {'form': form}
        return render(request, template_name='question/question_form.html', context=ctx)


def question_delete(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()
    return redirect('question:question_list')


# 답글댓글

def comment_create(request,pk):
    question = Question.objects.get(id=pk)
    comment = Comment.objects.create(question=question)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('question:question_detail', pk=comment.question.pk)
    else:
        form = CommentForm(instance=comment)
        ctx = {'form': form}
        return render(request, template_name='question/comment_form.html', context=ctx)


def comment_edit(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('question:question_detail', pk=comment.question.pk)
    else:
        form = CommentForm(instance=comment)
        ctx = {'form': form}
        return render(request, template_name='question/comment_form.html', context=ctx)


def comment_delete(request, pk):
    comment = Comment.objects.get(id=pk)
    question = comment.question
    comment.delete()
    return redirect('question:question_detail', pk=question.pk)
