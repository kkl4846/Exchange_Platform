import json
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from config.functions import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from datetime import datetime, date, time, timedelta

URL_LOGIN = '/login/'


def country_list(request):
    countries = Country.objects.all().order_by('country_name')
    countries_dict = order_country(countries)

    return render(request, 'country/country_list.html', {'countries_dict': countries_dict})


'''
 위키
'''


def country_wiki(request, pk):
    country = get_object_or_404(Country, pk=pk)
    return render(request, 'country/country_wiki.html', {
        'country': country
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit(request, pk, wiki_type):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'type': wiki_type,
    })


'''
 대학 목록
'''


def country_univ(request, pk):
    country = get_object_or_404(Country, pk=pk)
    unives = country.country_univs.all().order_by('away_name')

    univ_dict = order_foreign(unives)

    return render(request, 'country/country_univ.html', {
        'country': country,
        'univ_dict': univ_dict,
    })


'''
 질문
'''


def question_list(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    questions = CQuestion.objects.filter(country=country)
    questions = questions.order_by('-pk')
    total_question = questions.count()
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'page_obj': page_obj,
        'country_id': country_id,
        'country': country,
        'total_question': total_question,
    }
    return render(request, 'country/question_list.html', context=ctx)


def question_search(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    questions = country.cquestion_set.order_by('-pk')

    q = request.POST.get('q', "")
    searched = questions.filter(question_title__icontains=q)
    total_question = searched.count()

    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'country': country,
        'country_id': country_id,
        'page_obj': page_obj,
        'total_question': total_question,
        'q': q
    }
    return render(request, template_name='country/question_search.html', context=ctx)


def question_detail(request, country_id, pk):
    country = get_object_or_404(Country, pk=country_id)
    question = CQuestion.objects.get(id=pk)
    comments = question.ccomment_set.all()
    undercomments = CUnderComment.objects.all()
    now = datetime.now()

    ctx = {
        'question': question,
        'comments': comments,
        'country': country,
        'is_authenticated': request.user.is_authenticated,
        'undercomments': undercomments,
        'now': now
    }

    response = render(
        request, template_name='country/question_detail.html', context=ctx)

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
def question_create(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    if request.method == 'POST':
        form = CQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.country = country
            post.save()
            return redirect('country:question_detail', country_id, post.pk)
    else:
        form = CQuestionForm()
        ctx = {
            'form': form,
            'country': country,
            'is_authenticated': request.user.is_authenticated,
        }
        return render(request, template_name='country/question_form.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_edit(request, country_id, pk):
    country = get_object_or_404(Country, pk=country_id)
    question = get_object_or_404(CQuestion, id=pk)
    if request.method == 'POST':
        form = CQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('country:question_detail', country_id, pk)
    else:
        form = CQuestionForm(instance=question)
        ctx = {
            'form': form,
            'country': country,
            'question': question,
        }
        return render(request, template_name='country/question_form.html', context=ctx)


def question_delete(request, country_id, pk):
    if request.method == 'POST':
        question = CQuestion.objects.get(id=pk)
        question.delete()

    return redirect('country:question_list', country_id)


'''
 댓글
'''


@csrf_exempt
def comment_create(request, country_id, pk):
    req = json.loads(request.body)
    question_id = req['question_id']
    new_comment_content = req['comment_content']

    new_comment = CComment.objects.create(
        question=CQuestion.objects.get(id=question_id),
        comment_content=new_comment_content,
        comment_author=request.user
    )
    new_comment.save()

    return JsonResponse({'question_id': question_id, 'comment_id': new_comment.id, 'comment_content': new_comment_content})


@csrf_exempt
def comment_update(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    edit_comment_content = req['comment_content']

    edit_comment = CComment.objects.get(id=comment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'comment_content': edit_comment_content, 'nickname': request.user.nickname})


@csrf_exempt
def comment_delete(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    delete_comment = CComment.objects.get(id=comment_id)
    delete_comment.delete()

    return JsonResponse({'comment_id': comment_id})


@csrf_exempt
def undercomment_create(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_undercomment = CUnderComment.objects.create(
        comment=CComment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_undercomment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': new_undercomment.id, 'undercomment_author': request.user.nickname, 'undercomment_content': new_comment_content})


@csrf_exempt
def undercomment_update(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    undercomment_id = req['undercomment_id']
    edit_comment_content = req['comment_content']

    edit_comment = CUnderComment.objects.get(id=undercomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': undercomment_id, 'undercomment_author': edit_comment.comment_author.nickname, 'undercomment_content': edit_comment_content})


@csrf_exempt
def undercomment_delete(request, country_id, pk):
    req = json.loads(request.body)
    undercomment_id = req['undercomment_id']
    delete_comment = CUnderComment.objects.get(id=undercomment_id)
    delete_comment.delete()

    return JsonResponse({'undercomment_id': undercomment_id})
