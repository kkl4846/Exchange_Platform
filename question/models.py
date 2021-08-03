from django.db import models

# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(to='login.User')
    home_university = models.ForeignKey(
        to='domestic.Domestic University', null=True, blank=True)
    away_university = models.ForeignKey(
        to='foreign.Foreign University', null=True, blank=True)
    country = models.ForeignKey(to='country.Country', null=True, blank=True)
    question_title = models.CharField(max_length=50)
    question_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
