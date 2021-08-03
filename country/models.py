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