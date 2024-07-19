from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Auctions(models.Model):
  
    user = models.CharField(max_length=250, null=True, blank=True)
    merchandise_name = models.CharField(max_length=250, null=True, blank=True)
    minimum_bid = models.CharField(max_length=250, null=True, blank=True)
    asking_price = models.CharField(max_length=250, null=True, blank=True)
    current_top_bid = models.CharField(max_length=250, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=True)    
    description = models.CharField(max_length=250, null=True, blank=True)
    auctioners = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
    all_bids = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
   
    
    
    def __str__(self):
        return f'Brands Auctions'


