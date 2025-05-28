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
    # FIXED: Removed null=True from ArrayField items
    available_sizes = ArrayField(models.CharField(max_length=250), default=list, blank=True)
    available_colors = ArrayField(models.CharField(max_length=250), default=list, blank=True)
    merchandise_type = models.CharField(default='', null=True, blank=True, max_length=250)
    merchandise_description = models.TextField(default='')
    merchandise_details = models.TextField(default='', null=True, blank=True)
    merchandise_gender = models.CharField(default='', null=True, blank=True, max_length=250)
    display_image = models.URLField()
    # FIXED: Removed null=True from ArrayField items
    reviews = ArrayField(models.CharField(max_length=250), default=list, blank=True)
    image_1 = models.ImageField(upload_to='Merch Image', null=True, blank=True)
    image_2 = models.ImageField(upload_to='Merch Image', null=True, blank=True)
    image_3 = models.ImageField(upload_to='Merch Image', null=True, blank=True)
    image_4 = models.ImageField(upload_to='Merch Image', null=True, blank=True)
    image_5 = models.ImageField(upload_to='Merch Image', null=True, blank=True)
    labels = models.CharField(max_length=250, null=True, blank=True, default='')
    price = models.IntegerField(null=True, blank=True)
    delivery_cost = models.FloatField(null=True, blank=True, default=0.00)
    discount = models.FloatField(null=True, blank=True, default=0.00)
    slug = models.SlugField(null=True, blank=True)
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Merchandise Name : {self.merchandise_name}'

    # FIXED: Added save method to generate slug
    def save(self, *args, **kwargs):
        if not self.slug and self.merchandise_name:
            self.slug = slugify(f'{self.merchandise_name}')
        return super().save(*args, **kwargs)


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    subject = models.TextField()
    slug = models.SlugField(null=True, blank=True, default='')
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.brand_name} articles'

    def save(self, *args, **kwargs):
        if not self.slug:
            # FIXED: Use title instead of brand_name for better SEO
            slug_source = self.title or self.brand_name or 'blog'
            self.slug = slugify(slug_source)
        return super().save(*args, **kwargs)


class Leads(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    email_address = models.CharField(max_length=250, null=True, blank=True)
    instagram_username = models.CharField(max_length=250, null=True, blank=True)
    website_link = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, default='')
    # FIXED: Added date_created field
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Lead: {self.brand_name or self.email_address or "Unknown"}'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_source = self.brand_name or self.email_address or 'lead'
            self.slug = slugify(slug_source)
        return super().save(*args, **kwargs)


class BillingAddress(models.Model):
    user = models.OneToOneField(BrandUser, on_delete=models.CASCADE, related_name='address', null=True, blank=True)
    street_address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    zip = models.CharField(max_length=250, default='')

    def __str__(self):
        return f'{self.user} - {self.city}, {self.state}'

    
class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shipping_address', null=True, blank=True)
    street_address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    zip = models.CharField(max_length=250, default='')

    def __str__(self):
        return f'{self.user} - {self.city}, {self.state}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_cart')
    quantity = models.IntegerField(null=True, blank=True)
    merchandises = models.ManyToManyField(Merchandise, blank=True)
    address = models.ForeignKey('BillingAddress', on_delete=models.CASCADE, null=True, blank=True)
    # FIXED: Added date fields for better tracking
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        merch_count = self.merchandises.count()
        return f'Cart for {self.user} - {merch_count} items'

    # FIXED: Added method to calculate total
    def get_total_items(self):
        return self.merchandises.count()


class WishList(models.Model):
    user_email = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wishlist', null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    # FIXED: Removed null=True from ArrayField items and improved field name
    merchandises = ArrayField(models.CharField(max_length=250), blank=True, default=list)
    # FIXED: Added date fields
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Wishlist for {self.user_email}'


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='brand_gallery')
    # FIXED: Removed null=True from ArrayField items
    images = ArrayField(models.CharField(max_length=250), blank=True, default=list)
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)
    # FIXED: Added title and description fields
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} Gallery - {self.images.__len__()} images'

    
class MerchandiseGallery(models.Model):
    # Each Merch Gallery belongs to a Merch
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE, null=True, blank=True, related_name='merchandise_gallery')
    # FIXED: Removed null=True from ArrayField items
    images = ArrayField(models.CharField(max_length=250), blank=True, default=list)
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)
    # FIXED: Added title field
    title = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        merch_name = self.merchandise.merchandise_name if self.merchandise else 'Unknown'
        return f'{merch_name} Gallery - {len(self.images)} images'