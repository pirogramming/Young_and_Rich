# Generated by Django 2.2.9 on 2020-02-06 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200206_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='comp',
            new_name='star',
        ),
    ]
