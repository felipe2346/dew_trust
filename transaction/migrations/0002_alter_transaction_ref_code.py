# Generated by Django 5.0 on 2024-03-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='ref_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
