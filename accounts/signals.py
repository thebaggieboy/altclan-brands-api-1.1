
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail

User = settings.AUTH_USER_MODEL
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Altclan'

        message = f'Hi {instance.email},Thank you for registering with Altclan. We are excited to have you on board! Best regards, Altclan Team'
        email_from = 'noreply@altclan.com'
        recipient_list = [instance.email]
        
        Profile.objects.create(user=instance)
        print("New user profile has been created for ", instance.email)
        # send email to new user
        send_mail( subject, message, email_from, recipient_list )

 