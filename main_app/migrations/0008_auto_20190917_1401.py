# Generated by Django 2.2.5 on 2019-09-17 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_task_importance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='task',
            name='progress',
        ),
        migrations.AddField(
            model_name='post',
            name='assignedtasks',
            field=models.ManyToManyField(related_name='assignedTasks', to='main_app.Task'),
        ),
        migrations.AddField(
            model_name='post',
            name='completedtasks',
            field=models.ManyToManyField(related_name='completedTasks', to='main_app.Task'),
        ),
        migrations.AddField(
            model_name='post',
            name='inprogresstasks',
            field=models.ManyToManyField(related_name='inProgressTasks', to='main_app.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='importance',
            field=models.CharField(choices=[('1', 'Low Importance'), ('3', 'Medium Importance'), ('5', 'High Importance')], default='Low Importance', max_length=1),
        ),
    ]
