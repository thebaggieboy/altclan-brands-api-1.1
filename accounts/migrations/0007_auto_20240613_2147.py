# Generated by Django 3.2.5 on 2024-06-13 20:47

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20240507_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='followers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='brandprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 13, 20, 47, 2, 560597, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 13, 20, 47, 2, 560597, tzinfo=utc)),
        ),
    ]