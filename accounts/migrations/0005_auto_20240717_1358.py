# Generated by Django 3.2.5 on 2024-07-17 20:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20240713_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 17, 20, 58, 14, 707794, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 17, 20, 58, 14, 706796, tzinfo=utc)),
        ),
    ]
