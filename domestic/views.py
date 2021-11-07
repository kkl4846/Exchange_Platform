import json
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from config.functions import *
from .models import *
from .forms import *
from foreign.models import *
from datetime import datetime, date, timedelta

URL_LOGIN = '/login/'


def is_enrolled(domestic, user):
    is_enrolled = 'False'
    if user.is_authenticated and user.university == domestic.home_name:
        is_enrolled = 'True'
    return is_enrolled


def univ_list(request):
    universities = Domestic.objects.all().order_by('home_name')
    universities_dict = order_domestic(universities)
    ctx = {'universities_dict': universities_dict}

    return render(request, 'domestic/univ_list.html', ctx)


def wiki(request, domestic_id):
    domestic = Domestic.objects.get(pk=domestic_id)
    user = request.user

    ctx = {
        'domestic': domestic,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
    }
    return render(request, 'domestic/wiki.html', ctx)


@login_required(login_url=URL_LOGIN)
def wiki_edit(request, domestic_id, wiki_type):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if is_enrolled(domestic, user):
        if request.method == 'POST':
            form = DomesticForm(request.POST, request.FILES, instance=domestic)
            if form.is_valid():
                domestic = form.save()
                return redirect('domestic:wiki', domestic_id)
        else:
            form = DomesticForm(instance=domestic)
            ctx = {
                'form': form,
                'domestic': domestic,
                'type': wiki_type,
            }
            return render(request, 'domestic/wiki_edit.html', context=ctx)
    else:
        ctx = {
            'univ': domestic,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': 'False',
        }
        return render(request, 'domestic/wiki.html', context=ctx)

# QnA


