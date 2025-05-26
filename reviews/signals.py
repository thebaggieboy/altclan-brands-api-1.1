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
        try:
            # Get the reviewer (person who created the review)
            reviewer_user = CustomUser.objects.get(email=instance.email)
            
            # Get the product that was reviewed
            # Assuming your Reviews model has a field that links to Merchandise
            # You'll need to adapt this based on your actual Reviews model structure
            
            # Option 1: If Reviews model has a direct merchandise field
            if hasattr(instance, 'merchandise') and instance.merchandise:
                product = instance.merchandise
                brand_name = product.brand_name
                
            # Option 2: If Reviews model has a product_id or merchandise_id field
            elif hasattr(instance, 'merchandise_id') and instance.merchandise_id:
                try:
                    product = Merchandise.objects.get(id=instance.merchandise_id)
                    brand_name = product.brand_name
                except Merchandise.DoesNotExist:
                    return  # Skip if product doesn't exist
                    
            # Option 3: If you store brand_name directly in Reviews model
            elif hasattr(instance, 'brand_name') and instance.brand_name:
                brand_name = instance.brand_name
                
            else:
                return  # Skip if we can't determine the product/brand
            
            # Get the brand owner using brand_name
            # You'll need to adapt this based on how you link brand_name to users
            # Assuming BrandProfile has a brand_name field and is linked to CustomUser
            try:
                from accounts.models import BrandProfile
                brand_profile = BrandProfile.objects.get(brand_name=brand_name)
                recipient_user = brand_profile.user  # Assuming BrandProfile has a user field
                
            except BrandProfile.DoesNotExist:
                # Alternative: if brand_name is stored directly in CustomUser
                try:
                    recipient_user = CustomUser.objects.get(brand_name=brand_name)
                except CustomUser.DoesNotExist:
                    return  # Skip if brand owner doesn't exist
            
            # Don't send notification to yourself (if reviewer is also the brand owner)
            if recipient_user == reviewer_user:
                return
                
            # Create notification with User instances
            notification = Notification.objects.create(
                user=recipient_user,  # Brand owner receives notification
                sender=reviewer_user,   # Reviewer sends notification
                notification_type='REVIEWS',  # Fixed typo: was 'REVEIWS' in your model
                message=f"{reviewer_user.email} reviewed your product: {product.merchandise_name if 'product' in locals() else 'your product'}",
                target_url=f"/reviews/{instance.id}/"
            )
        
        # Send real-time notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{recipient_user.id}",  # Use user ID, not instance.id
            {
                'type': 'send_notification',
                'notification': {
                    'id': notification.id,  # Use notification.id, not instance.id
                    'message': f"{reviewer_user.email} reviewed your product: {product.merchandise_name if 'product' in locals() else 'your product'}",
                    'is_read': False,
                    'created_at': str(notification.created_at),  # Use notification.created_at
                    'target_url': f"/reviews/{instance.id}/"
                }
            }
        )

        
@receiver(post_save, sender=Reviews)
def save_review_notification(sender, instance, **kwargs):
    # This signal runs after every save (create or update)
    # If you need to do something after saving a review, put it here
    # The original code `instance.user_reviews.save()` doesn't make sense
    # because user_reviews is a reverse relationship manager, not a model instance
    
    print("------ Review saved! ------")
 

@receiver(post_save, sender=CustomUser)
def create_new_user_notification(sender, instance, created, **kwargs):
    if created:
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