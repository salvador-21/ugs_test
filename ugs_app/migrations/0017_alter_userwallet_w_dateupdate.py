# Generated by Django 5.0.3 on 2024-12-04 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0016_alter_userprofile_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='w_dateupdate',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 5, 0, 25, 16, 746343)),
        ),
    ]
