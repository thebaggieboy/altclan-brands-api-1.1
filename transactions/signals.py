# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Comment, Post
from accounts.models import CustomUser
from transactions.models import Payment, Coupon, Order
 


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Payment)
def create_payment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.email,
            sender=instance.email,
            notification_type='PAYMENT',
            message=f"{instance.email} made a payment of {instance.amount}",
            target_url=f"/payment/{instance.post.id}/"
        )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"payments_{instance.post.author.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': f"{instance.email} made a payment of {instance.amount}",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/payment/{instance.id}/"
                }
            }
        )

# Add similar signal handlers for other events like likes, follows, etc.

@receiver(post_save, sender=CustomUser)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.email,
            sender=instance.email,
            notification_type='ORDER',
            message=f"{instance.email} made a new order",
            target_url=f"/order/{instance.post.id}/"
        )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"order_{instance.post.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': f"{instance.email} made a new order",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/posts/{instance.id}/"
                }
            }
        )
