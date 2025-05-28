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

@receiver(post_save, sender=CustomUser)
def create_new_user_notification(sender, instance, created, **kwargs):
    """
    Create a welcome notification for newly registered users.
    
    Args:
        sender: The model class (CustomUser)
        instance: The actual instance being saved  
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if not created:
        return
    
    try:
        with transaction.atomic():
            # Validate user instance
            if not instance or not hasattr(instance, 'id') or not instance.id:
                logger.error("Invalid user instance provided for notification creation")
                print("❌ ERROR: Invalid user instance - cannot create welcome notification")
                return
            
            # Validate email exists
            if not instance.email:
                logger.warning(f"User {instance.id} has no email address")
                print(f"⚠️  WARNING: User {instance.id} has no email - using generic welcome message")
                email_text = "new user"
            else:
                email_text = instance.email
            
            # Create welcome notification
            notification = Notification.objects.create(
                user=instance,
                sender=instance,  # Self-notification for welcome message
                notification_type='NEW ACCOUNT',
                message=f"Welcome to altclan {email_text}! You can get started by uploading your products.",
                target_url=f"/brands/profile/{instance.id}/"
            )
    
            # Log successful creation
            logger.info(f"Welcome notification created successfully for user {instance.id} ({instance.email})")
            print(f"✅ SUCCESS: Welcome notification created for user {instance.email} (ID: {instance.id})")
            
            # Send real-time notification via WebSocket
            try:
                channel_layer = get_channel_layer()
                
                if channel_layer is None:
                    logger.warning("Channel layer not configured - skipping real-time notification")
                    print("⚠️  WARNING: Channel layer not configured - notification saved but not sent via WebSocket")
                else:
                    async_to_sync(channel_layer.group_send)(
                        f"notifications_{instance.id}",
                        {
                            'type': 'send_notification',
                            'notification': {
                                'id': notification.id,
                                'message': notification.message,
                                'notification_type': notification.notification_type,
                                'is_read': notification.is_read,
                                'created_at': notification.created_at.isoformat(),
                                'target_url': notification.target_url
                            }
                        }
                    )
                    
                    logger.info(f"Real-time notification sent successfully for user {instance.id}")
                    print(f"📡 Real-time notification sent via WebSocket for user {instance.email}")
                    
            except Exception as websocket_error:
                # Don't fail the entire process if WebSocket fails
                logger.error(f"Failed to send real-time notification for user {instance.id}: {websocket_error}")
                print(f"❌ ERROR: Failed to send real-time notification for {instance.email}: {websocket_error}")
                print("   📝 NOTE: Notification was still saved to database successfully")
                
    except ValidationError as ve:
        logger.error(f"Validation error creating notification for user {instance.id}: {ve}")
        print(f"❌ VALIDATION ERROR: Failed to create notification for {instance.email}: {ve}")
        
    except Exception as e:
        logger.error(f"Unexpected error creating welcome notification for user {instance.id}: {e}")
        print(f"❌ UNEXPECTED ERROR: Failed to create welcome notification for {instance.email}: {e}")


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