# Generated by Django 5.0.3 on 2024-12-04 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0012_alter_fight_f_created_alter_fight_f_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='convertrewards',
            name='r_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='longestfight',
            name='l_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='points',
            name='p_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='points',
            name='p_update',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='stakefund',
            name='s_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='uwalletcashout',
            name='cw_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='uwalletcashout',
            name='cw_update',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]