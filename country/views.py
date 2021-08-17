import json
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from jamo import h2j, j2hcj
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

URL_LOGIN = '/login/'


def country_list(request):
    countries = Country.objects.all().order_by('country_name')
    countries_dict = alpha_group(countries)

    # print(countries_dict)

    return render(request, 'country/country_list.html', {'countries_dict': countries_dict})


def alpha_group(things):
    things_dict = {}
    last_alpha = 'ㄱ'
    things_dict[last_alpha] = []

    for thing in things:
        this_thing = thing.country_name
        this_alpha = j2hcj(h2j(this_thing[0]))[0]
        if last_alpha != this_alpha:     # 직전 초성과 다른 초성
            things_dict[this_alpha] = []
            things_dict[this_alpha].append(thing)
            last_alpha = this_alpha
        else:                           # 같은 초성
            things_dict[this_alpha].append(thing)
    g_cho = 'ㄱ'
    if len(things_dict[g_cho]) == 0:
        del(things_dict[g_cho])
    return things_dict


'''
 위키
'''


def country_wiki(request, pk):
    country = get_object_or_404(Country, pk=pk)
    return render(request, 'country/country_wiki.html', {
        'country': country
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit_visa(request, pk):
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
        'btn': 1,
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit_lifestyle(request, pk):
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
        'btn': 2,
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit_money(request, pk):
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
        'btn': 3,
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit_culture(request, pk):
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
        'btn': 4,
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit_covid_info(request, pk):
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
        'btn': 5,
    })


'''
 대학 목록
'''


def country_univ(request, pk):
    country = get_object_or_404(Country, pk=pk)
    unives = country.country_univs.all().order_by('away_name')

    univ_dict = alpha_group(unives)

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
    questions = questions.order_by('-created_at')
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'page_obj': page_obj,
        'country_id': country_id,
        'country': country,
    }
    return render(request, 'country/question_list.html', context=ctx)


def question_search(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    questions = country.cquestion_set.all()

    q = request.POST.get('q', "")
    searched = questions.filter(question_title__icontains=q)

    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'country': country,
        'country_id': country_id,
        'page_obj': page_obj,
        'q': q
    }
    return render(request, template_name='country/question_search.html', context=ctx)


def question_detail(request, country_id, pk):
    country = get_object_or_404(Country, pk=country_id)
    question = CQuestion.objects.get(id=pk)
    comments = question.ccomment_set.all()
    undercomments = CUnderComment.objects.all()
    ctx = {
        'question': question,
        'comments': comments,
        'country': country,
        'is_authenticated': request.user.is_authenticated,
        'undercomments': undercomments,
    }
    return render(request, template_name='country/question_detail.html', context=ctx)


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
            'country': country
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


@login_required(login_url=URL_LOGIN)
def comment_create(request, country_id, pk):
    country = get_object_or_404(Country, pk=country_id)
    question = CQuestion.objects.get(id=pk)
    undercomments = CUnderComment.objects.all()
    if request.method == 'POST':
        form = CCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.comment_author = request.user
            comment.save()
            return redirect('country:question_detail', country_id, pk)
    else:
        form = CCommentForm()
        ctx = {
            'form': form,
            'question': question,
            'country': country,
            'is_authenticated': request.user.is_authenticated,
            'undercomments': undercomments,
        }
        return render(request, template_name='country/comment_form.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def comment_edit(request, country_id, comment_id):
    country = get_object_or_404(Country, pk=country_id)
    comment = get_object_or_404(CComment, id=comment_id)
    undercomments = CUnderComment.objects.all()
    question = comment.question
    if request.method == 'POST':
        form = CCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('country:question_detail', country_id, question.pk)
    else:
        form = CCommentForm(instance=comment)
        ctx = {
            'form': form,
            'question': comment.question,
            'country': country,
            'is_authenticated': request.user.is_authenticated,
            'undercomments': undercomments,
        }
        return render(request, template_name='country/comment_form.html', context=ctx)


def comment_delete(request, country_id, comment_id):
    comment = CComment.objects.get(id=comment_id)
    question = comment.question
    if request.method == 'POST':
        comment.delete()
    return redirect('country:question_detail', country_id, question.pk)


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
