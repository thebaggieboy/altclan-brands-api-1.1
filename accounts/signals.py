from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Profile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Create the user profile first
        Profile.objects.create(user=instance)
        print(f"New user profile has been created for {instance.email}")
        
        # Email configuration
        subject = 'Welcome to Altclan'
        email_from = 'noreply@altclan.com'
        recipient_list = [instance.email]
        
        # Context data for templates
        context = {
            'user': instance,
            'user_name': instance.first_name if instance.first_name else 'there',
            'user_email': instance.email,
            'dashboard_url': 'https://altclan.com/dashboard',
            'profile_complete_url': 'https://altclan.com/profile/complete',
            'support_email': 'support@altclan.com',
            'website_url': 'https://altclan.com',
        }
        
        # Render email templates
        try:
            # Render HTML template
            html_content = render_to_string('emails/welcome_email.html', context)
            
            # Render plain text template (fallback)
            text_content = render_to_string('emails/welcome_email.txt', context)
            
            # Create and send email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=email_from,
                to=recipient_list
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            print(f"Welcome email sent successfully to {instance.email}")
            
        except Exception as e:
            print(f"Failed to send welcome email to {instance.email}: {str(e)}")
            # You might want to log this error or handle it differently
            # depending on your application's error handling strategy