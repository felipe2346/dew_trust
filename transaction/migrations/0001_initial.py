# Generated by Django 5.0 on 2023-12-23 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_alter_myuser_otp_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beneficiary_bank', models.CharField(blank=True, max_length=200)),
                ('beneficiary_name', models.CharField(max_length=200)),
                ('beneficiary_account', models.CharField(blank=True, max_length=50, null=True)),
                ('iban_number', models.CharField(blank=True, max_length=100)),
                ('route_code', models.CharField(blank=True, max_length=100)),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=14)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('transaction_type', models.CharField(choices=[('DR', 'Debit'), ('CR', 'Credit')], max_length=20)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Successful', 'Successful'), ('Failed', 'Failed')], max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('transaction_date', models.DateField()),
                ('transaction_time', models.TimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='account.userbankaccount')),
            ],
            options={
                'ordering': ['-transaction_date', '-transaction_time'],
            },
        ),
    ]
