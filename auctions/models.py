from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Auctions(models.Model):
  
    user = models.CharField(max_length=250, null=True, blank=True)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    merchandise_name = models.CharField(max_length=250, null=True, blank=True)
    merchandise_type = models.CharField(default='', null=True, blank=True, max_length=250)
    merchandise_description = models.TextField(default='')
    merchandise_details = models.TextField(default='',  null=True, blank=True)
    merchandise_gender = models.CharField(default='', null=True, blank=True, max_length=250)   
    size_type = models.CharField(default='', null=True, blank=True, max_length=250)
    color_type = models.CharField(default='', null=True, blank=True, max_length=250)
    available_sizes = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)
    available_colors = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)
    #display_image = models.ImageField(upload_to='Display Picture', default='') 
    display_image = models.URLField()
    minimum_bid = models.CharField(max_length=250, null=True, blank=True)
    asking_price = models.CharField(max_length=250, null=True, blank=True)
    current_top_bid = models.CharField(max_length=250, null=True, blank=True)
    highest_bid = models.CharField(max_length=250, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=True)    
    description = models.CharField(max_length=250, null=True, blank=True)
    auctioners = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
    all_bids = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
   
    
    
    def __str__(self):
        return f'Brands Auctions'


