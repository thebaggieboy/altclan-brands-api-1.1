from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_articles_seo_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=250, null=True),
        ),
    ]