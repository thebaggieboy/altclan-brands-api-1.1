# Generated by Django 4.2 on 2025-01-24 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 24, 9, 14, 29, 748506, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 24, 9, 14, 29, 748506, tzinfo=datetime.timezone.utc)),
        ),
    ]
