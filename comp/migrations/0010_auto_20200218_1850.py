# Generated by Django 2.2.9 on 2020-02-18 09:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0009_auto_20200218_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codecomment',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='codecomment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='codepost',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='codepost_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comcomment',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='comcomment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comp',
            name='star',
            field=models.ManyToManyField(blank=True, related_name='comp_star', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='compost',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='compost_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]