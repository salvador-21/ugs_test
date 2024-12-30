# Generated by Django 5.0.3 on 2024-11-18 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='stake_commission',
            fields=[
                ('sc_id', models.AutoField(primary_key=True, serialize=False)),
                ('sc_code', models.CharField(default=0, max_length=50)),
                ('sc_player', models.CharField(default='', max_length=100)),
                ('sc_level', models.CharField(default=0, max_length=50)),
                ('sc_percent', models.CharField(default=0, max_length=50)),
                ('sc_type', models.CharField(default=0, max_length=50)),
                ('sc_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sc_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('screated', models.DateTimeField(auto_now_add=True)),
                ('sc_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stake_withdrawal',
            fields=[
                ('sw_id', models.AutoField(primary_key=True, serialize=False)),
                ('sw_code', models.CharField(blank=True, max_length=50, null=True)),
                ('sw_mop', models.CharField(blank=True, max_length=50, null=True)),
                ('sw_ac_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sw_ac_number', models.CharField(blank=True, max_length=50, null=True)),
                ('sw_available', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sw_withdraw', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sw_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sw_date', models.DateTimeField(auto_now=True)),
                ('sw_status', models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED')], default='PENDING', max_length=50)),
                ('sw_confirmed', models.CharField(blank=True, max_length=50, null=True)),
                ('sw_dateconfirm', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StakeLogs',
            fields=[
                ('stk_id', models.AutoField(primary_key=True, serialize=False)),
                ('stk_code', models.CharField(blank=True, max_length=50, null=True)),
                ('stk_name', models.CharField(blank=True, default=0, max_length=50)),
                ('stk_earnings', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('stk_type', models.CharField(blank=True, default=0, max_length=50)),
                ('stk_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StakeSlot',
            fields=[
                ('sl_id', models.AutoField(primary_key=True, serialize=False)),
                ('sl_code', models.CharField(blank=True, max_length=50, null=True)),
                ('sl_name', models.CharField(blank=True, default=0, max_length=50)),
                ('sl_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sl_amount', models.IntegerField(blank=True, default=0)),
                ('sl_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sl_daily', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sl_earnings', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sl_type', models.CharField(blank=True, default=0, max_length=50)),
                ('sl_status', models.CharField(choices=[('PENDING', 'PENDING'), ('ACTIVE', 'ACTIVE'), ('CLAIMED', 'CLAIMED')], default='PENDING', max_length=50)),
                ('sl_duration', models.IntegerField(blank=True, default=0)),
                ('sl_daysactive', models.IntegerField(blank=True, default=0)),
                ('sl_date', models.DateTimeField(auto_now=True)),
                ('sl_claimed', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sl_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
