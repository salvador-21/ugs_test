# Generated by Django 5.0.3 on 2024-11-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='p_agentbal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
