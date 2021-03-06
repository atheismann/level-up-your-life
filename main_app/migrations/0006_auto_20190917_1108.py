# Generated by Django 2.2.5 on 2019-09-17 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20190917_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='author',
        ),
        migrations.AddField(
            model_name='journal',
            name='about',
            field=models.TextField(default=1, max_length=2500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='journal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
