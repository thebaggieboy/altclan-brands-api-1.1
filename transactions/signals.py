# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
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
            f"notifications_{instance.id}",
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

@receiver(post_save, sender=Order)
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
            f"notifications_{instance.post.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': f"{instance.email} made a new order",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/order/{instance.id}/"
                }
            }
        )

@receiver(post_save, sender=Order)
def create_coupon_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.email,
            sender=instance.email,
            notification_type='COUPON',
            message=f"{instance.email} made a new coupon",
            target_url=f"/coupon/{instance.post.id}/"
        )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.post.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': f"{instance.email} made a new coupon",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/coupon/{instance.id}/"
                }
            }
        )
    
    
@receiver(post_save, sender=Payment)
def save_payment_notifications(sender, instance, **kwargs):
    instance.user_payment.save()
    
    print("------ Payment saved! ------")
 
    
@receiver(post_save, sender=Order)
def save_order_notifications(sender, instance, **kwargs):
    instance.user_order.save()
    
    print("------ Order saved! ------")
 
@receiver(post_save, sender=Order)
def save_coupon_notifications(sender, instance, **kwargs):
    instance.user_coupon.save()
    
    print("------ Coupon saved! ------")
 