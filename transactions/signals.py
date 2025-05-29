# notifications/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from notifications.models import Notification
from accounts.models import CustomUser
from transactions.models import Payment, Coupon, Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Set up logging
logger = logging.getLogger(__name__)


def send_realtime_notification(user_id, notification_data):
    """
    Send real-time notification via WebSocket channels.
    
    Args:
        user_id: ID of the user to send notification to
        notification_data: Dictionary containing notification data
    """
    try:
        channel_layer = get_channel_layer()
        
        if channel_layer is None:
            logger.warning("Channel layer not configured - skipping real-time notification")
            print("⚠️  WARNING: Channel layer not configured - notification saved but not sent via WebSocket")
            return False
            
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user_id}",
            {
                'type': 'send_notification',
                'notification': notification_data
            }
        )
        
        logger.info(f"Real-time notification sent successfully to user {user_id}")
        print(f"📡 Real-time notification sent to user ID: {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send real-time notification to user {user_id}: {e}")
        print(f"❌ ERROR: Failed to send real-time notification to user {user_id}: {e}")
        return False


def get_user_from_instance(instance, field_name='user'):
    """
    Safely extract user from instance, handling both User objects and email strings.
    
    Args:
        instance: The model instance
        field_name: The field name to get user from (default: 'user')
        
    Returns:
        CustomUser instance or None
    """
    try:
        user_field = getattr(instance, field_name, None)
        
        if isinstance(user_field, CustomUser):
            return user_field
        elif isinstance(user_field, str) and '@' in user_field:
            # If it's an email string, try to find the user
            try:
                return CustomUser.objects.get(email=user_field)
            except CustomUser.DoesNotExist:
                logger.warning(f"User with email {user_field} not found")
                return None
        elif hasattr(instance, 'email') and instance.email:
            # Try to get user by email from instance
            try:
                return CustomUser.objects.get(email=instance.email)
            except CustomUser.DoesNotExist:
                logger.warning(f"User with email {instance.email} not found")
                return None
        else:
            logger.error(f"Could not extract user from {instance.__class__.__name__} instance")
            return None
            
    except Exception as e:
        logger.error(f"Error extracting user from instance: {e}")
        return None


@receiver(post_save, sender=Payment)
def create_payment_notification(sender, instance, created, **kwargs):
    """
    Create notification when a payment is made.
    
    Args:
        sender: The model class (Payment)
        instance: The payment instance
        created: Boolean indicating if this is a new instance
    """
    if not created:
        return
    
    try:
        with transaction.atomic():
            # Get the user who made the payment
            payment_user = get_user_from_instance(instance, 'user')
            if not payment_user:
                logger.error(f"Could not determine user for payment {instance.id}")
                print(f"❌ ERROR: Could not determine user for payment {instance.id}")
                return
            
            # Get the merchant/brand user who should receive the notification
            merchant_user = None
            if hasattr(instance, 'order') and instance.order:
                # If payment is linked to an order, notify the merchant
                if hasattr(instance.order, 'merchandise') and instance.order.merchandise:
                    if hasattr(instance.order.merchandise, 'brand'):
                        merchant_user = instance.order.merchandise.brand
            
            # Create notification for the merchant (if exists)
            if merchant_user:
                notification = Notification.objects.create(
                    user=merchant_user,
                    sender=payment_user,
                    notification_type='PAYMENT',
                    message=f"Payment of ${instance.amount} received from {payment_user.email}",
                    target_url=f"/payments/{instance.id}/"
                )
                
                logger.info(f"Payment notification created for merchant {merchant_user.email}")
                print(f"💰 SUCCESS: Payment notification created for merchant {merchant_user.email}")
                
                # Send real-time notification to merchant
                notification_data = {
                    'id': notification.id,
                    'message': notification.message,
                    'notification_type': notification.notification_type,
                    'is_read': notification.is_read,
                    'created_at': notification.created_at.isoformat(),
                    'target_url': notification.target_url,
                    'sender_email': payment_user.email
                }
                
                send_realtime_notification(merchant_user.id, notification_data)
            
            # Also create confirmation notification for the payer
            payer_notification = Notification.objects.create(
                user=payment_user,
                sender=payment_user,  # Self-notification
                notification_type='PAYMENT_CONFIRMATION',
                message=f"Payment of ${instance.amount} completed successfully",
                target_url=f"/payments/{instance.id}/"
            )
            
            logger.info(f"Payment confirmation notification created for user {payment_user.email}")
            print(f"✅ SUCCESS: Payment confirmation sent to {payment_user.email}")
            
            # Send real-time confirmation to payer
            payer_notification_data = {
                'id': payer_notification.id,
                'message': payer_notification.message,
                'notification_type': payer_notification.notification_type,
                'is_read': payer_notification.is_read,
                'created_at': payer_notification.created_at.isoformat(),
                'target_url': payer_notification.target_url
            }
            
            send_realtime_notification(payment_user.id, payer_notification_data)
                
    except Exception as e:
        logger.error(f"Error creating payment notification for payment {instance.id}: {e}")
        print(f"❌ ERROR: Failed to create payment notification: {e}")


