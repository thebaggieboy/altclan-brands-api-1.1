from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from brands.models import Leads, Merchandise
from accounts.signals import send_account_email

User = settings.AUTH_USER_MODEL

# Brand (Lead) creation email
@receiver(post_save, sender=Leads)
def send_brand_lead_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Your brand has been registered on Altclan'
        message = (
            f'Hi {instance.email_address or "there"},\n\n'
            f'Thank you for signing up your brand "{instance.brand_name}" on Altclan.\n'
            f'You can manage your brand dashboard at {settings.FRONTEND_BASE_URL}/brand/dashboard.\n\n'
            'Best regards,\n'
            'Altclan Team'
        )
        send_account_email(instance.email_address, subject, message)

# Merchandise creation email to marketing list
@receiver(post_save, sender=Merchandise)
def send_merchandise_created_email(sender, instance, created, **kwargs):
    if created:
        subject = f'New merchandise added: {instance.merchandise_name}'
        message = (
            f'A new merchandise "{instance.merchandise_name}" has been added to the platform.\n\n'
            f'Description: {instance.merchandise_description}\n'
            f'Price: ${instance.price:.2f}\n'
            f'View: {settings.FRONTEND_BASE_URL}/merchandise/{instance.slug}\n\n'
            'Best,\n'
            'Altclan Marketing'
        )
        # Send to all marketing emails
        for email in getattr(settings, "MARKETING_EMAILS", []):
            send_account_email(email, subject, message)
