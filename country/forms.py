from .models import *
from django import forms


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['visa', 'lifestyle', 'money',
                  'culture', 'covid_info']
        labels = {
            'visa': '비자 발급 방법',
            'lifestyle': '현지생활 및 치안',
            'money': '물가 및 체류 비용',
            'culture': '문화적 특징',
            'covid_info': '코로나 정보',
        }


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
