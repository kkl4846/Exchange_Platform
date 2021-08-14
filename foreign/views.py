import foreign
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from jamo import h2j, j2hcj
from django.core.paginator import Paginator
from datetime import datetime


URL_LOGIN = '/login/'


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
            univ_dict[this_alpha].append(univ)
            last_alpha = this_alpha
        else:
            univ_dict[this_alpha].append(univ)
    if len(univ_dict['A']) == 0:  # A인 대학이 없을 때 A출력 제거
        del(univ_dict['A'])
    alphaList = [chr(c) for c in range(ord('A'), ord('Z')+1)]
    return render(request, 'foreign/univ_list.html', {
        'univ_dict': univ_dict,
        'alphaList': alphaList,

    })

# 해외 대학 추가


@login_required(login_url=URL_LOGIN)
def univ_search(request):
    if request.method == 'POST':  # newforeign폼 입력시
        form = NewForeignForm(request.POST)
        if form.is_valid():
            univ = form.save()
            return redirect('foreign:univ_list')
    else:
        f = open('config/univ.json', 'r', encoding='UTF8')
        file = json.load(f)
        foreign_univs = []
        search_univs = []
        for university_dicts in file:
            for university_name in (university_dicts.get(key) for key in university_dicts.keys() if 'name' in key):
                foreign_univs.append(university_name)
        foreign_univs.sort()
        query = request.GET.get('query', '')
        univ_dict = {}
        last_alpha = 'A'
        univ_dict[last_alpha] = []
        if query:
            for univ in foreign_univs:
                if query in univ:
                    search_univs.append(univ)
            for univ in search_univs:
                this_alpha = univ[0]
                if last_alpha != this_alpha:
                    univ_dict[this_alpha] = []
                    univ_dict[this_alpha].append(univ)
                    last_alpha = this_alpha
                else:
                    univ_dict[this_alpha].append(univ)
        if len(univ_dict['A']) == 0:  # A인 대학이 없을 때 A출력 제거
            del(univ_dict['A'])

        form = NewForeignForm()

        return render(request, 'foreign/univ_search.html', {
            'univ_dict': univ_dict,
            'form': form,
        })


# 해외 대학 추가 폼
@login_required(login_url=URL_LOGIN)
def univ_create(request, univ_name):
    if request.method == 'POST':
        form = NewForeignForm(request.POST)
        if form.is_valid():
            univ = form.save(commit=False)
            univ.save()
            univs = Foreign.objects.filter()
            return redirect('foreign:univ_list')
    else:
        form = NewForeignForm()
        ctx = {
            'form': form,
            'univ_name': univ_name,
        }
        return render(request, template_name='foreign/univ_create.html', context=ctx)


# 자매대학


def sister(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    sisters = foreign.sisters.all().order_by('home_name')
    sisters_dict = {}
    last_cho = 'ㄱ'
    sisters_dict[last_cho] = []

    for university in sisters:
        this_university = university.home_name
        university_cho = j2hcj(h2j(this_university[0]))[0]
        if last_cho != university_cho:     # 직전 초성과 다른 초성
            sisters_dict[university_cho] = []
            sisters_dict[university_cho].append(university)
            last_cho = university_cho
        else:                           # 같은 초성
            sisters_dict[university_cho].append(university)
    g_cho = 'ㄱ'
    if len(sisters_dict[g_cho]) == 0:
        del(sisters_dict[g_cho])
    ctx = {
        'sisters_dict': sisters_dict,
        'univ': foreign,
    }
    return render(request, 'foreign/sister.html', ctx)

# 자매대학 추가


@login_required(login_url=URL_LOGIN)
def create_sister(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    if request.method == 'POST':
        sister_name = request.POST['sister']
        sister = get_object_or_404(Domestic, home_name=sister_name)
        foreign.sisters.add(sister.id)

        return redirect("foreign:sister", foreign_id)
    else:
        univs = Domestic.objects.all()
    return render(request, 'foreign/create_sister.html', {
        'domestic_univs': univs,
        'univ': foreign
    })

# wiki


def wiki(request, pk):
    univ = Foreign.objects.get(pk=pk)
    ctx = {
        'univ': univ,
    }
    return render(request, 'foreign/wiki.html', ctx)

# wiki 1번 항목


@login_required(login_url=URL_LOGIN)
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


@login_required(login_url=URL_LOGIN)
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


@login_required(login_url=URL_LOGIN)
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


@login_required(login_url=URL_LOGIN)
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


@login_required(login_url=URL_LOGIN)
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


@login_required(login_url=URL_LOGIN)
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


@login_required(login_url=URL_LOGIN)
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
    all_review = foreign.reviews.order_by('-created_at')
    paginator = Paginator(all_review, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'univ': foreign,
        'page_obj': page_obj,
    }
    return render(request, 'foreign/review_list.html', ctx)


def review_detail(request, pk, foreign_id):
    review = get_object_or_404(Post, pk=pk)
    all_comment = review.post_comment.all()
    recomments = FReComment.objects.all()
    foreign = get_object_or_404(
        Foreign, pk=foreign_id)  # 외국 대학과 국가 넘겨주기위해 받음
    if request.user == review.post_author:
        IsReviewAuthor = True
    else:
        IsReviewAuthor = False
    now = datetime.now()
    ctx = {
        'review': review,
        'univ': foreign,
        'all_comment': all_comment,
        'IsReviewAuthor': IsReviewAuthor,
        'recomments': recomments,
        'now': now,
    }
    return render(request, 'foreign/review_detail.html', ctx)


@login_required(login_url=URL_LOGIN)
def review_create(request, foreign_id, post=None):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    IsReviewAuthor = True
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
            if request.user != post.post_author:
                IsReviewAuthor = False
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
        'IsReviewAuthor': IsReviewAuthor,
    })


