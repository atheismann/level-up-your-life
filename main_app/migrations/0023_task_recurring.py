# Generated by Django 2.2.5 on 2019-09-19 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_remove_task_recurring'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='recurring',
            field=models.BooleanField(default=True),
        ),
    ]
