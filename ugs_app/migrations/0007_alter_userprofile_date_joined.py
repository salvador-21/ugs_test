# Generated by Django 5.0.3 on 2024-12-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0006_bet_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(),
        ),
    ]