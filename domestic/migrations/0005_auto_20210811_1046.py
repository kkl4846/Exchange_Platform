# Generated by Django 3.2.6 on 2021-08-11 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domestic', '0004_dundercomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dquestion',
            name='away_university',
        ),
        migrations.RemoveField(
            model_name='dquestion',
            name='country',
        ),
        migrations.RemoveField(
            model_name='dquestion',
            name='home_university',
        ),
    ]
