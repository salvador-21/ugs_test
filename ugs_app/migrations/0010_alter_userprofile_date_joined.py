# Generated by Django 5.0.3 on 2024-12-04 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0009_alter_games_g_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
