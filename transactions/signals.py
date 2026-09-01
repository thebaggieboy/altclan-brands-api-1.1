from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order
from accounts.signals import send_account_email

@receiver(pre_save, sender=Order)
def store_original_status(sender, instance, **kwargs):
    """Store the original status before saving to detect changes."""
    if instance.pk:
        try:
            original = sender.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except sender.DoesNotExist:
            instance._original_status = None
    else:
        instance._original_status = None

@receiver(post_save, sender=Order)
def order_created_email(sender, instance, created, **kwargs):
    """Send an email when a new order is created."""
    if created:
        subject = f"Your order #{instance.ref_code} has been placed"
        button_url = f"{settings.FRONTEND_BASE_URL}/orders/{instance.ref_code}"
        context_extra = {
            "user_email": instance.email or (instance.user.email if instance.user else ''),
            "ref_code": instance.ref_code,
            "total": instance.total,
            "button_url": button_url,
            "button_text": "View Order",
        }
        send_account_email(
            instance.email or (instance.user.email if instance.user else ''),
            subject,
            f"Your order #{instance.ref_code} was successfully created.",
            template_name='email/order_created_email.html',
            extra_context=context_extra,
        )

@receiver(post_save, sender=Order)
def order_shipped_email(sender, instance, created, **kwargs):
    """Send an email when an order status changes to shipped."""
    if not created and getattr(instance, '_original_status', None) != 'Shipped' and instance.status == 'Shipped':
        subject = f"Your order #{instance.ref_code} has shipped"
        button_url = f"{settings.FRONTEND_BASE_URL}/orders/{instance.ref_code}"
        # Try to get tracking number from a related Delivery if exists
        tracking = ''
        try:
            delivery = instance.deliveries_set.first()
            if delivery:
                tracking = delivery.tracking_number
        except Exception:
            pass
        context_extra = {
            "user_email": instance.email or (instance.user.email if instance.user else ''),
            "ref_code": instance.ref_code,
            "tracking_number": tracking,
            "button_url": button_url,
            "button_text": "Track Order",
        }
        send_account_email(
            instance.email or (instance.user.email if instance.user else ''),
            subject,
            f"Your order #{instance.ref_code} has been shipped.",
            template_name='email/order_shipped_email.html',
            extra_context=context_extra,
        )
