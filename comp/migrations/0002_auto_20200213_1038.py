# Generated by Django 2.2.9 on 2020-02-13 01:38

import comp.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='answer',
            name='accuracy',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='file',
            field=models.FileField(null=True, upload_to=comp.utils.user_answer_upload_to),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comp_file',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]