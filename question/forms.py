from django import forms
from .models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['author', 
        # 'away_university', 'country',
                  'question_title', 'question_content']
        labels = {
            'author': '작성자',
            # 'away_university': '파견교',
            # 'country': '파견 국가',
            'question_title': '제목',
            'question_content': '내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_author', 'comment_content']
        labels = {
            'comment_author': '작성자',
            'comment_content': '내용'
        }
