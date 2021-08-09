from .models import *
from django import forms


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['visa', 'lifestyle', 'money',
                  'culture', 'covid_info']


class CQuestionForm(forms.ModelForm):
    class Meta:
        model = CQuestion
        fields = [
            'question_title', 'question_content']
        labels = {
            'question_title': '제목',
            'question_content': '내용',
        }


class CCommentForm(forms.ModelForm):
    class Meta:
        model = CComment
        fields = ['comment_content']
        labels = {
            'comment_content': '내용'
        }
