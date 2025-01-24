# Generated by Django 4.2 on 2025-01-17 07:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=250, null=True)),
                ('merchandise_name', models.CharField(blank=True, max_length=250, null=True)),
                ('brand_name', models.CharField(blank=True, max_length=250, null=True)),
                ('review', models.TextField(blank=True, default='', null=True)),
                ('rating', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None)),
                ('overall_score', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=250, null=True)),
                ('merchandise_name', models.CharField(blank=True, max_length=250, null=True)),
                ('brand_name', models.CharField(blank=True, max_length=250, null=True)),
                ('review', models.TextField(blank=True, default='', null=True)),
            ],
        ),
    ]
