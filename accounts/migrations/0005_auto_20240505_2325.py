# Generated by Django 3.2.5 on 2024-05-05 22:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20240503_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 22, 25, 2, 402594, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='brand_bio',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='brand_logo',
            field=models.ImageField(blank=True, default='', null=True, upload_to='Brand Logos'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='brand_name',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='brand_type',
            field=models.CharField(blank=True, choices=[('Clothing & Apparel', 'Clothing & Apparel'), ('Streetwear', 'Streetwear'), ('Kids Clothing', 'Kids Clothing'), ('Accessories', 'Accessories'), ('Jewelleries', 'Jewelleries'), ('Resale wears', 'Resale wears'), ('Thrift wears', 'Thrift wears'), ('Arts & Aesthetics', 'Arts & Aesthetics'), ('Footwears', 'Footwears'), ('Enigmas', 'Enigmas'), ('Watches', 'Watches'), ('Skates', 'Skates'), ('Caps', 'Caps'), ('Masks', 'Masks'), ('Gothic', 'Gothic')], default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 22, 25, 2, 402594, tzinfo=utc)),
        ),
    ]