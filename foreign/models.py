from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator


class Foreign(models.Model):
    away_name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(
        "country.Country", on_delete=models.CASCADE, related_name="country_univs")
    away_apply = models.TextField(blank=True)
    language_score = models.TextField(blank=True)
    course_enroll = models.TextField(blank=True)
    accommodation = models.TextField(blank=True)
    atmosphere = models.TextField(blank=True)
    club = models.TextField(blank=True)
    away_scholarship = models.TextField(blank=True)

    def __str__(self):
        return self.away_name


class Post(models.Model):
    foreign = models.ForeignKey(
        Foreign, on_delete=models.CASCADE, related_name="reviews", default='')
    post_author = models.ForeignKey(
        "login.User", on_delete=models.CASCADE, related_name="user_posts")
    CHOICES = (
        ("1학기", "1학기"),
        ("2학기", "2학기"),
    )
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    away_year = models.IntegerField(default=2020, validators=[
        MinValueValidator(2000), MaxValueValidator(2100)])
    away_semester = models.CharField(
        max_length=10,
        choices=CHOICES
    )
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_author = models.ForeignKey(
        "login.User", on_delete=models.CASCADE, related_name="user_comments")
    comment_content = models.TextField()
    post = models.ForeignKey(Post, on_delete=CASCADE,
                             related_name="post_comment")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment_content


class FQuestion(models.Model):
    author = models.ForeignKey(to='login.User', on_delete=models.CASCADE)
    home_university = models.ForeignKey(
        to='domestic.Domestic', on_delete=models.CASCADE, null=True, blank=True)
    away_university = models.ForeignKey(
        to='foreign.Foreign', on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(
        to='country.Country', on_delete=models.CASCADE, null=True, blank=True)
    question_title = models.CharField(max_length=50)
    question_content = models.TextField()
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')

    created_at = models.DateField(auto_now_add=True, blank=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.question_title


class FComment(models.Model):
    comment_author = models.ForeignKey(
        to='login.User', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('FQuestion', on_delete=models.CASCADE)
    comment_content = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True, blank=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment_content


class FUnderComment(models.Model):
    comment = models.ForeignKey('FComment', on_delete=models.CASCADE)
    comment_author = models.ForeignKey('login.User', on_delete=models.CASCADE)
    comment_content = models.TextField(blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class FReComment(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    comment_author = models.ForeignKey('login.User', on_delete=models.CASCADE)
    comment_content = models.TextField(blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
