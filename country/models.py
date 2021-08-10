from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=50, verbose_name='나라 이름')
    visa = models.TextField(blank=True, verbose_name='비자 발급 방법')
    lifestyle = models.TextField(blank=True, verbose_name='현지 생활 및 치안')
    money = models.TextField(blank=True, verbose_name='물가 및 체류 비용')
    culture = models.TextField(blank=True, verbose_name='문화적 특징')
    covid_info = models.TextField(blank=True, verbose_name='코로나 정보')

    def __str__(self):
        return self.country_name


class CQuestion(models.Model):
    author = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    home_university = models.ForeignKey(
        to='domestic.Domestic', on_delete=models.CASCADE, null=True, blank=True)
    away_university = models.ForeignKey(
        to='foreign.Foreign', on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(
        to='country.Country', on_delete=models.CASCADE, null=True, blank=True)
    question_title = models.CharField(max_length=50)
    question_content = models.TextField()

    created_at = models.DateField(auto_now_add=True, blank=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.question_title


class CComment(models.Model):
    comment_author = models.ForeignKey(
        to='login.User', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('CQuestion', on_delete=models.CASCADE)
    comment_content = models.TextField(null=True)

    created_at = models.DateField(auto_now_add=True, blank=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment_content


class CUnderComment(models.Model):
    comment = models.ForeignKey('CComment', on_delete=models.CASCADE)
    comment_author = models.ForeignKey('login.User', on_delete=models.CASCADE)
    comment_content = models.TextField(blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
