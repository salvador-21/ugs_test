# Generated by Django 5.0.3 on 2024-12-04 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0019_alter_userwallet_w_dateupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='w_dateupdate',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
