from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from brands.models import ShippingAddress, BillingAddress, BrandDashboard, Merchandise, Gallery, MerchandiseGallery

User = settings.AUTH_USER_MODEL


