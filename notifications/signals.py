# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from accounts.models import CustomUser
from brands.models import Merchandise
from transactions.models import Payment, Coupon, Order
from reviews.models import Reviews

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=CustomUser)
def create_new_user_notification(sender, instance, created, **kwargs):
    if created:
        try:
            # Create welcome notification for the new user
            notification = Notification.objects.create(
                user=instance,  # Use the CustomUser instance directly
                sender=instance,  # Self-notification for welcome message
                notification_type='NEW ACCOUNT',  # Use 'SYSTEM' instead of 'NEW ACCOUNT'
                message=f"Welcome to altclan {instance.email}, you can get started by uploading your products",
                target_url=f"/brands/profile/{instance.id}/"
            )
            
            # Send real-time notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{instance.id}",  # Use instance.id (the new user's ID)
                {
                    'type': 'send_notification',
                    'notification': {
                        'id': notification.id,
                        'message': f"Welcome to altclan {instance.email}, you can get started by uploading your products",
                        'is_read': False,
                        'created_at': str(notification.created_at),
                        'target_url': f"/brands/profile/{instance.id}/"
                    }
                }
            )
            
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f"Error creating welcome notification: {e}")