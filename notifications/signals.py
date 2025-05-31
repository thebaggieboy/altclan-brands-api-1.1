# notifications/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Notification
from accounts.models import CustomUser
from brands.models import Merchandise
from transactions.models import Payment, Coupon, Order
from reviews.models import Reviews

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Set up logging
logger = logging.getLogger(__name__)

# Example of additional signal handlers you might want to add:

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    """Create notification when a new order is placed."""
    if not created:
        return
        
    try:
        with transaction.atomic():
            # Notify the brand owner about new order
            if hasattr(instance, 'merchandise') and instance.merchandise.brand:
                notification = Notification.objects.create(
                    user=instance.merchandise.brand,
                    sender=instance.user,
                    notification_type='NEW ORDER',
                    message=f"New order received for {instance.merchandise.name}",
                    target_url=f"/orders/{instance.id}/"
                )
                
                logger.info(f"Order notification created for brand {instance.merchandise.brand.email}")
                print(f"✅ ORDER: Notification sent to {instance.merchandise.brand.email} for new order")
                
    except Exception as e:
        logger.error(f"Failed to create order notification: {e}")
        print(f"❌ ERROR: Failed to create order notification: {e}")


@receiver(post_save, sender=Reviews)
def create_review_notification(sender, instance, created, **kwargs):
    """Create notification when a new review is posted."""
    if not created:
        return
        
    try:
        with transaction.atomic():
            # Notify the brand owner about new review
            if hasattr(instance, 'merchandise') and instance.merchandise.brand:
                notification = Notification.objects.create(
                    user=instance.merchandise.brand,
                    sender=instance.user,
                    notification_type='NEW REVIEW',
                    message=f"New {instance.rating}-star review for {instance.merchandise.name}",
                    target_url=f"/products/{instance.merchandise.id}/#reviews"
                )
                
                logger.info(f"Review notification created for brand {instance.merchandise.brand.email}")
                print(f"✅ REVIEW: Notification sent to {instance.merchandise.brand.email} for new review")
                
    except Exception as e:
        logger.error(f"Failed to create review notification: {e}")
        print(f"❌ ERROR: Failed to create review notification: {e}")


# Utility function to test notifications
def test_notification_system(user_id):
    """
    Utility function to test the notification system.
    Usage: from notifications.signals import test_notification_system; test_notification_system(1)
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        notification = Notification.objects.create(
            user=user,
            sender=user,
            notification_type='TEST',
            message="This is a test notification",
            target_url="/"
        )
        print(f"✅ TEST: Notification created successfully (ID: {notification.id})")
        return notification
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return None