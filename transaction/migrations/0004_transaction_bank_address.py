# Generated by Django 5.0 on 2025-02-07 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_transaction_beneficiary_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='bank_address',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
