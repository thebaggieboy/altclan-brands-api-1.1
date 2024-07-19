from django.db import models
from django.shortcuts import reverse # Create your models here.
from django.conf import settings
from django.utils.text import slugify
User = settings.AUTH_USER_MODEL

# Create your models here.
class Reviews(models.Model):
    email = models.CharField(max_length=250, blank=True, null=True)
    brand_name = models.CharField(max_length=250, blank=True, null=True)
    review = models.TextField(default='', blank=True, null=True)

    
    def __str__(self):
        return f'{self.user}'

 
