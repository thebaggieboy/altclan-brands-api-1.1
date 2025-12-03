import uuid
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    subject = models.TextField()
    slug = models.SlugField(null=True, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Brands Blogs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand_name}')
        return super().save(*args, **kwargs)

class Articles(models.Model):

    brand_name = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    subject = models.TextField()
    slug = models.SlugField(null=True, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Brands Articles'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand_name}')
        return super().save(*args, **kwargs)
# ProductOrder, these are the items that have been
