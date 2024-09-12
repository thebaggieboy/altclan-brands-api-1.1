# Generated by Django 3.2.5 on 2024-09-12 17:23

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(default='', max_length=250)),
                ('city', models.CharField(default='', max_length=250)),
                ('state', models.CharField(default='', max_length=250)),
                ('zip', models.CharField(default='', max_length=250)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='accounts.branduser')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('brand_name', models.CharField(blank=True, max_length=250, null=True)),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('subject', models.TextField()),
                ('slug', models.SlugField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('brand_name', models.CharField(blank=True, max_length=250, null=True)),
                ('instagram_username', models.CharField(blank=True, max_length=250, null=True)),
                ('website_link', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(blank=True, max_length=250, null=True)),
                ('merchandise_name', models.CharField(default='', max_length=250)),
                ('merchandise_color', models.CharField(default='', max_length=250)),
                ('size_type', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('color_type', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('available_sizes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
                ('available_colors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
                ('merchandise_type', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('merchandise_description', models.TextField(default='')),
                ('merchandise_details', models.TextField(default='')),
                ('merchandise_gender', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('display_image', models.URLField()),
                ('image_1', models.ImageField(blank=True, default='', null=True, upload_to='Merch Image')),
                ('image_2', models.ImageField(blank=True, default='', null=True, upload_to='Merch Image')),
                ('image_3', models.ImageField(blank=True, default='', null=True, upload_to='Merch Image')),
                ('image_4', models.ImageField(blank=True, default='', null=True, upload_to='Merch Image')),
                ('image_5', models.ImageField(blank=True, default='', null=True, upload_to='Merch Image')),
                ('labels', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('price', models.IntegerField(null=True)),
                ('delivery_cost', models.FloatField(default=0.0, null=True)),
                ('discount', models.FloatField(default=0.0, null=True)),
                ('slug', models.SlugField()),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 9, 12, 17, 23, 51, 976639, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('merchandises', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250), blank=True, null=True, size=None)),
                ('user_email', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(default='', max_length=250)),
                ('city', models.CharField(default='', max_length=250)),
                ('state', models.CharField(default='', max_length=250)),
                ('zip', models.CharField(default='', max_length=250)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brands.billingaddress')),
                ('merchandises', models.ManyToManyField(to='brands.Merchandise')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BrandDashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_views', models.CharField(blank=True, max_length=250, null=True)),
                ('total_users', models.CharField(blank=True, max_length=250, null=True)),
                ('total_products', models.CharField(blank=True, max_length=250, null=True)),
                ('total_profit', models.CharField(blank=True, max_length=250, null=True)),
                ('total_revenue', models.CharField(blank=True, max_length=250, null=True)),
                ('total_sales', models.CharField(blank=True, max_length=250, null=True)),
                ('total_orders', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_dashboard', to='accounts.branduser')),
            ],
        ),
    ]
