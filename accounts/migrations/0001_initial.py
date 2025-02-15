# Generated by Django 4.2 on 2025-02-15 07:24

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('brand_name', models.CharField(blank=True, default='', max_length=250, null=True, unique=True)),
                ('brand_logo', models.URLField(blank=True, default='', null=True)),
                ('brand_bio', models.TextField(blank=True, default='', null=True)),
                ('brand_type', models.CharField(blank=True, choices=[('Clothing & Apparel', 'Clothing & Apparel'), ('Streetwear', 'Streetwear'), ('Kids Clothing', 'Kids Clothing'), ('Accessories', 'Accessories'), ('Jewelleries', 'Jewelleries'), ('Resale wears', 'Resale wears'), ('Thrift wears', 'Thrift wears'), ('Arts & Aesthetics', 'Arts & Aesthetics'), ('Footwears', 'Footwears'), ('Enigmas', 'Enigmas'), ('Watches', 'Watches'), ('Skates', 'Skates'), ('Caps', 'Caps'), ('Masks', 'Masks'), ('Gothic', 'Gothic')], default='', max_length=250, null=True)),
                ('mobile_number', models.CharField(blank=True, default='', max_length=250, null=True, unique=True)),
                ('followers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
                ('wish_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
                ('slug', models.SlugField(blank=True, default='', null=True)),
                ('billing_address', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('zip', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BrandUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('brand_name', models.CharField(default='', max_length=250)),
                ('brand_logo', models.ImageField(default='', upload_to='Brand Logos')),
                ('brand_bio', models.TextField(default='')),
                ('brand_type', models.CharField(choices=[('Clothing & Apparel', 'Clothing & Apparel'), ('Streetwear', 'Streetwear'), ('Kids Clothing', 'Kids Clothing'), ('Accessories', 'Accessories'), ('Jewelleries', 'Jewelleries'), ('Resale wears', 'Resale wears'), ('Thrift wears', 'Thrift wears'), ('Arts & Aesthetics', 'Arts & Aesthetics'), ('Footwears', 'Footwears'), ('Enigmas', 'Enigmas'), ('Watches', 'Watches'), ('Skates', 'Skates'), ('Caps', 'Caps'), ('Masks', 'Masks'), ('Gothic', 'Gothic')], default='', max_length=250)),
                ('mobile_number', models.CharField(default='', max_length=250)),
                ('slug', models.SlugField(blank=True, default='', null=True)),
                ('billing_address', models.CharField(default='', max_length=250)),
                ('city', models.CharField(default='', max_length=250)),
                ('state', models.CharField(default='', max_length=250)),
                ('zip', models.CharField(default='', max_length=250)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2025, 2, 15, 7, 24, 33, 451292, tzinfo=datetime.timezone.utc))),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_followers', to='accounts.branduser')),
            ],
        ),
        migrations.CreateModel(
            name='BrandProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2025, 2, 15, 7, 24, 33, 451292, tzinfo=datetime.timezone.utc))),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_profile', to='accounts.branduser')),
            ],
        ),
    ]
