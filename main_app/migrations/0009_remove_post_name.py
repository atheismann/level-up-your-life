# Generated by Django 2.2.5 on 2019-09-17 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20190917_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='name',
        ),
    ]
