<<<<<<< Updated upstream
# Generated by Django 3.2.6 on 2021-08-09 05:53
=======
# Generated by Django 3.2.6 on 2021-08-09 05:49
>>>>>>> Stashed changes

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< Updated upstream
        ('domestic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foreign', '0001_initial'),
        ('country', '0001_initial'),
=======
        ('country', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('domestic', '0001_initial'),
        ('foreign', '0001_initial'),
>>>>>>> Stashed changes
    ]

    operations = [
        migrations.AddField(
            model_name='cquestion',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cquestion',
            name='away_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foreign.foreign'),
        ),
        migrations.AddField(
            model_name='cquestion',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.country'),
        ),
        migrations.AddField(
            model_name='cquestion',
            name='home_university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domestic.domestic'),
        ),
        migrations.AddField(
            model_name='ccomment',
            name='comment_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ccomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country.cquestion'),
        ),
    ]
