# Generated by Django 5.0.3 on 2024-12-11 14:11

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs_app', '0028_controls'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcription',
            fields=[
                ('s_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('s_movie', models.CharField(blank=True, max_length=50)),
                ('s_date', models.DateTimeField(auto_now_add=True)),
                ('s_by', models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': ('-s_date',),
            },
        ),
    ]