@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    """
    Create notification when a new order is placed.
    
    Args:
        sender: The model class (Order)
        instance: The order instance
        created: Boolean indicating if this is a new instance
    """
    if not created:
        return
    
    try:
        with transaction.atomic():
            # Get the customer who placed the order
            customer = get_user_from_instance(instance, 'user')
            if not customer:
                logger.error(f"Could not determine customer for order {instance.id}")
                print(f"❌ ERROR: Could not determine customer for order {instance.id}")
                return
            
            # Get the merchant/brand who should receive the notification
            merchant = None
            product_name = "Unknown Product"
            
            if hasattr(instance, 'merchandise') and instance.merchandise:
                product_name = instance.merchandise.name
                if hasattr(instance.merchandise, 'brand'):
                    merchant = instance.merchandise.brand
            
            # Create notification for the merchant
            if merchant:
                merchant_notification = Notification.objects.create(
                    user=merchant,
                    sender=customer,
                    notification_type='NEW_ORDER',
                    message=f"New order for {product_name} from {customer.email}",
                    target_url=f"/orders/{instance.id}/"
                )
                
                logger.info(f"Order notification created for merchant {merchant.email}")
                print(f"🛒 SUCCESS: Order notification sent to merchant {merchant.email}")
                
                # Send real-time notification to merchant
                merchant_notification_data = {
                    'id': merchant_notification.id,
                    'message': merchant_notification.message,
                    'notification_type': merchant_notification.notification_type,
                    'is_read': merchant_notification.is_read,
                    'created_at': merchant_notification.created_at.isoformat(),
                    'target_url': merchant_notification.target_url,
                    'sender_email': customer.email
                }
                
                send_realtime_notification(merchant.id, merchant_notification_data)
            
            # Create order confirmation for the customer
            customer_notification = Notification.objects.create(
                user=customer,
                sender=customer,  # Self-notification
                notification_type='ORDER_CONFIRMATION',
                message=f"Order confirmed for {product_name}. Order ID: {instance.id}",
                target_url=f"/orders/{instance.id}/"
            )
            
            logger.info(f"Order confirmation created for customer {customer.email}")
            print(f"✅ SUCCESS: Order confirmation sent to {customer.email}")
            
            # Send real-time confirmation to customer
            customer_notification_data = {
                'id': customer_notification.id,
                'message': customer_notification.message,
                'notification_type': customer_notification.notification_type,
                'is_read': customer_notification.is_read,
                'created_at': customer_notification.created_at.isoformat(),
                'target_url': customer_notification.target_url
            }
            
            send_realtime_notification(customer.id, customer_notification_data)
                
    except Exception as e:
        logger.error(f"Error creating order notification for order {instance.id}: {e}")
        print(f"❌ ERROR: Failed to create order notification: {e}")


