<<<<<<< HEAD
# Generated by Django 2.2.9 on 2020-02-18 08:50
=======
# Generated by Django 2.2.9 on 2020-02-19 10:08
>>>>>>> Seung

import comp.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
<<<<<<< HEAD
        ('comp', '0009_auto_20200218_1750'),
=======
        ('comp', '0001_initial'),
>>>>>>> Seung
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to=comp.utils.user_profile_image_path)),
                ('rank', models.IntegerField(default=0)),
                ('phone_number', models.CharField(blank=True, max_length=11)),
                ('organization', models.CharField(blank=True, max_length=255)),
                ('gold_list', models.TextField(default='[]')),
                ('silver_list', models.TextField(default='[]')),
                ('bronze_list', models.TextField(default='[]')),
                ('badge_list', models.TextField(default='[]')),
                ('is_id', models.IntegerField(default=0)),
=======
                ('image', models.ImageField(default='default.jpg', upload_to=comp.utils.user_profile_image_path)),
                ('total_rank', models.IntegerField(default=0)),
                ('comp_rank', models.TextField(default='{}')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participate_profile', to='comp.Comp')),
>>>>>>> Seung
                ('star', models.ManyToManyField(blank=True, to='comp.Comp')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
