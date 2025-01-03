# Generated by Django 3.2.5 on 2025-01-03 15:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20241217_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 3, 15, 50, 38, 19941, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 3, 15, 50, 38, 18969, tzinfo=utc)),
        ),
    ]
