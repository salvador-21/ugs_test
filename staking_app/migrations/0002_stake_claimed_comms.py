# Generated by Django 5.0.3 on 2024-11-23 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staking_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stake_claimed_comms',
            fields=[
                ('sr_id', models.AutoField(primary_key=True, serialize=False)),
                ('sr_code', models.CharField(blank=True, max_length=50, null=True)),
                ('sr_mop', models.CharField(blank=True, max_length=50, null=True)),
                ('sr_ac_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sr_ac_number', models.CharField(blank=True, max_length=50, null=True)),
                ('sr_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sr_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sr_date', models.DateTimeField(auto_now=True)),
                ('sr_status', models.IntegerField(default=0)),
                ('sr_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sr_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