@receiver(post_save, sender=Coupon)
def create_coupon_notification(sender, instance, created, **kwargs):
    """
    Create notification when a new coupon is created or used.
    
    Args:
        sender: The model class (Coupon)
        instance: The coupon instance
        created: Boolean indicating if this is a new instance
    """
    if not created:
        # Handle coupon usage updates
        if hasattr(instance, 'is_used') and instance.is_used:
            try:
                # Get the user who used the coupon
                user = get_user_from_instance(instance, 'user')
                if user:
                    notification = Notification.objects.create(
                        user=user,
                        sender=user,
                        notification_type='COUPON_USED',
                        message=f"Coupon '{instance.code}' applied successfully! You saved ${instance.discount_amount}",
                        target_url=f"/coupons/{instance.id}/"
                    )
                    
                    logger.info(f"Coupon usage notification created for user {user.email}")
                    print(f"🎟️ SUCCESS: Coupon usage notification sent to {user.email}")
                    
                    # Send real-time notification
                    notification_data = {
                        'id': notification.id,
                        'message': notification.message,
                        'notification_type': notification.notification_type,
                        'is_read': notification.is_read,
                        'created_at': notification.created_at.isoformat(),
                        'target_url': notification.target_url
                    }
                    
                    send_realtime_notification(user.id, notification_data)
                    
            except Exception as e:
                logger.error(f"Error creating coupon usage notification: {e}")
                print(f"❌ ERROR: Failed to create coupon usage notification: {e}")
        return
    
    try:
        with transaction.atomic():
            # Get the brand/merchant who created the coupon
            creator = get_user_from_instance(instance, 'created_by')
            if not creator:
                logger.warning(f"Could not determine creator for coupon {instance.id}")
                print(f"⚠️  WARNING: Could not determine creator for coupon {instance.id}")
                return
            
            # Create notification for coupon creation confirmation
            notification = Notification.objects.create(
                user=creator,
                sender=creator,
                notification_type='COUPON_CREATED',
                message=f"Coupon '{instance.code}' created successfully with {instance.discount_amount}% discount",
                target_url=f"/coupons/{instance.id}/"
            )
            
            logger.info(f"Coupon creation notification created for user {creator.email}")
            print(f"🎫 SUCCESS: Coupon creation notification sent to {creator.email}")
            
            # Send real-time notification
            notification_data = {
                'id': notification.id,
                'message': notification.message,
                'notification_type': notification.notification_type,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),
                'target_url': notification.target_url
            }
            
            send_realtime_notification(creator.id, notification_data)
                
    except Exception as e:
        logger.error(f"Error creating coupon notification for coupon {instance.id}: {e}")
        print(f"❌ ERROR: Failed to create coupon notification: {e}")


# REMOVED: The problematic save handlers that were causing recursion
# The original save_payment_notifications, save_order_notifications, and save_coupon_notifications
# functions were removed as they were:
# 1. Causing infinite recursion by calling save() in post_save signals
# 2. Referencing non-existent attributes (user_payment, user_order, user_coupon)
# 3. Not providing any meaningful functionality

# Additional utility functions for testing and management

def test_notification_system():
    """
    Test the notification system with sample data.
    Usage: from notifications.signals import test_notification_system; test_notification_system()
    """
    try:
        # Test with existing users and data
        payments = Payment.objects.filter(created_at__gte=timezone.now().replace(hour=0, minute=0, second=0))[:1]
        orders = Order.objects.filter(created_at__gte=timezone.now().replace(hour=0, minute=0, second=0))[:1]
        
        if payments.exists():
            payment = payments.first()
            print(f"🧪 Testing payment notifications with payment ID: {payment.id}")
            create_payment_notification(Payment, payment, True)
        
        if orders.exists():
            order = orders.first()
            print(f"🧪 Testing order notifications with order ID: {order.id}")
            create_order_notification(Order, order, True)
        
        print("✅ Notification system test completed")
        
    except Exception as e:
        print(f"❌ Notification system test failed: {e}")


def get_notification_stats():
    """
    Get statistics about notifications in the system.
    Usage: from notifications.signals import get_notification_stats; get_notification_stats()
    """
    try:
        from django.db.models import Count
        
        stats = Notification.objects.values('notification_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        print("📊 NOTIFICATION STATISTICS:")
        print("-" * 40)
        for stat in stats:
            print(f"  {stat['notification_type']}: {stat['count']}")
        
        total = Notification.objects.count()
        unread = Notification.objects.filter(is_read=False).count()
        
        print("-" * 40)
        print(f"  TOTAL: {total}")
        print(f"  UNREAD: {unread}")
        print(f"  READ: {total - unread}")
        
    except Exception as e:
        print(f"❌ Failed to get notification stats: {e}")


# Signal connection verification
def verify_signal_connections():
    """
    Verify that all signals are properly connected.
    Usage: from notifications.signals import verify_signal_connections; verify_signal_connections()
    """
    from django.db.models.signals import post_save
    
    print("🔍 SIGNAL CONNECTION VERIFICATION:")
    print("-" * 50)
    
    # Check Payment signals
    payment_receivers = post_save._live_receivers(sender=Payment)
    print(f"Payment signals: {len(payment_receivers)} connected")
    
    # Check Order signals  
    order_receivers = post_save._live_receivers(sender=Order)
    print(f"Order signals: {len(order_receivers)} connected")
    
    # Check Coupon signals
    coupon_receivers = post_save._live_receivers(sender=Coupon)
    print(f"Coupon signals: {len(coupon_receivers)} connected")
    
    print("✅ Signal verification completed")