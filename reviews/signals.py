# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from accounts.models import CustomUser
from accounts.models import CustomUser
from communities.models import Community, CommunityPost    
from brands.models import Merchandise
from transactions.models import Payment, Coupon, Order
from reviews.models import Reviews


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Reviews)
def create_reviews_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.email,
            sender=instance.email,
            notification_type='REVIEW',
            message=f"{instance.email} made a new review",
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
                    'message': f"{instance.email} created a new review",
                    'is_read': False,
                    'created_at': str(instance.created_at),
                    'target_url': f"/reviews/{instance.id}/"
                }
            }
        )
        
        
@receiver(post_save, sender=Reviews)
def save_reviews_notifications(sender, instance, **kwargs):
    instance.user_reviews.save()
    
    print("------ Review saved! ------")
 

# Add similar signal handlers for other events like likes, follows, etc.

