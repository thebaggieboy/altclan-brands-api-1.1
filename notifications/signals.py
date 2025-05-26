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

@receiver(post_save, sender=Reviews)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.email,
            sender=instance.email,
            notification_type='REVIEWS',
            message=f"{instance.email} commented on your post",
            target_url=f"/reviews/{instance.post.id}/"
        )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': f"{instance.email} made a review on your product",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/reviews/{instance.id}/"
                }
            }
        )

        
@receiver(post_save, sender=Reviews)
def save_comment_notification(sender, instance, **kwargs):
    instance.user_reviews.save()
    
    print("------ Reviews saved! ------")
 
# Add similar signal handlers for other events like likes, follows, etc.

@receiver(post_save, sender=CustomUser)
def create_new_user_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user.email,
            sender=instance.user.email,
            notification_type='NEW ACCOUNT',
            message=f"Welcome to altclan {instance.user.email}, you can get started by uploading your products",
            target_url=f"/brands/profile/{instance.id}/"
        )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"New account{instance.post.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': f"Welcome to altclan {instance.email}, you can get started by uploading your products",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/brands/profile/{instance.id}/"
                }
            }
        )
