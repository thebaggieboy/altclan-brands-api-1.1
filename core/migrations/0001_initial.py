from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SessionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(blank=True, max_length=255, null=True)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('url', models.URLField(blank=True, max_length=2048, null=True)),
                ('hostname', models.CharField(blank=True, max_length=255, null=True)),
                ('pathname', models.CharField(blank=True, max_length=2048, null=True)),
                ('referrer', models.URLField(blank=True, max_length=2048, null=True)),
                ('cookies', models.JSONField(blank=True, default=dict)),
                ('local_storage', models.JSONField(blank=True, default=dict)),
                ('session_storage', models.JSONField(blank=True, default=dict)),
                ('operating_system', models.CharField(blank=True, max_length=255, null=True)),
                ('platform', models.CharField(blank=True, max_length=255, null=True)),
                ('browser', models.CharField(blank=True, max_length=255, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('timezone', models.CharField(blank=True, max_length=255, null=True)),
                ('online', models.BooleanField(default=True)),
                ('screen', models.JSONField(blank=True, default=dict)),
                ('connection', models.JSONField(blank=True, default=dict)),
                ('extra_data', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
