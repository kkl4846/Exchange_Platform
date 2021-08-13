from domestic.models import *
from .models import *
from django import forms

from django_summernote.widgets import SummernoteWidget


class ForeignForm(forms.ModelForm):
    class Meta:
        model = Foreign
        fields = ['away_apply', 'language_score', 'course_enroll',
                  'accommodation', 'atmosphere', 'club', 'away_scholarship']


class NewForeignForm(forms.ModelForm):
    domestics = forms.ModelChoiceField(queryset=Domestic.objects.all())

    class Meta:
        model = Foreign
        fields = ['away_name', 'country', 'domestics']

    def __init__(self, *args, **kwargs):  # tuple/dictionary
        # instance 생성
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['domestics'] = [t.pk for t in
                                    kwargs['instance'].sisters.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field

    def save(self, commit=True):
        # 저장되지 않은 NewForeignForm 저장
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # domestics와 foreign폼 연결
            instance.sisters.clear()

            instance.sisters.add(self.cleaned_data['domestics'])

        self.save_m2m = save_m2m
        instance.save()
        self.save_m2m()

        return instance


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ''
        self.fields['content'].label = ''

    class Meta:
        model = Post
        fields = ['title', 'content', 'away_year', 'away_semester']
        labels = {
            'away_year': '파견 연도',
            'away_semester': '파견 학기'
        }
        widgets = {
            'content': SummernoteWidget(),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = FQuestion
        fields = [
            'question_title', 'question_content']
        labels = {

            'question_title': '제목',
            'question_content': '내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = FComment
        fields = ['comment_content']
        labels = {

            'comment_content': '내용'
        }
