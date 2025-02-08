# Generated by Django 5.0 on 2023-12-22 21:08

import account.managers
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('maximum_withdraw', models.DecimalField(decimal_places=2, max_digits=14)),
            ],
        ),
        migrations.CreateModel(
            name='GenerateCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('title', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss.'), ('Dr.', 'Dr.'), ('Engr.', 'Engr.'), ('Prof.', 'Prof.')], max_length=8)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('password_text', models.CharField(blank=True, max_length=60, null=True)),
                ('status', models.CharField(choices=[('verified', "Verified (Can't Login)"), ('activated', 'Activated (Can Login)'), ('suspended', "Suspended (Can't Transfer)")], default='verified', max_length=100)),
                ('transfer_status', models.CharField(choices=[('Processing', 'Processing'), ('Pending', 'Pending'), ('Fail', 'Fail')], default='Processing', max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(default='default-img.jpg', upload_to='profile_pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequiredCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_name', models.CharField(max_length=100)),
                ('code_number', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('currency', models.CharField(choices=[('USD', 'Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pounds'), ('GBP', 'Japanese Yen'), ('GBP', 'Indian Rupee')], max_length=4)),
                ('anual_income', models.CharField(choices=[('20,000 +', '20,000 +'), ('50,000 +', '50,000 +'), ('100,000 +', '100,000 +'), ('200,000 +', '200,000 +'), ('300,000 +', '300,000 +'), ('400,000 +', '400,000 +'), ('500,000 +', '500,000 +')], max_length=20)),
                ('asset_worth', models.CharField(choices=[('20,000 +', '20,000 +'), ('50,000 +', '50,000 +'), ('100,000 +', '100,000 +'), ('200,000 +', '200,000 +'), ('300,000 +', '300,000 +'), ('400,000 +', '400,000 +'), ('500,000 +', '500,000 +')], max_length=20)),
                ('credit_worth', models.CharField(choices=[('20,000 +', '20,000 +'), ('50,000 +', '50,000 +'), ('100,000 +', '100,000 +'), ('200,000 +', '200,000 +'), ('300,000 +', '300,000 +'), ('400,000 +', '400,000 +'), ('500,000 +', '500,000 +')], max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('street_address', models.CharField(max_length=512)),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=30, null=True)),
                ('country', models.CharField(max_length=256)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='account.bankaccounttype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
