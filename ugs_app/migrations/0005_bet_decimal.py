# Generated by Django 5.0.3 on 2024-11-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0004_fight_f_revert'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='decimal',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
