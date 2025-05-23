from django.db import models
from django.shortcuts import reverse # Create your models here.
from django.conf import settings
from django.utils.text import slugify
from datetime import timezone
from django.contrib.postgres.fields import ArrayField
 
User = settings.AUTH_USER_MODEL

# Create your models here.
class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    email = models.CharField(max_length=250, blank=True, null=True)
    merchandise_name = models.CharField(max_length=250, blank=True, null=True)
    review = models.TextField(default='', blank=True, null=True)
    created_at = models.DateTimeField()
    
    def __str__(self):
        return f'{self.email}'

 
class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    email = models.CharField(max_length=250, blank=True, null=True)
    merchandise_name = models.CharField(max_length=250, blank=True, null=True)
    merchandise_id = models.CharField(max_length=250, blank=True, null=True)
    rating = ArrayField(models.IntegerField(), default=list) 
    overall_score = models.CharField(max_length=250, null=True, blank=True) 
   
    def __str__(self):
        return f'Ratings'