# Generated by Django 2.2.5 on 2019-09-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_auto_20190919_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='recurring',
            field=models.BooleanField(),
        ),
    ]