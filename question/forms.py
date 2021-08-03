from django import forms
from .models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['author', 'away_university', 'country',
                  'question_title', 'question_content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_author', 'question', 'comment_content']
