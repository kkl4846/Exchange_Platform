from django import forms
from .models import *
from foreign.models import *
class DomesticForm(forms.ModelForm):
    class Meta:
        model = Domestic
        fields = ['home_apply', 'home_document', 'semester',
                  'home_scholarship', 'insurance']
        labels = {
            'home_apply' : '지원 방법',
            'home_document': '필요 서류',
            'semester' : '수학 가능 학기',
            'home_scholarship' :' 교내 장학금 정보',
            'insurance' : '유학생 보험 준비'
        }
class DQuestionForm(forms.ModelForm):
    class Meta:
        model = DQuestion
        fields = ['question_title', 'question_content']
        labels = {
            'question_title': '제목',
            'question_content': '내용',
        }


class DCommentForm(forms.ModelForm):
    class Meta:
        model = DComment
        fields = ['comment_content']
        labels = {'comment_content': '내용'}

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = [
        'college','credit','grade_average','apply_semester','away_university','pass_fail'
        ]
        labels = {
            'college': '단과대학',
            'credit': '이수 학점',
            'grade_average': '평점 평균',
            'apply_semester': '지원 시기',
            'away_university': '지원 학교',
            'pass_fail': '합격 여부'
        }

class AddSisterForm(forms.ModelForm):
    class Meta:
        model = Domestic
        fields=['home_sister']