def review_delete(request, pk, foreign_id):
    review = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        review.delete()
    return redirect('foreign:review_list', foreign_id)


@login_required(login_url=URL_LOGIN)
def review_update(request, pk, foreign_id):
    post = get_object_or_404(Post, pk=pk)
    return review_create(request, foreign_id, post)


# Q&A


def question_list(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    questions = FQuestion.objects.filter(away_university=foreign)
    questions = questions.order_by('-created_at')
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'page_obj': page_obj,
        'univ': foreign,
    }
    return render(request, 'foreign/question_list.html', context=ctx)


def question_detail(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    question = FQuestion.objects.get(id=pk)
    comments = question.fcomment_set.all()
    undercomments = FUnderComment.objects.all()
    ctx = {
        'question': question,
        'comments': comments,
        'univ': foreign,
        'is_authenticated': request.user.is_authenticated,
        'undercomments': undercomments,
    }
    return render(request, 'foreign/question_detail.html', context=ctx)


@login_required(login_url=URL_LOGIN)
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
            'univ': foreign,
        }
        return render(request, template_name='foreign/question_form.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_edit(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    question = get_object_or_404(FQuestion, id=pk)
    IsQuestionAuthor = True
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('foreign:question_detail', foreign_id, pk)
    else:
        if question != None:                # 수정할 때
            if request.user != question.author:
                IsQuestionAuthor = False
            type = 'update'
        else:                           # 새로 생성할 때
            type = 'create'
        form = QuestionForm(instance=question)
        ctx = {
            'form': form,
            'univ': foreign,
            'IsQuestionAuthor': IsQuestionAuthor,
            'type': type,
        }
        return render(request, template_name='foreign/question_form.html', context=ctx)


def question_delete(request, foreign_id, pk):
    question = get_object_or_404(FQuestion, id=pk)
    if request.method == 'POST':
        question.delete()
    return redirect('foreign:question_list', foreign_id)


def question_search(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    questions = foreign.fquestion_set.all()

    q = request.POST.get('q', "")
    searched = questions.filter(question_title__icontains=q)

    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == foreign.away_name:
            is_enrolled = 'True'

    ctx = {
        'univ': foreign,
        'page_obj': page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
        'q': q
    }
    return render(request, template_name='foreign/question_search.html', context=ctx)

# qna 댓글


@csrf_exempt
@login_required(login_url=URL_LOGIN)
def q_comment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    question_id = req['question_id']
    new_comment_content = req['comment_content']

    new_comment = FComment.objects.create(
        question=FQuestion.objects.get(id=question_id),
        comment_content=new_comment_content,
        comment_author=request.user
    )
    new_comment.save()

    return JsonResponse({'question_id': question_id, 'comment_id': new_comment.id, 'comment_content': new_comment_content})


@csrf_exempt
@login_required(login_url=URL_LOGIN)
def q_comment_edit(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    edit_comment_content = req['comment_content']

    edit_comment = FComment.objects.get(id=comment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'comment_content': edit_comment_content, 'nickname': request.user.nickname})


@csrf_exempt
def q_comment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    delete_comment = FComment.objects.get(id=comment_id)
    delete_comment.delete()

    return JsonResponse({'comment_id': comment_id})


# qna 대댓글
@csrf_exempt
def undercomment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_undercomment = FUnderComment.objects.create(
        comment=FComment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_undercomment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': new_undercomment.id, 'undercomment_author': request.user.nickname, 'undercomment_content': new_comment_content})


@csrf_exempt
def undercomment_update(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    undercomment_id = req['undercomment_id']
    edit_comment_content = req['comment_content']

    edit_comment = FUnderComment.objects.get(id=undercomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': undercomment_id, 'undercomment_author': edit_comment.comment_author.nickname, 'undercomment_content': edit_comment_content})


@csrf_exempt
def undercomment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    undercomment_id = req['undercomment_id']
    delete_comment = FUnderComment.objects.get(id=undercomment_id)
    delete_comment.delete()

    return JsonResponse({'undercomment_id': undercomment_id})


# 댓글달기

@method_decorator(csrf_exempt, name="dispatch")
def comment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    Post_id = req['post_id']
    post = Post.objects.get(id=Post_id)
    content = req['comment_content']
    new_comment = Comment.objects.create(
        comment_author=request.user, comment_content=content, post=post)
    new_comment.save()
    return JsonResponse({'post_id': Post_id, 'comment_content': content, 'comment_id': new_comment.id})


@method_decorator(csrf_exempt, name="dispatch")
def comment_update(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    comment = Comment.objects.get(id=comment_id)
    content = req['comment_content']
    comment.comment_content = content
    comment.save()
    nickname = comment.comment_author.nickname
    return JsonResponse({'comment_id': comment_id, 'comment_content': content, 'nickname': nickname, })


@method_decorator(csrf_exempt, name="dispatch")
def comment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'comment_id': comment_id})


# review 대댓글
@csrf_exempt
def Rrecomment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_recomment = FReComment.objects.create(
        comment=Comment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_recomment.save()

    return JsonResponse({'comment_id': comment_id, 'recomment_id': new_recomment.id, 'recomment_author': request.user.nickname, 'recomment_content': new_comment_content})


@csrf_exempt
def Rrecomment_update(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    recomment_id = req['recomment_id']
    edit_comment_content = req['comment_content']

    edit_comment = FReComment.objects.get(id=recomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'recomment_id': recomment_id, 'recomment_author': edit_comment.comment_author.nickname, 'recomment_content': edit_comment_content})


@csrf_exempt
def Rrecomment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    recomment_id = req['recomment_id']
    delete_comment = FReComment.objects.get(id=recomment_id)
    delete_comment.delete()

    return JsonResponse({'recomment_id': recomment_id})
