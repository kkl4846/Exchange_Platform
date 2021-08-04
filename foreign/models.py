from django.db import models
from django.db.models.deletion import CASCADE


class Foreign(models.Model):
    away_name = models.CharField(max_length=50)
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
        ("1", "1"),
        ("2", "2"),
    )
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    away_year = models.IntegerField()
    away_semester = models.CharField(
        max_length=10,
        choices=CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_author = models.ForeignKey(
        "login.User", on_delete=models.CASCADE, related_name="user_comments")
    comment_content = models.TextField()
    post = models.ForeignKey(Post, on_delete=CASCADE,
                             related_name="post_comment")

    def __str__(self):
        return self.comment_content
