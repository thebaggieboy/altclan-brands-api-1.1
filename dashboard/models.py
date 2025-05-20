from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Customers(models.Model):
    #id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    brand = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    mobile_number = models.IntegerField()
    orders = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
    last_order = models.DateTimeField()
    date_created = models.DateTimeField(default=timezone.now())
    total_amount_spent = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
   
    
    
  
    slug = models.SlugField(null=True, blank=True, default='')
    
    def __str__(self):
        return f'Brands Customers'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name}')
        return super().save(*args, **kwargs)
# ProductOrder, these are the items that have been

