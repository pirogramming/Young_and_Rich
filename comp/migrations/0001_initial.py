<<<<<<< HEAD
<<<<<<< HEAD
# Generated by Django 2.2.9 on 2020-02-20 07:35
=======
# Generated by Django 2.2.9 on 2020-02-20 08:20
>>>>>>> core-final
=======
# Generated by Django 2.2.9 on 2020-02-20 08:03
>>>>>>> soo-new

import comp.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('context', models.TextField()),
                ('profile_thumb', models.ImageField(blank=True, null=True, upload_to='')),
                ('back_thumb', models.ImageField(blank=True, null=True, upload_to='')),
                ('prize', models.IntegerField()),
                ('comp_answer', models.FileField(blank=True, upload_to=comp.utils.comp_answer_upload_to)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('deadline', models.DateField()),
                ('overview_context', models.TextField()),
                ('timeline', models.TextField()),
                ('prize_context', models.TextField()),
                ('evaluation', models.TextField()),
                ('data_context', models.TextField()),
                ('not_is_main', models.IntegerField(choices=[(0, 0), (1, 1)], default=1)),
                ('continue_complete', models.IntegerField(choices=[(0, 0), (1, 1)], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo_thumb', models.ImageField(upload_to='')),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('phone', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='ComPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('context', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comp.Comp')),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='compost_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comp_File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comp.Comp')),
            ],
        ),
        migrations.AddField(
            model_name='comp',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comp.Company'),
        ),
        migrations.AddField(
            model_name='comp',
            name='star',
            field=models.ManyToManyField(blank=True, related_name='comp_star', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ComComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('commcomment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comp.ComComment')),
                ('compost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comp.ComPost')),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='comcomment_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CodePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('context', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recommend', models.IntegerField(blank=True, null=True)),
                ('comp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comp.Comp')),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='codepost_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CodeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('codepost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comp.CodePost')),
                ('commcomment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comp.CodeComment')),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='codecomment_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(null=True, upload_to=comp.utils.user_answer_upload_to)),
                ('is_selected', models.IntegerField(choices=[(0, 0), (1, 1)], default=0)),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='comp.Comp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
