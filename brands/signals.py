
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
 
from accounts.models import BrandUser
from django.template.defaultfilters import slugify
from accounts.models import BrandProfile
from brands.models import ShippingAddress, BillingAddress, BrandDashboard, Merchandise, Gallery, MerchandiseGallery

User = settings.AUTH_USER_MODEL
 

# If a new merchandise is created, silmultaneously create a gallery for the merchandise.
@receiver(post_save, sender=Merchandise)
def create_merchandise_gallery(sender, instance, created, **kwargs):
    if created:
        MerchandiseGallery.objects.create(merchandise=instance)
        instance.slug = slugify(f'{instance.merchandise_name}')
        
 
   
        print("------ Merchandise Gallery Created! ------")
        print(f"Gallery created for ${instance.merchandise_name}")

@receiver(post_save, sender=Merchandise)
def save_merchandise_gallery(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f'{instance.merchandise_name}')
        print("------ Merchandise Slug saved! ------")
 

  
   
