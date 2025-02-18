# Generated by Django 4.2 on 2025-02-18 12:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auctions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=250, null=True)),
                ('merchandise_name', models.CharField(blank=True, max_length=250, null=True)),
                ('minimum_bid', models.CharField(blank=True, max_length=250, null=True)),
                ('asking_price', models.CharField(blank=True, max_length=250, null=True)),
                ('current_top_bid', models.CharField(blank=True, max_length=250, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('auctioners', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
                ('all_bids', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
            ],
        ),
    ]
