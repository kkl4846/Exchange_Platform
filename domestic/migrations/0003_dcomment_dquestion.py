# Generated by Django 3.2.6 on 2021-08-04 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foreign', '0003_post_foreign'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('country', '0001_initial'),
        ('domestic', '0002_domestic_home_sister'),
    ]

    operations = [
        migrations.CreateModel(
            name='DQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=50)),
                ('question_content', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('away_university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foreign.foreign')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.country')),
                ('home_university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domestic.domestic')),
            ],
        ),
        migrations.CreateModel(
            name='DComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('comment_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domestic.dquestion')),
            ],
        ),
    ]
