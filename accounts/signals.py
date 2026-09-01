
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import (
    email_added,
    email_changed,
    email_confirmation_sent,
    email_confirmed,
    email_removed,
    password_changed,
    password_reset,
    password_set,
    user_signed_up,
)
from djoser import signals as djoser_signals

from .models import Profile

User = settings.AUTH_USER_MODEL


def send_account_email(user_email, subject, message, html_message=None):
    """Send email with optional HTML content.
    If html_message is None, we generate a simple styled HTML wrapper
    using the provided subject and plain message.
    """
    if not user_email:
        return
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@altclan.store"
    # Build a basic HTML template if none supplied
    if html_message is None:
        html_message = f"""
        <!DOCTYPE html>
        <html lang='en'>
        <head><meta charset='UTF-8'><title>{subject}</title></head>
        <body style='font-family: Inter, sans-serif; background:#f8fafc; padding:2rem;'>
            <div style='max-width:600px;margin:auto;background:#fff;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.05);padding:2rem;'>
                <h2 style='color:#667eea;'>{subject}</h2>
                <p>{message.replace('\n', '<br>')}</p>
            </div>
        </body>
        </html>
        """
    # Use EmailMultiAlternatives for multipart
    from django.core.mail import EmailMultiAlternatives
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[user_email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

        send_account_email(
            instance.email,
            'Welcome to Altclan',
            (
                f'Hi {instance.email},\n\n'
                'Thank you for registering with Altclan. We are excited to have you on board!\n\n'
                'Best regards,\n'
                'The Altclan Team'
            ),
        )


@receiver(djoser_signals.user_registered)
def send_djoser_signup_email(sender, user, request, **kwargs):
    send_account_email(
        user.email,
        'Your Altclan account has been created',
        (
            f'Hello {user.email},\n\n'
            'Your Altclan account was created successfully.\n\n'
            'You can now explore brands, discover communities, and shop the latest pieces.\n\n'
            'Warm regards,\n'
            'Altclan Team'
        ),
    )


@receiver(user_signed_up)
def send_allauth_signup_email(sender, request, user, **kwargs):
    send_account_email(
        user.email,
        'Welcome to Altclan',
        (
            f'Hi {user.email},\n\n'
            'Welcome to Altclan — your account has been successfully created.\n\n'
            'We are glad to have you with us.\n\n'
            'Best regards,\n'
            'Altclan Team'
        ),
    )


@receiver(djoser_signals.user_activated)
def send_account_activated_email(sender, user, request, **kwargs):
    send_account_email(
        user.email,
        'Your Altclan account is active',
        (
            f'Hi {user.email},\n\n'
            'Your Altclan account has been activated successfully.\n\n'
            'You can now access all available features and continue your experience.\n\n'
            'Best regards,\n'
            'Altclan Team'
        ),
    )


@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    send_account_email(
        user.email,
        'Altclan sign-in alert',
        (
            f'Hi {user.email},\n\n'
            'We noticed a successful sign-in to your Altclan account.\n\n'
            'If this was you, no further action is required. If this wasn\'t you, please reset your password immediately.\n\n'
            'Regards,\n'
            'Altclan Security'
        ),
    )


@receiver(password_set)
def send_password_set_email(sender, request, user, **kwargs):
    send_account_email(
        user.email,
        'Your Altclan password has been set',
        (
            f'Hi {user.email},\n\n'
            'Your Altclan password has been set successfully.\n\n'
            'If you did not do this, please contact support immediately.\n\n'
            'Best,\n'
            'Altclan Team'
        ),
    )


@receiver(password_changed)
def send_password_changed_email(sender, request, user, **kwargs):
    send_account_email(
        user.email,
        'Your Altclan password was changed',
        (
            f'Hi {user.email},\n\n'
            'Your Altclan password was changed successfully.\n\n'
            'If this was not you, please reset your password and contact support right away.\n\n'
            'Regards,\n'
            'Altclan Security'
        ),
    )


@receiver(password_reset)
def send_password_reset_email(sender, request, user, **kwargs):
    send_account_email(
        user.email,
        'Altclan password reset requested',
        (
            f'Hi {user.email},\n\n'
            'A password reset was requested for your Altclan account.\n\n'
            'Please follow the reset instructions in the app to continue.\n\n'
            'If you did not request this, you can ignore this message.\n\n'
            'Regards,\n'
            'Altclan Team'
        ),
    )


@receiver(email_confirmation_sent)
def send_verification_email_sent(sender, request, signup, email_address, **kwargs):
    send_account_email(
        email_address.email,
        'Confirm your Altclan email',
        (
            f'Hi {email_address.email},\n\n'
            'A confirmation email was sent for your Altclan account.\n\n'
            'Please confirm it to complete your account setup and secure your access.\n\n'
            'Regards,\n'
            'Altclan Team'
        ),
    )


@receiver(email_confirmed)
def send_email_confirmed_email(sender, request, email_address, **kwargs):
    send_account_email(
        email_address.email,
        'Your Altclan email was confirmed',
        (
            f'Hi {email_address.email},\n\n'
            'Your email address has been confirmed successfully.\n\n'
            'Thank you for keeping your Altclan account secure.\n\n'
            'Best regards,\n'
            'Altclan Team'
        ),
    )


@receiver(email_added)
def send_email_added_email(sender, request, user, email_address, **kwargs):
    send_account_email(
        email_address.email,
        'A new email was added to your Altclan account',
        (
            f'Hi {email_address.email},\n\n'
            'A new email address has been added to your Altclan account.\n\n'
            'If this was not you, please contact support immediately.\n\n'
            'Regards,\n'
            'Altclan Team'
        ),
    )


@receiver(email_changed)
def send_email_changed_email(sender, request, user, from_email_address, to_email_address, **kwargs):
    send_account_email(
        user.email,
        'Your Altclan email address was changed',
        (
            f'Hi {user.email},\n\n'
            'Your Altclan account email was updated from {from_email_address.email} to {to_email_address.email}.\n\n'
            'If this was not you, please contact support immediately.\n\n'
            'Regards,\n'
            'Altclan Security'
        ),
    )


@receiver(email_removed)
def send_email_removed_email(sender, request, user, email_address, **kwargs):
    send_account_email(
        user.email,
        'Your Altclan email address was removed',
        (
            f'Hi {user.email},\n\n'
            'An email address was removed from your Altclan account.\n\n'
            'If this was not you, please contact support immediately.\n\n'
            'Regards,\n'
            'Altclan Team'
        ),
    )

 