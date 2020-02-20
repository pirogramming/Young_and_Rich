# Generated by Django 2.2.9 on 2020-02-05 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='badge',
        ),
        migrations.AddField(
            model_name='comp',
            name='team_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='badge_list',
            field=models.TextField(default='[]'),
        ),
    ]