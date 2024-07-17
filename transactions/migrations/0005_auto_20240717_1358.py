# Generated by Django 3.2.5 on 2024-07-17 20:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20240713_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paystack_reference_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 17, 20, 58, 14, 730823, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(default='BEjdsyqKAgGe', max_length=250),
        ),
    ]
