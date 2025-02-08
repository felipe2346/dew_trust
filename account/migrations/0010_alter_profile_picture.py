# Generated by Django 5.0 on 2024-04-06 18:07

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_myuser_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