def question_list(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    questions = domestic.dquestion_set.order_by('-pk')
    total_question = questions.count()

    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    ctx = {
        'domestic': domestic,
        'page_obj': page_obj,
        'total_question': total_question,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
    }
    return render(request, template_name='domestic/question_list.html', context=ctx)


def question_detail(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = DQuestion.objects.get(id=pk)
    comments = question.dcomment_set.all()
    undercomments = DUnderComment.objects.all()

    user = request.user

    now = datetime.now()

    ctx = {
        'question': question,
        'comments': comments,
        'undercomments': undercomments,
        'domestic': domestic,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
        'now': now
    }

    response = render(
        request, template_name='domestic/question_detail.html', context=ctx)

    # 조회수 기능
    expire_date = datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(
        hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard', '_')

    if f'_{pk}_' not in cookie_value:
        cookie_value += f'{pk}_'
        response.set_cookie('hitboard', value=cookie_value,
                            max_age=max_age, httponly=True)
        question.hits += 1
        question.save()
    return response


@login_required(login_url=URL_LOGIN)
def question_create(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if is_enrolled(domestic, user):
        if request.method == 'POST':
            form = DQuestionForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.home_university = domestic
                post.save()
                return redirect('domestic:question_detail', domestic_id, post.pk)
        else:
            form = DQuestionForm()
            ctx = {
                'form': form,
                'domestic': domestic,
                'is_authenticated': user.is_authenticated,
                'is_enrolled': 'True',
            }
            return render(request, template_name='domestic/question_form.html', context=ctx)
    else:
        questions = domestic.dquestion_set.all()
        paginator = Paginator(questions, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ctx = {
            'domestic': domestic,
            'page_obj': page_obj,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': 'False',
        }
        return render(request, template_name='domestic/question_list.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_edit(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = get_object_or_404(DQuestion, id=pk)
    user = request.user
    if user == question.author:
        if request.method == 'POST':
            form = DQuestionForm(request.POST, instance=question)
            if form.is_valid():
                question = form.save()
                return redirect('domestic:question_detail', domestic_id, pk)
        else:
            form = DQuestionForm(instance=question)
            ctx = {
                'form': form,
                'domestic': domestic,
                'question': question
            }
            return render(request, template_name='domestic/question_form.html', context=ctx)
    else:
        is_enrolled = False
        comments = question.dcomment_set.all()
        ctx = {
            'question': question,
            'comments': comments,
            'domestic': domestic,
            'q_verification_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, template_name='domestic/question_detail.html', context=ctx)


def question_delete(request, domestic_id, pk):
    question = DQuestion.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()

    return redirect('domestic:question_list', domestic_id)


def question_search(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    questions = domestic.dquestion_set.order_by('-pk')

    q = request.POST.get('q', "")
    searched = questions.filter(question_title__icontains=q)
    total_question = searched.count()
    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    ctx = {
        'domestic': domestic,
        'page_obj': page_obj,
        'total_question': total_question,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
        'q': q
    }
    return render(request, template_name='domestic/question_search.html', context=ctx)

# 댓글


@csrf_exempt
def comment_create(request, domestic_id, pk):
    req = json.loads(request.body)
    question_id = req['question_id']
    new_comment_content = req['comment_content']

    new_comment = DComment.objects.create(
        question=DQuestion.objects.get(id=question_id),
        comment_content=new_comment_content,
        comment_author=request.user
    )
    new_comment.save()

    return JsonResponse({'question_id': question_id, 'comment_id': new_comment.id, 'comment_content': new_comment_content})


@csrf_exempt
def comment_update(request, domestic_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    edit_comment_content = req['comment_content']
    edit_comment = DComment.objects.get(id=comment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'comment_content': edit_comment_content, 'nickname': request.user.nickname})


@csrf_exempt
def comment_delete(request, domestic_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    delete_comment = DComment.objects.get(id=comment_id)
    delete_comment.delete()

    return JsonResponse({'comment_id': comment_id})

# 대댓글


@csrf_exempt
def undercomment_create(request, domestic_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_undercomment = DUnderComment.objects.create(
        comment=DComment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_undercomment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': new_undercomment.id, 'undercomment_author': request.user.nickname, 'undercomment_content': new_comment_content})


@csrf_exempt
def undercomment_update(request, domestic_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    undercomment_id = req['undercomment_id']
    undercomment_author = request.user
    edit_comment_content = req['comment_content']

    edit_comment = DUnderComment.objects.get(id=undercomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': undercomment_id, 'undercomment_author': undercomment_author.nickname, 'undercomment_content': edit_comment_content})


@csrf_exempt
def undercomment_delete(request, domestic_id, pk):
    req = json.loads(request.body)
    undercomment_id = req['undercomment_id']
    delete_comment = DUnderComment.objects.get(id=undercomment_id)
    delete_comment.delete()

    return JsonResponse({'undercomment_id': undercomment_id})

# 자매결연대학 목록


def sister_list(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)

    user = request.user

    sisters = domestic.home_sister.all().order_by('away_name')
    sisters_dict = order_foreign(sisters)

    ctx = {
        'domestic': domestic,
        'sisters_dict': sisters_dict,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
    }
    return render(request, 'domestic/sister_list.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def sister_add(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
    user = request.user
    if is_enrolled(domestic, user):
        if request.method == 'POST':
            sister_name = request.POST['sister']
            sister = get_object_or_404(Foreign, away_name=sister_name)
            domestic.home_sister.add(sister.id)
            return redirect('domestic:sister_list', domestic_id)
        else:
            univs = Foreign.objects.order_by('away_name')
            ctx = {
                'domestic': domestic,
                'is_authenticated': user.is_authenticated,
                'univs': univs,
                'is_enrolled': 'True',
            }
            return render(request, template_name='domestic/sister_add.html', context=ctx)
    else:
        sisters = domestic.home_sister.all().order_by('away_name')
        sisters_dict = order_foreign(sisters)

        ctx = {
            'domestic': domestic,
            'sisters_dict': sisters_dict,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': 'False',
        }
        return render(request, 'domestic/sister_list.html', context=ctx)


# 학점컷


def credit_list(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
    credit_posts = domestic.credit_set.order_by('-pk')

    paginator = Paginator(credit_posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    ctx = {
        'domestic': domestic,
        'page_obj': page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
    }
    return render(request, template_name='domestic/credit_list.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def credit_create(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
    user = request.user
    if is_enrolled(domestic, user):
        if request.method == 'POST':
            form = CreditForm(request.POST)
            if form.is_valid():
                credit_post = form.save(commit=False)
                credit_post.home_school = domestic
                credit_post.credit_author = request.user
                credit_post.save()
                return redirect('domestic:credit_list', domestic_id)
            else:
                form = CreditForm()
                ctx = {
                    'form': form,
                    'domestic': domestic,
                    'message': "입력한 내용을 다시 확인해주세요.",
                }
                return render(request, template_name='domestic/credit_form.html', context=ctx)
        else:
            form = CreditForm()
            ctx = {
                'form': form,
                'domestic': domestic,
            }
            return render(request, template_name='domestic/credit_form.html', context=ctx)
    else:
        credit_posts = domestic.credit_set.all()
        paginator = Paginator(credit_posts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ctx = {
            'domestic': domestic,
            'page_obj': page_obj,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': 'False',
        }
        return render(request, template_name='domestic/credit_list.html', context=ctx)


def credit_search(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
    credit_posts = domestic.credit_set.order_by('-pk')

    filter = request.POST.get('filter', "")
    q = request.POST.get('q', "")
    if filter == '단과대학':
        searched = credit_posts.filter(college__icontains=q)
    elif filter == '합격여부':
        searched = credit_posts.filter(pass_fail__icontains=q)

    paginator = Paginator(searched, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    ctx = {
        'domestic': domestic,
        'page_obj': page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled(domestic, user),
        'q': q,
        'filter': filter
    }
    return render(request, template_name='domestic/credit_search.html', context=ctx)
