from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
 
from accounts.models import BrandUser
from django.template.defaultfilters import slugify
from accounts.models import BrandProfile
from brands.models import ShippingAddress, BillingAddress, BrandDashboard, Merchandise, Gallery, MerchandiseGallery

User = settings.AUTH_USER_MODEL


# Only handle gallery creation for new merchandise
@receiver(post_save, sender=Merchandise)
def create_merchandise_gallery(sender, instance, created, **kwargs):
    if created:
        MerchandiseGallery.objects.create(merchandise=instance)
        print("------ Merchandise Gallery Created! ------")
        print(f"Gallery created for {instance.merchandise_name}")