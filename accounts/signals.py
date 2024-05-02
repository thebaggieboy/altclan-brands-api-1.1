
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile
from accounts.models import BrandUser
from .models import CustomUser
from accounts.models import BrandProfile
from brands.models import UserBillingAddress, BillingAddress, BrandDashboard

User = settings.AUTH_USER_MODEL
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        
        Profile.objects.create(user=instance)
        print("New user profile has been created")

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print("Profile saved!")
   

# If a new brand is created, silmultaneously create a profile & dashboard for the brand.
@receiver(post_save, sender=BrandUser)
def create_brand_profile(sender, instance, created, **kwargs):
    if created:
        BrandProfile.objects.create(user=instance)
        BrandDashboard.objects.create(user=instance)
        
   
        print("Brand Profile & Address Created!")

@receiver(post_save, sender=BrandUser)
def save_brand_profile(sender, instance, **kwargs):
    instance.brand_profile.save()
    instance.brand_dashboard.save()

    print("Brand Profile saved!")
    print("Brand Address saved!")
   

