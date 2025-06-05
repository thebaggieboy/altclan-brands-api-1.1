# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Notification
from accounts.models import CustomUser
from reviews.models import Reviews
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=CustomUser)
def create_new_user_notification(sender, instance, created, **kwargs):
    if created:
        # Create the notification
        notification = Notification.objects.create(
            user=instance,
            sender=instance,
            notification_type='NEW ACCOUNT',
            message=f"Welcome to altclan {instance.first_name}, you can get started by uploading your products",
            target_url=f"/brands/profile/{instance.id}/"
        )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"New account{instance.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': notification.id,  # Use notification.id instead of instance.id
                    'message': f"Welcome to altclan {instance.email}, you can get started by uploading your products",
                    'is_read': False,
                    'created_at': str(notification.created_at),  # Use notification.created_at
                    'target_url': f"/brands/profile/{instance.id}/"
                }
            }
         )