from django.db import models

# Create your models here.


class Domestic(models.Model):
    home_name = models.CharField(max_length=50)
    home_sister = models.ManyToManyField(
        verbose_name="자매결연", to='foreign.Foreign', related_name='sisters')
    home_apply = models.TextField(blank=True)
    home_document = models.TextField(blank=True)
    semester = models.TextField(blank=True)
    home_scholarship = models.TextField(blank=True)
    insurance = models.TextField(blank=True)

    def __str__(self):
        return self.home_name


class DQuestion(models.Model):
    author = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    home_university = models.ForeignKey(
        to='Domestic', on_delete=models.CASCADE, null=True, blank=True)
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


class DComment(models.Model):
    comment_author = models.ForeignKey(
        to='login.User', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('DQuestion', on_delete=models.CASCADE)
    comment_content = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True, blank=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment_content


class Credit(models.Model):
    credit_author = models.ForeignKey(
        to='login.User', on_delete=models.CASCADE)
    home_school = models.ForeignKey(
        to='Domestic', on_delete=models.CASCADE, null=True, blank=True)
    college = models.CharField(max_length=20)
    credit = models.IntegerField(default=1)
    grade_average = models.FloatField(default=0.0)
    apply_semester = models.CharField(
        max_length=20, choices=(("1학기", "1학기"), ("2학기", "2학기")))
    away_university = models.ForeignKey(
        to='foreign.Foreign', on_delete=models.CASCADE, null=True, blank=True)
    pass_fail = models.CharField(
        max_length=20, choices=(("O", "O"), ("X", "X")))

    def __str__(self):
        return self.college
