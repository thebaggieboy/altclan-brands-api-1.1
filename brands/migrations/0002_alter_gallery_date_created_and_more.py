# Generated by Django 4.2 on 2025-02-18 21:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 18, 21, 29, 15, 773514, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='merchandise',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 18, 21, 29, 15, 770513, tzinfo=datetime.timezone.utc)),
        ),
    ]
