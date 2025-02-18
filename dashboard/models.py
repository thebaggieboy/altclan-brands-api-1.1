from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

class Customers(models.Model):
    #id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    
  
    slug = models.SlugField(null=True, blank=True, default='')
    
    def __str__(self):
        return f'Brands Customers'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name}')
        return super().save(*args, **kwargs)
# ProductOrder, these are the items that have been

