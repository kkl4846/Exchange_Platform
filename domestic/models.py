from django.db import models

# Create your models here.


class Domestic(models.Model):
    home_name = models.CharField(max_length=50)
    home_sister = models.ManyToManyField(
        verbose_name="자매결연", to='foreign.Foreign', related_name='sisters', null=True, blank=True)
    home_apply = models.TextField(blank=True)
    home_document = models.TextField(blank=True)
    semester = models.TextField(blank=True)
    home_scholarship = models.TextField(blank=True)
    insurance = models.TextField(blank=True)

    def __str__(self):
        return self.home_name
