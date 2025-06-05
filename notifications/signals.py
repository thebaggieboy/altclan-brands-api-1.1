# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Notification
from accounts.models import CustomUser
import logging
from threading import Thread

logger = logging.getLogger(__name__)

# Try to import Profile model
try:
    from accounts.models import Profile
except ImportError:
    Profile = None


@receiver(post_save, sender=CustomUser)
def handle_new_user_creation(sender, instance, created, **kwargs):
    """
    Handle new user creation - create notification and profile
    """
    if created:
        try:
            logger.info(f"Processing new user: {instance.email}")
            
            # Create user profile if Profile model exists
            if Profile:
                try:
                    Profile.objects.create(user=instance)
                    logger.info(f"Created profile for user: {instance.email}")
                except Exception as profile_error:
                    logger.error(f"Error creating profile for {instance.email}: {str(profile_error)}")
            
            # Get display name
            display_name = instance.first_name if instance.first_name else instance.email.split('@')[0]
            
            # Create the notification
            notification = Notification.objects.create(
                user=instance,
                sender=instance,
                notification_type='NEW_ACCOUNT',
                message=f"Welcome to altclan {display_name}! You can get started by uploading your products.",
                target_url=f"/brands/profile/{instance.id}/"
            )
            
            logger.info(f"Created notification for new user: {instance.email}")
            
            # Send welcome email in background (non-blocking)
            def send_welcome_email():
                try:
                    subject = 'Welcome to Altclan'
                    message = f'Hi {instance.email},\n\nThank you for registering with Altclan. We are excited to have you on board!\n\nBest regards,\nAltclan Team'
                    email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@altclan.com')
                    recipient_list = [instance.email]
                    
                    send_mail(subject, message, email_from, recipient_list, fail_silently=True)
                    logger.info(f"Welcome email sent to: {instance.email}")
                except Exception as email_error:
                    logger.error(f"Failed to send welcome email to {instance.email}: {str(email_error)}")
            
            # Send email in background thread
            if getattr(settings, 'SEND_WELCOME_EMAILS', True):  # Add this setting to control emails
                email_thread = Thread(target=send_welcome_email)
                email_thread.daemon = True
                email_thread.start()
                
        except Exception as e:
            logger.error(f"Error in user creation signal for {instance.email}: {str(e)}")
            # Don't re-raise to allow user creation to succeed