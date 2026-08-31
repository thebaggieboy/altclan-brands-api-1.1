from django.db import migrations, models
from django.template.defaultfilters import slugify


def populate_article_slugs(apps, schema_editor):
    Articles = apps.get_model('blog', 'Articles')
    used_slugs = set()

    for article in Articles.objects.order_by('date_created', 'pk'):
        base_slug = slugify(article.title or article.brand_name or str(article.pk)) or 'article'
        slug = base_slug
        suffix = 2
        while slug in used_slugs:
            slug = f'{base_slug}-{suffix}'
            suffix += 1
        article.slug = slug
        article.save(update_fields=['slug'])
        used_slugs.add(slug)


def populate_article_dates(apps, schema_editor):
    Articles = apps.get_model('blog', 'Articles')
    for article in Articles.objects.filter(updated_at__isnull=True):
        article.updated_at = article.date_created
        article.save(update_fields=['updated_at'])


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='author',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='articles',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='articles',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.RunPython(populate_article_slugs, migrations.RunPython.noop),
        migrations.RunPython(populate_article_dates, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='articles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]