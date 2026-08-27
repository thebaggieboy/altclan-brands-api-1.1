from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils.text import slugify
from datetime import timezone
from django.contrib.postgres.fields import ArrayField
 
User = settings.AUTH_USER_MODEL


# A FloatField variant that coerces empty-string inputs to 0.0 so DB prep won't fail
class SafeFloatField(models.FloatField):
    def get_prep_value(self, value):
        if value == '':
            return 0.0
        return super().get_prep_value(value)

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews', null=True, blank=True)  # Made optional
    email = models.CharField(max_length=250, blank=True, null=True)
    merchandise_id = models.IntegerField()
    merchandise_slug = models.SlugField(max_length=250, blank=True, null=True)
    merchandise_name = models.CharField(max_length=250, blank=True, null=True)
    review = models.TextField(default='', blank=True, null=True)
    # Store ratings as integers for clarity and correctness
    individual_rating = models.IntegerField(null=True, blank=True)
    max_rating = models.IntegerField(null=True, blank=True, default=5)
    # cummulative_rating stored as a float fraction (e.g., 4/5 = 0.8)
    cummulative_rating = SafeFloatField(null=True, blank=True, default=0.0)
    rating = ArrayField(models.IntegerField(), default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        # Coerce empty-string or string numbers to float to avoid DB errors
        try:
            if isinstance(self.cummulative_rating, str):
                if self.cummulative_rating.strip() == '':
                    self.cummulative_rating = 0.0
                else:
                    self.cummulative_rating = float(self.cummulative_rating)
        except Exception:
            self.cummulative_rating = 0.0
        super().save(*args, **kwargs)

class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings', null=True, blank=True)  # Made optional
    email = models.CharField(max_length=250, blank=True, null=True)
    merchandise_name = models.CharField(max_length=250, blank=True, null=True)
    merchandise_id = models.CharField(max_length=250, blank=True, null=True)
    individual_rating = models.IntegerField()
    max_rating = models.IntegerField()
    cummulative_rating = SafeFloatField(null=True, blank=True, default=0.0)
    rating = ArrayField(models.IntegerField(), default=list)
    overall_score = models.CharField(max_length=250, null=True, blank=True)
   
    def __str__(self):
        return f'Ratings'

    def save(self, *args, **kwargs):
        # Coerce empty-string or string numbers to float to avoid DB errors
        try:
            if isinstance(self.cummulative_rating, str):
                if self.cummulative_rating.strip() == '':
                    self.cummulative_rating = 0.0
                else:
                    self.cummulative_rating = float(self.cummulative_rating)
        except Exception:
            self.cummulative_rating = 0.0
        super().save(*args, **kwargs)
