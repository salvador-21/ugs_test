# Generated by Django 5.0.3 on 2024-12-04 15:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0013_alter_bet_created_alter_convertrewards_r_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='w_dateupdate',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 4, 23, 55, 22, 741680)),
        ),
    ]
