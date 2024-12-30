# Generated by Django 5.0.3 on 2024-12-04 14:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0007_alter_userprofile_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]