from .models import *
from django import forms
from question.models import *


class ForeignForm(forms.ModelForm):
    class Meta:
        model = Foreign
        fields = ['away_apply', 'language_score', 'course_enroll',
                  'accommodation', 'atmosphere', 'club', 'away_scholarship']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'away_year', 'away_semester']


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
