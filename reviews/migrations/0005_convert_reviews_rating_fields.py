# Generated manually to convert Reviews rating fields from CharField to IntegerField and populate values
from django.db import migrations, models


def forwards(apps, schema_editor):
    Reviews = apps.get_model('reviews', 'Reviews')
    for r in Reviews.objects.all():
        # try to parse existing string fields safely
        try:
            ind = int(r.individual_rating) if r.individual_rating not in (None, '') else None
        except Exception:
            ind = None
        try:
            maxr = int(r.max_rating) if r.max_rating not in (None, '') else 5
        except Exception:
            maxr = 5
        # set new integer fields (we added temporary fields before renaming)
        if hasattr(r, 'individual_rating_int'):
            r.individual_rating_int = ind
        if hasattr(r, 'max_rating_int'):
            r.max_rating_int = maxr
        # compute cummulative_rating if possible
        if ind is not None and maxr:
            r.cummulative_rating = float(ind) / float(maxr)
        else:
            # leave existing cummulative_rating if present, else default to 0
            r.cummulative_rating = r.cummulative_rating or 0.0
        r.save()


def backwards(apps, schema_editor):
    # best-effort revert: copy ints back into string fields
    Reviews = apps.get_model('reviews', 'Reviews')
    for r in Reviews.objects.all():
        try:
            if hasattr(r, 'individual_rating_int') and r.individual_rating_int is not None:
                r.individual_rating = str(r.individual_rating_int)
            if hasattr(r, 'max_rating_int') and r.max_rating_int is not None:
                r.max_rating = str(r.max_rating_int)
            r.save()
        except Exception:
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_fix_all_ratings_fields'),
    ]

    operations = [
        # Add temporary integer fields to hold converted values
        migrations.AddField(
            model_name='reviews',
            name='individual_rating_int',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reviews',
            name='max_rating_int',
            field=models.IntegerField(null=True, blank=True, default=5),
        ),
        migrations.RunPython(forwards, backwards),
        # Rename original char fields to keep a backup
        migrations.RenameField(
            model_name='reviews',
            old_name='individual_rating',
            new_name='individual_rating_str',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='individual_rating_int',
            new_name='individual_rating',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='max_rating',
            new_name='max_rating_str',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='max_rating_int',
            new_name='max_rating',
        ),
        # Optionally remove the old string backup fields
        migrations.RemoveField(
            model_name='reviews',
            name='individual_rating_str',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='max_rating_str',
        ),
        # Ensure new fields have sensible defaults and nullability
        migrations.AlterField(
            model_name='reviews',
            name='individual_rating',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='max_rating',
            field=models.IntegerField(null=True, blank=True, default=5),
        ),
    ]
