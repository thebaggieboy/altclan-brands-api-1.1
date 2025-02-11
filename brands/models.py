import uuid
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from .display import LABEL_DISPLAY, COLLECTION_DISPLAY, COMMUNITY_TYPE_DISPLAY
from django.conf import settings
from accounts.models import BrandProfile


from django.contrib.postgres.fields import ArrayField

User = settings.AUTH_USER_MODEL
BrandUser = settings.BRAND_USER_MODEL

from .choices import STATUS, GENDER, COMMUNITY_TYPE, CLOTHING_CATEGORY
from accounts.models import BrandProfile


class BrandDashboard(models.Model):
    user = models.OneToOneField(BrandUser, on_delete=models.CASCADE, related_name='brand_dashboard', null=True, blank=True)
    #profile = models.OneToOneField(BrandProfile, on_delete=models.CASCADE, related_name='brand_dashboard', null=True, blank=True)
    total_views = models.CharField(max_length=250, null=True, blank=True)
    total_users = models.CharField(max_length=250, null=True, blank=True)
    total_products = models.CharField(max_length=250, null=True, blank=True)
    total_profit = models.CharField(max_length=250, null=True, blank=True)
    total_revenue = models.CharField(max_length=250, null=True, blank=True)
    total_sales = models.CharField(max_length=250, null=True, blank=True)
    total_orders = models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return f'{self.user} Dashboard'



class Merchandise(models.Model):
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    merchandise_name = models.CharField(max_length=250, default='')
    merchandise_color = models.CharField(max_length=250, default='')
    size_type = models.CharField(default='', null=True, blank=True, max_length=250)
    color_type = models.CharField(default='', null=True, blank=True, max_length=250)
    available_sizes = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)
    available_colors = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)
    merchandise_type = models.CharField(default='', null=True, blank=True, max_length=250)
    merchandise_description = models.TextField(default='')
    merchandise_details = models.TextField(default='')
    merchandise_gender = models.CharField(default='', null=True, blank=True, max_length=250)
    #display_image = models.ImageField(upload_to='Display Picture', default='') 
    display_image = models.URLField()
    reviews = ArrayField(models.JSONField(), default=list)
    image_1 = models.ImageField(upload_to='Merch Image', default='', null=True, blank=True)
    image_2 = models.ImageField(upload_to='Merch Image', default='', null=True, blank=True)
    image_3 = models.ImageField(upload_to='Merch Image', default='', null=True, blank=True)
    image_4 = models.ImageField(upload_to='Merch Image', default='', null=True, blank=True)
    image_5 = models.ImageField(upload_to='Merch Image', default='', null=True, blank=True)
    labels = models.CharField(max_length=250,null=True, blank=True, default='')
    price = models.IntegerField(null=True)
    delivery_cost = models.FloatField(null=True, default=0.00)
    discount = models.FloatField(null=True, default=0.00)
    
    slug = models.SlugField()
    date_created = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f'Merchandise Name : {self.merchandise_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.id}')
        return super().save(*args, **kwargs)


class Blog(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    subject = models.TextField()
    slug = models.SlugField(null=True, blank=True, default='')
    def __str__(self):
        return f'Brands Blogs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand_name}')
        return super().save(*args, **kwargs)
# ProductOrder, these are the items that have been

class Leads(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    instagram_username = models.CharField(max_length=250, null=True, blank=True)
    website_link = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, default='')
    def __str__(self):
        return f'Brands Leads'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand_name}')
        return super().save(*args, **kwargs)
# ProductOrder, these are the items that have been
class BillingAddress(models.Model):
    
    user = models.OneToOneField(BrandUser, on_delete=models.CASCADE, related_name='address', null=True, blank=True)
    street_address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    zip = models.CharField(max_length=250, default='')

    def __str__(self):
        return f'{self.user}'
    
class UserBillingAddress(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_address', null=True, blank=True)
    street_address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    zip = models.CharField(max_length=250, default='')

    def __str__(self):
        return f'{self.user}'    
# Inherits from brand


class Cart(models.Model):
    #id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    merchandises = models.ManyToManyField(Merchandise)
    address = models.ForeignKey('BillingAddress', on_delete=models.CASCADE, null=True, blank=True, )
    # Inherit order and bring it into the cart
    # Show list of orders and their quantities

    def __str__(self):
        return f'{self.merchandises} x ( {self.quantity} ) pcs by {self.user} '


class WishList(models.Model):

    user_email = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist', null=True, blank=True)
   
    quantity = models.IntegerField(null=True, blank=True)
    merchandises = ArrayField(models.CharField(max_length=250),blank=True, null=True)

    def __str__(self):
        return f'{self.merchandises} x ( {self.quantity} ) pcs by {self.user_email} '

# Represent a particular product order
