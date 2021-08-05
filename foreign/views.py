from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *


def univ_list(request):
    all_univ = Foreign.objects.all()
    return render(request, 'templates/foreign/univ_list', {
        'all_univ': all_univ,
    })

# wiki


def wiki(request, pk):
    univ = Foreign.objects.get(pk=pk)
    ctx = {
        'univ': univ,
    }
    return render(request, 'foreign/wiki.html', ctx)

# wiki 1번 항목


def wiki_edit_apply(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign = form.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 1,
    })

# wiki 2번 항목


def wiki_edit_language_score(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 2,
    })
# wiki 3번 항목


def wiki_edit_course_enroll(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 3,
    })

# wiki 4번 항목


def wiki_edit_accommodation(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 4,
    })

# wiki 5번 항목


def wiki_edit_atmosphere(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 5,
    })

# wiki 6번 항목


def wiki_edit_club(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 6,
    })

# wiki 7번 항목


def wiki_edit_away_scholarship(request, pk):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'btn': 7,
    })


# review

def review_list(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    all_review = foreign.reviews.all()
    ctx = {
        'all_review': all_review,
        'foreign_id': foreign_id,
        'univ': foreign,
    }
    return render(request, 'foreign/review_list.html', ctx)


def review_detail(request, pk, foreign_id):
    review = get_object_or_404(Post, pk=pk)
    all_comment = review.post_comment.all()
    foreign = get_object_or_404(
        Foreign, pk=foreign_id)  # 외국 대학과 국가 넘겨주기위해 받음
    ctx = {
        'review': review,
        'foreign_id': foreign_id,
        'univ': foreign,
        'all_comment': all_comment,
    }
    return render(request, 'foreign/review_detail.html', ctx)


def review_create(request, foreign_id, post=None):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=post)
        form.author_post = request.user
        if form.is_valid():
            review = form.save(commit=False)  # db에 바로 저장되지 않도록
            review.post_author = request.user
            review.foreign = get_object_or_404(Foreign, id=foreign_id)
            review.save()
            return redirect('foreign:review_detail', foreign_id, review.pk)
    else:
        if post != None:                # 수정할 때
            post.post_author = request.user
            post.save()
            type = 'update'
        else:                           # 새로 생성할 때
            type = 'create'
        form = ReviewForm(instance=post)

    return render(request, 'foreign/review_create.html', {
        'form': form,
        'review': post,
        'type': type,
        'univ': foreign,
    })


def review_delete(request, pk, foreign_id):
    review = get_object_or_404(Post, pk=pk)
    review.delete()
    return redirect('foreign:review_list')


def review_update(request, pk, foreign_id):
    post = get_object_or_404(Post, pk=pk)
    return review_create(request, foreign_id, post)

# Q&A


def question_list(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    questions = FQuestion.objects.filter(away_university=foreign)
    ctx = {
        'questions': questions,
        'foreign_id': foreign_id,
        'univ': foreign,
    }
    return render(request, 'foreign/question_list.html', context=ctx)


def question_detail(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    question = FQuestion.objects.get(id=pk)
    comments = question.fcomment_set.all()
    ctx = {
        'question': question,
        'comments': comments,
        'foreign_id': foreign_id,
        'univ': foreign,
    }
    return render(request, 'foreign/question_detail.html', context=ctx)


def question_create(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        form.author_fquestion = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.away_university = foreign
            post.save()
            return redirect('foreign:question_detail', foreign_id, post.pk)
    else:
        form = QuestionForm()
        ctx = {
            'form': form,
            'foreign_id': foreign_id,
            'univ': foreign,
        }
        return render(request, template_name='foreign/question_form.html', context=ctx)


def question_edit(request, foreign_id, pk):
    question = get_object_or_404(FQuestion, id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('foreign:question_detail', pk)
    else:
        form = QuestionForm(instance=question)
        ctx = {'form': form}
        return render(request, template_name='foreign/question_form.html', context=ctx)


def question_delete(request, foreign_id, pk):
    question = get_object_or_404(FQuestion, id=pk)
    question.delete()
    return redirect('foreign:question_list', foreign_id)


# 답글댓글

def comment_create(request, pk):
    question = FQuestion.objects.get(id=pk)
    # comment = Comment.objects.create(question=question)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            return redirect('question:question_detail', pk)
    else:
        form = CommentForm()
        ctx = {'form': form,
               'question': question}
        return render(request, template_name='question/comment_form.html', context=ctx)


def comment_edit(request, pk):
    comment = get_object_or_404(FComment, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('question:question_detail', pk=comment.question.pk)
    else:
        form = CommentForm(instance=comment)
        ctx = {'form': form, 'question': comment.question}
        return render(request, template_name='question/comment_form.html', context=ctx)


def comment_delete(request, pk):
    comment = FComment.objects.get(id=pk)
    question = comment.question
    comment.delete()
    return redirect('question:question_detail', pk=question.pk)


# 댓글달기

@method_decorator(csrf_exempt, name="dispatch")
def comment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    Post_id = req['post_id']
    post = Post.objects.get(id=Post_id)
    content = req['comment_content']
    new_comment = Comment(comment_author=request.user,
                          comment_content=content, post=post)
    new_comment.save()

    return JsonResponse({'post_id': Post_id, 'comment_content': content, 'comment_id': new_comment.id})


def comment_delete(request):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'comment_id': comment_id})
