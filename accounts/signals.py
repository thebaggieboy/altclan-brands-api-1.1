
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile
from accounts.models import BrandUser
from .models import CustomUser
from accounts.models import BrandProfile
from brands.models import UserBillingAddress, BillingAddress, BrandDashboard, ShippingAddress, Gallery
from django.core.mail import send_mail


User = settings.AUTH_USER_MODEL
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Altclan'

        email_from = 'noreply@altclan.com'

        message = f"""
            Welcome to Altclan {instance.email} We’re thrilled to have you join our vibrant community of fashion enthusiasts and aesthetes.
            At Altclan, we strive to bring you the latest trends and unique pieces that elevate your style and express your individuality. 
            Whether you’re looking for the latest fashion, exclusive designs, or aesthetic inspirations, we’ve got you covered.

            To get started, here are a few things you can do:
            Explore Our Collections: Discover a curated selection of fashion items and aesthetic pieces tailored to your taste.
            Personalize Your Profile: Complete your profile to receive personalized recommendations and exclusive offers.
            We’re here to support you every step of the way. If you have any questions or need assistance, feel free to reach out to our support team at support@altclan.com

            Thank you for choosing Altclan. We look forward to being a part of your fashion journey!
            Best regards,

            Enimofe Odujirin
            Co-Founder, Altclan
            https://altclan.com
            noreply@altclan.com
"""
        recipient_list = [instance.email]
        Profile.objects.create(user=instance)
        
        send_mail(subject, message, email_from, recipient_list )

        print("New brand profile has been created")

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
        ShippingAddress.objects.create(user=instance)
        Gallery.objects.create(user=instance)
        
   
        print(" ------- [CREATED] Brand profile, dashboard & shipping address! ------")

@receiver(post_save, sender=BrandUser)
def save_brand_profile(sender, instance, **kwargs):
    instance.brand_profile.save()
    instance.brand_dashboard.save()
    instance.shipping_address.save()
    instance.brand_gallery.save()

    print(" ------- [SAVED] Brand profile, dashboard & shipping address! ------")
   
   

