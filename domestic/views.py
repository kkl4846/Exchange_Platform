from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from jamo import h2j, j2hcj
# Create your views here.
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

    return render(request, 'domestic/univ_list.html', {'universities_dict': universities_dict})

def wiki(request, domestic_id):
    univ = Domestic.objects.get(pk=domestic_id)
    ctx = {
        'univ': univ,
    }
    return render(request, 'domestic/wiki.html', ctx)

def wiki_edit_apply(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if request.method == 'POST':
        form = DomesticForm(request.POST, request.FILES, instance=domestic)
        if form.is_valid():
            domestic = form.save()
            return redirect('domestic:wiki', domestic_id)
    else:
        form = DomesticForm(instance=domestic)
    return render(request, 'domestic/wiki_edit.html', {
        'form': form,
        'univ': domestic,
        'btn': 1,
    })

def wiki_edit_document(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if request.method == 'POST':
        form = DomesticForm(request.POST, request.FILES, instance=domestic)
        if form.is_valid():
            domestic = form.save()
            return redirect('domestic:wiki', domestic_id)
    else:
        form = DomesticForm(instance=domestic)
    return render(request, 'domestic/wiki_edit.html', {
        'form': form,
        'univ': domestic,
        'btn': 2,
    })

def wiki_edit_semester(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if request.method == 'POST':
        form = DomesticForm(request.POST, request.FILES, instance=domestic)
        if form.is_valid():
            domestic.save()
            return redirect('domestic:wiki', domestic_id)
    else:
        form = DomesticForm(instance=domestic)
    return render(request, 'domestic/wiki_edit.html', {
        'form': form,
        'univ': domestic,
        'btn': 3,
    })

def wiki_edit_scholarship(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if request.method == 'POST':
        form = DomesticForm(request.POST, request.FILES, instance=domestic)
        if form.is_valid():
            domestic.save()
            return redirect('domestic:wiki', domestic_id)
    else:
        form = DomesticForm(instance=domestic)
    return render(request, 'domestic/wiki_edit.html', {
        'form': form,
        'univ': domestic,
        'btn': 4,
    })

def wiki_edit_insurance(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if request.method == 'POST':
        form = DomesticForm(request.POST, request.FILES, instance=domestic)
        if form.is_valid():
            domestic.save()
            return redirect('domestic:wiki', domestic_id)
    else:
        form = DomesticForm(instance=domestic)
    return render(request, 'domestic/wiki_edit.html', {
        'form': form,
        'univ': domestic,
        'btn': 5,
    })

# QnA
def question_list(request, domestic_id):
    domestic= get_object_or_404(Domestic, pk=domestic_id)
    questions = domestic.dquestion_set.all()
    ctx = {
        'domestic': domestic  ,
        'questions': questions,
        'is_authenticated':request.user.is_authenticated
    }
    return render(request, template_name='domestic/question_list.html', context=ctx)


def question_detail(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = DQuestion.objects.get(id=pk)
    comments = question.dcomment_set.all()
    ctx = {
        'question': question, 
        'comments': comments,
        'domestic': domestic,
        'is_authenticated':request.user.is_authenticated
        }
    return render(request, template_name='domestic/question_detail.html', context=ctx)


def question_create(request, domestic_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    if request.method == 'POST':
        form = DQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author=request.user
            post.home_university =domestic
            post.save()
            return redirect('domestic:question_detail', domestic_id, post.pk)
    else:
        form = DQuestionForm()
        ctx = {
            'form': form,
            'domestic':domestic,
            'is_authenticated': request.user.is_authenticated,
            }
        return render(request, template_name='domestic/question_form.html', context=ctx)
        


def question_edit(request, domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = get_object_or_404(DQuestion, id=pk)
    if request.method == 'POST':
        form = DQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('domestic:question_detail',domestic_id, pk)
    else:
        form = DQuestionForm(instance=question)
        ctx = {
            'form': form,
            'domestic':domestic
            }
        return render(request, template_name='domestic/question_form.html', context=ctx)


def question_delete(request, domestic_id, pk):
    question = DQuestion.objects.get(id=pk)
    question.delete()
    return redirect('domestic:question_list', domestic_id)


# 답글댓글

def comment_create(request,domestic_id, pk):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    question = DQuestion.objects.get(id=pk)
    if request.method == 'POST':
        form = DCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question=question
            comment.comment_author = request.user
            comment.save()
            return redirect('domestic:question_detail',domestic_id, pk)
    else:
        form = DCommentForm()
        ctx = {
            'form': form,
            'question':question,
            'domestic':domestic,
            'is_authenticated': request.user.is_authenticated,
            }
        return render(request, template_name='domestic/comment_form.html', context=ctx)


def comment_edit(request, domestic_id, comment_id):
    domestic = get_object_or_404(Domestic, pk=domestic_id)
    comment = get_object_or_404(DComment, id=comment_id)
    question = comment.question
    if request.method == 'POST':
        form = DCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('domestic:question_detail', domestic_id, question.pk)
    else:
        form = DCommentForm(instance=comment)
        ctx = {
            'form': form,
            'question':comment.question,
            'domestic':domestic,
            'is_authenticated': request.user.is_authenticated,
            }
        return render(request, template_name='domestic/comment_form.html', context=ctx)


def comment_delete(request, domestic_id, comment_id):
    comment = DComment.objects.get(id=comment_id)
    question = comment.question
    comment.delete()
    return redirect('domestic:question_detail',domestic_id, question.pk)

#자매결연대학 목록
def sister_list(request,domestic_id):
    domestic=Domestic.objects.get(id=domestic_id)
    sisters=domestic.home_sister.all()
    ctx={
        'domestic':domestic,
        'sisters': sisters,
        }
    return render(request, template_name='domestic/sister_list.html',context=ctx)

#학점컷
def credit_list(request,domestic_id):
    domestic=Domestic.objects.get(id=domestic_id)
    ctx={'domestic':domestic}
    return render(request,template_name='domestic/credit_list.html',context=ctx)

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