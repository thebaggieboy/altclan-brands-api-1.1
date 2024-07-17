from django.db import models
from django.conf import settings
from accounts.models import User
from django.utils import timezone
import uuid
from django.utils.crypto import get_random_string
from brands.models import BillingAddress
from django.utils.text import slugify

from django.contrib.postgres.fields import ArrayField


User = settings.AUTH_USER_MODEL
RANDOM_ORDER_ID = get_random_string(length=12)



class Community(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='community_user')

    community_name = models.CharField(max_length=50, default='', null=True, blank=True)
    community_bio = models.CharField(max_length=250, blank=True, null=True)
    members = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)

    timestamp = models.DateTimeField(auto_now_add=True)

 
    def save(self, *args, **kwargs):


        super(Community, self).save(*args, **kwargs)
        
    def __str__(self): 
        return self.amount

class CommunityPost(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='community_owner')

    community = models.OneToOneField(Community, on_delete=models.CASCADE, null=True, blank=True,related_name='community')
    
    post = models.TextField(blank=True, null=True,)
    comments = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)

    timestamp = models.DateTimeField(auto_now_add=True)

 
    def save(self, *args, **kwargs):


        super(Community, self).save(*args, **kwargs)
        
    def __str__(self): 
        return self.amount

