from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from jamo import h2j, j2hcj
from foreign.models import *
from django.core.paginator import Paginator

URL_LOGIN = '/login/'


def univ_list(request):
    universities = Domestic.objects.all().order_by('home_name')
    universities_dict = {}
    last_cho = 'ㄱ'
    universities_dict[last_cho] = []

    for university in universities:
        this_university = university.home_name
        university_cho = j2hcj(h2j(this_university[0]))[0]
        if last_cho != university_cho:     # 직전 초성과 다른 초성
            universities_dict[university_cho] = []
            universities_dict[university_cho].append(university)
            last_cho = university_cho
        else:                           # 같은 초성
            universities_dict[university_cho].append(university)

    g_cho = 'ㄱ'
    if len(universities_dict[g_cho]) == 0:
        del(universities_dict[g_cho])

    ctx = {'universities_dict': universities_dict}

    return render(request, 'domestic/univ_list.html', ctx)


def wiki(request, domestic_id):
    univ = Domestic.objects.get(pk=domestic_id)
    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == univ.home_name:
            is_enrolled = 'True'
    ctx = {
        'univ': univ,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'domestic/wiki.html', ctx)


@login_required(login_url=URL_LOGIN)
def wiki_edit_apply(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if user.school_certificate == True and user.university == domestic.home_name:
        if request.method == 'POST':
            form = DomesticForm(request.POST, request.FILES, instance=domestic)
            if form.is_valid():
                domestic = form.save()
                return redirect('domestic:wiki', domestic_id)
        else:
            form = DomesticForm(instance=domestic)
            ctx = {
                'form': form,
                'univ': domestic,
                'btn': 1,
            }
            return render(request, 'domestic/wiki_edit.html', context=ctx)

    else:
        is_enrolled = False
        ctx = {
            'univ': domestic,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, 'domestic/wiki.html', context=ctx)

@login_required(login_url=URL_LOGIN)
def wiki_edit_document(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if user.school_certificate == True and user.university == domestic.home_name:
        if request.method == 'POST':
            form = DomesticForm(request.POST, request.FILES, instance=domestic)
            if form.is_valid():
                domestic = form.save()
                return redirect('domestic:wiki', domestic_id)
        else:
            form = DomesticForm(instance=domestic)
            ctx= {
                'form': form,
                'univ': domestic,
                'btn': 2,
            }
            return render(request, 'domestic/wiki_edit.html', context=ctx)
    else:
        is_enrolled = False
        ctx = {
            'univ': domestic,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, 'domestic/wiki.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def wiki_edit_semester(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if user.school_certificate == True and user.university == domestic.home_name:
        if request.method == 'POST':
            form = DomesticForm(request.POST, request.FILES, instance=domestic)
            if form.is_valid():
                domestic.save()
                return redirect('domestic:wiki', domestic_id)
        else:
            form = DomesticForm(instance=domestic)
            ctx = {
                'form': form,
                'univ': domestic,
                'btn': 3,
            }
            return render(request, 'domestic/wiki_edit.html', context=ctx)
    else:
        is_enrolled = False
        ctx = {
            'univ': domestic,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, 'domestic/wiki.html', context=ctx)

@login_required(login_url=URL_LOGIN)
def wiki_edit_scholarship(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if user.school_certificate == True and user.university == domestic.home_name:
        if request.method == 'POST':
            form = DomesticForm(request.POST, request.FILES, instance=domestic)
            if form.is_valid():
                domestic.save()
                return redirect('domestic:wiki', domestic_id)
        else:
            form = DomesticForm(instance=domestic)
            ctx = {
                'form': form,
                'univ': domestic,
                'btn': 4,
            }
            return render(request, 'domestic/wiki_edit.html', context= ctx)
    else:
        is_enrolled = False
        ctx = {
            'univ': domestic,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, 'domestic/wiki.html', context=ctx)

@login_required(login_url=URL_LOGIN)
def wiki_edit_insurance(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if user.school_certificate == True and user.university == domestic.home_name:
        if request.method == 'POST':
            form = DomesticForm(request.POST, request.FILES, instance=domestic)
            if form.is_valid():
                domestic.save()
                return redirect('domestic:wiki', domestic_id)
        else:
            form = DomesticForm(instance=domestic)
            ctx = {
                'form': form,
                'univ': domestic,
                'btn': 5,
            }
            return render(request, 'domestic/wiki_edit.html', context=ctx)
    else:
        is_enrolled = False
        ctx = {
            'univ': domestic,
            'certificate_error': True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, 'domestic/wiki.html', context=ctx)
# QnA


def question_list(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    questions = domestic.dquestion_set.all()

    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'

    ctx = {
        'domestic': domestic,
        'page_obj': page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
    }
    return render(request, template_name='domestic/question_list.html', context=ctx)


def question_detail(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = DQuestion.objects.get(id=pk)
    comments = question.dcomment_set.all()
    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'
    ctx = {
        'question': question,
        'comments': comments,
        'domestic': domestic,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
    }
    return render(request, template_name='domestic/question_detail.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_create(request, domestic_id):
    user = request.user
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if user.school_certificate == True and user.university == domestic.home_name:
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
            'certificate_error':True,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': 'False',
        }
        return render(request, template_name='domestic/question_list.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_edit(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = get_object_or_404(DQuestion, id=pk)
    user = request.user
    if user == question.author :
        if request.method == 'POST':
            form = DQuestionForm(request.POST, instance=question)
            if form.is_valid():
                question = form.save()
                return redirect('domestic:question_detail', domestic_id, pk)
        else:
            form = DQuestionForm(instance=question)
            ctx = {
            'form': form,
            'domestic': domestic
            }
            return render(request, template_name='domestic/question_form.html', context=ctx)
    else:
        is_enrolled = False
        comments = question.dcomment_set.all()
        ctx = {
        'question': question,
        'comments': comments,
        'domestic': domestic,
        'verification_error': True,
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
    questions = domestic.dquestion_set.all()

    q = request.POST.get('q', "") 
    searched = questions.filter(question_title__icontains=q)
    
    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'

    ctx = {
        'domestic': domestic,
        'page_obj': page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
        'q' : q
    }
    return render(request, template_name='domestic/question_search.html', context=ctx)


# 답글댓글
@login_required(login_url=URL_LOGIN)
def comment_create(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = DQuestion.objects.get(id=pk)
    user = request.user
    if user.school_certificate == True and user.university == domestic.home_name:
        if request.method == 'POST':
            form = DCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.question = question
                comment.comment_author = user
                comment.save()
                return redirect('domestic:question_detail', domestic_id, pk)
        else:
            form = DCommentForm()
            ctx = {
                'form': form,
                'question': question,
                'domestic': domestic,
                'is_authenticated': user.is_authenticated,
                'is_enrolled': 'True',
            }
            return render(request, template_name='domestic/comment_form.html', context=ctx)
    else:
        comments = question.dcomment_set.all()
        ctx = {
        'question': question,
        'comments': comments,
        'domestic': domestic,
        'certificate_error':True,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': 'False',
        }
        return render(request, template_name='domestic/question_detail.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def comment_edit(request, domestic_id, comment_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    comment = get_object_or_404(DComment, id=comment_id)
    question = comment.question
    user = request.user
    if user == comment.comment_author :
        if request.method == 'POST':
            form = DCommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save()
                return redirect('domestic:question_detail', domestic_id, question.pk)
        else:
            form = DCommentForm(instance=comment)
    else: 
        is_enrolled = 'False'
        if user.is_authenticated:
            if user.university == domestic.home_name:
                is_enrolled = 'True'
        ctx = {
            'form': form,
            'question': comment.question,
            'domestic': domestic,
            'is_authenticated': user.is_authenticated,
            'is_enrolled': is_enrolled,
        }
        return render(request, template_name='domestic/comment_form.html', context=ctx)


def comment_delete(request, domestic_id, comment_id):
    comment = DComment.objects.get(id=comment_id)
    question = comment.question
    if request.method == 'POST':
        comment.delete()

    return redirect('domestic:question_detail', domestic_id, question.pk)

# 자매결연대학 목록


def sister_list(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'

    sisters = domestic.home_sister.all().order_by('away_name')
    sisters_dict = {}
    last_alpha = 'A'
    sisters_dict[last_alpha] = []
    for sister in sisters:
        s = sister.away_name
        this_alpha = s[0]
        if last_alpha != this_alpha:
            sisters_dict[this_alpha] = []
            sisters_dict[this_alpha].append(sister)
            last_alpha = this_alpha
        else:
            sisters_dict[this_alpha].append(sister)
    if len(sisters_dict['A']) == 0:
        del(sisters_dict['A'])

    ctx = {
        'domestic': domestic,
        'sisters': sisters,
        'sisters_dict': sisters_dict,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'domestic/sister_list.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def sister_add(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'

    if request.method == 'POST':
        sister_name = request.POST['sister']
        sister = get_object_or_404(Foreign, away_name=sister_name)
        print(sister)
        domestic.home_sister.add(sister.id)
        return redirect('domestic:sister_list', domestic_id)
    else:
        univs = Foreign.objects.all()
        print(univs)
        ctx = {
            'domestic': domestic,
            'is_authenticated': user.is_authenticated,
            'univs': univs,
            'is_enrolled': is_enrolled,
        }
        return render(request, template_name='domestic/sister_add.html', context=ctx)

# 학점컷


def credit_list(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
    credit_posts = domestic.credit_set.all()

    paginator = Paginator(credit_posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'

    ctx = {
        'domestic': domestic,
        'page_obj':page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
    }
    return render(request, template_name='domestic/credit_list.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def credit_create(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
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

def credit_search(request, domestic_id):
    domestic = Domestic.objects.get(id=domestic_id)
    credit_posts = domestic.credit_set.all()

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
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == domestic.home_name:
            is_enrolled = 'True'

    ctx = {
        'domestic': domestic,
        'page_obj':page_obj,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
        'q': q,
        'filter': filter
    }
    return render(request, template_name='domestic/credit_search.html', context=ctx)