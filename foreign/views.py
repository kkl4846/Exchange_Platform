from django.shortcuts import get_object_or_404, render, redirect
from . import models
from . import forms


def univ_list(request):
    all_univ = models.Foreign.objects.all()
    return render(request, 'templates/foreign/univ_list', {
        'all_univ': all_univ,
    })

# wiki


def wiki(request, pk):
    univ = models.Foreign.objects.get(pk=pk)
    ctx = {
        'univ': univ,
    }
    return render(request, 'foreign/wiki.html', ctx)

# wiki 1번 항목


def wiki_edit_apply(request, pk):
    foreign = get_object_or_404(models.Foreign, pk=pk)
    if request.method == 'POST':
        form = forms.ForeignForm(request.POST, request.FILES, instance=foreign)
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

# wiki 2번 항목


def wiki_edit_language_score(request, pk):
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
# wiki 3번 항목


def wiki_edit_course_enroll(request, pk):
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

# wiki 4번 항목


def wiki_edit_accommodation(request, pk):
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

# wiki 5번 항목


def wiki_edit_atmosphere(request, pk):
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
        'btn': 5,
    })

# wiki 6번 항목


def wiki_edit_club(request, pk):
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
        'btn': 6,
    })

# wiki 7번 항목


def wiki_edit_away_scholarship(request, pk):
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
        'btn': 7,
    })


# review

def review_list(request, foreign_id):
    foreign = get_object_or_404(models.Foreign, pk=foreign_id)
    all_review = foreign.reviews.all()
    print(all_review)
    ctx = {
        'all_review': all_review,
        'foreign_id': foreign_id,
    }
    return render(request, 'foreign/review_list.html', ctx)


def review_detail(request, pk, foreign_id):
    review = get_object_or_404(models.Post, pk=pk)
    ctx = {
        'review': review,
        'foreign_id': foreign_id,
    }
    return render(request, 'foreign/review_detail.html', ctx)


def review_create(request, foreign_id, post=None):
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, request.FILES, instance=post)
        form.author_post = request.user
        print(form.errors)
        if form.is_valid():
            review = form.save(commit=False)  # db에 바로 저장되지 않도록
            review.post_author = request.user
            review.foreign = get_object_or_404(models.Foreign, id=foreign_id)
            review.save()
            print(review.post_author)
            return redirect('foreign:review_list', foreign_id)
    else:
        if post != None:
            post.post_author = request.user
            post.save()
            type = 'update'
        else:
            type = 'create'
        form = forms.ReviewForm(instance=post)

    return render(request, 'foreign/review_create.html', {
        'form': form,
        'review': post,
        'type': type,
    })


def review_delete(request, pk, foreign_id):
    review = get_object_or_404(models.Post, pk=pk)
    review.delete()
    return redirect('foreign:review_list')


def review_update(request, pk, foreign_id):
    post = get_object_or_404(models.Post, pk=pk)
    return review_create(request, foreign_id, post)
