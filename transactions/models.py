from django.db import models
from django.conf import settings
from accounts.models import User
import uuid
from django.utils import timezone
import uuid
from django.utils.crypto import get_random_string
from brands.models import BillingAddress
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

STATUS = (
    ('P', 'Pending'),
    ('C', 'Completed'),
)

SHIPPING_METHODS = (
    ('Standard Delivery', 'Standard Delivery'),
    ('Express Delivery', 'Express Delivery'),
)

COUPON_TYPE = (
    ('Percentage', 'Percentage'),
    ('Fixed Amount', 'Fixed Amount'),
    ('Free Shipping', 'Free Shipping'),
)

DEPOSIT_TYPE = (
    ('Transfer', 'Transfer'),
    ('Card', 'Card'),
    ('USSD', 'USSD'),
    ('Paystack', 'Paystack'),
    ('Opay', 'Opay')
     
)

PAYMENT_TYPE = (
    ('Transfer', 'Transfer'),
    ('Card', 'Card'),
    ('USSD', 'USSD'),
    ('Paystack', 'Paystack'),
    ('Opay', 'Opay')
)

from django.contrib.auth import get_user_model
User = get_user_model()
RANDOM_ORDER_ID = get_random_string(length=12)


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_accounts')
    email = models.CharField(max_length=250, default='', null=True)
    bank_name = models.CharField(max_length=15, default='', null=True)
    bank_code = models.CharField(max_length=15, default='', null=True)
    account_name = models.CharField(max_length=15, default='', null=True)
    account_number = models.CharField(max_length=15, default='', null=True)

    def __str__(self):
        return self.bank_code or ''


class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_cards')
    email = models.CharField(max_length=250, default='', null=True)
    card_holder = models.CharField(max_length=250, default='', null=True)
    card_number = models.CharField(max_length=20, default='', null=True)
    expiry_date = models.CharField(max_length=15, default='', null=True)
    cvv = models.CharField(max_length=15, default='', null=True)

    def __str__(self):
        return self.card_holder or ''


class Deposit(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount)


class Withdraw(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount)


# FIXED: Order model with proper null handling
class Order(models.Model):
    # FIXED: Allow null user for guest checkout or handle appropriately
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', null=True, blank=True)
    email = models.CharField(max_length=250, default='', null=True)
    item = ArrayField(models.JSONField(), default=list)
    total = models.IntegerField()
    quantity = models.IntegerField()
    ref_code = models.CharField(max_length=250, default='', null=True)
    status = models.CharField(max_length=250, default='', null=True)
    shipping_method = models.CharField(max_length=250, default='Standard Delivery', null=True, choices=SHIPPING_METHODS)
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.ref_code}'


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_payment_method')
    email = models.CharField(max_length=250, default='', null=True)
    type = models.CharField(max_length=250, null=True, blank=True, choices=PAYMENT_TYPE, default='Paystack')
    
    # FIXED: Use timezone.now without parentheses
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name or ''


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_payment')
    email = models.CharField(max_length=250, default='', null=True)
    paystack_reference_number = models.CharField(max_length=250, blank=True, null=True)
    customer = models.CharField(max_length=250, blank=True, null=True)
    payment_method = models.CharField(max_length=250, blank=True, null=True, choices=PAYMENT_TYPE, default='Paystack')
    amount = models.FloatField()
    status = models.CharField(max_length=250, null=True, blank=True)
    order_id = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print('[CREATED] - A new payment has been made')
        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.amount)


class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_billing')
    email = models.CharField(max_length=250, default='', null=True)
    billing_period = models.CharField(max_length=250, blank=True, null=True)
    payment_method = models.CharField(max_length=250, blank=True, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, null=True, blank=True)
    invoice_id = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # FIXED: Allow null renewal_date
    renewal_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        print('[CREATED] - A new billing information has been created')
        # FIXED: Should call super(Billing, self).save() not super(Payment, self).save()
        super(Billing, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.timestamp)
class Deliveries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_deliveries')
    email = models.CharField(max_length=250, default='', null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    delivery_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, null=True, blank=True)
    tracking_number = models.CharField(max_length=250, default='', null=True)
    
    shipping_method = models.CharField(max_length=250, default='Standard Delivery', null=True, choices=SHIPPING_METHODS)
    
    
    
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=250, default='Pending', null=True)

    def __str__(self):
        return f'Delivery for {self.order.ref_code}' if self.order else 'Delivery'


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_coupon')
    email = models.CharField(max_length=250, default='', null=True)
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=15)
    type = models.CharField(max_length=150, choices=COUPON_TYPE, default="Percentage")
    status = models.CharField(max_length=150)
    minimum_purchase = models.IntegerField()
    usage_limit = models.IntegerField()
    usage_limit_per_user = models.IntegerField()
    amount = models.FloatField()
    # FIXED: Use timezone.now without parentheses
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

class Partners(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_partners')
    email = models.CharField(max_length=250, default='', null=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=250, null=True, blank=True)
    logo = models.ImageField(upload_to='partners/', null=True, blank=True)
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name or 'Partner'

class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_sales')
    email = models.CharField(max_length=250, default='', null=True)
    revenue = models.FloatField()

    def __str__(self):
        return str(self.revenue)


class Refund(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_refund')
    # FIXED: Removed duplicate email field
    email = models.EmailField(max_length=250, default='', null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reason}"


# FIXED: Customers model with proper null handling
class Customers(models.Model):
    brand = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='brand_customers')
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    # FIXED: Allow null mobile_number
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    orders = ArrayField(models.CharField(max_length=250), default=list, blank=True)
    # FIXED: Allow null last_order (new customers might not have orders yet)
    last_order = models.DateTimeField(null=True, blank=True)
    # FIXED: Use timezone.now without parentheses
    date_created = models.DateTimeField(default=timezone.now)
    total_amount_spent = ArrayField(models.CharField(max_length=250), default=list, blank=True)
    slug = models.SlugField(null=True, blank=True, default='')

    def __str__(self):
        return f'Customer: {self.full_name or self.email or "Unknown"}'

    def save(self, *args, **kwargs):
        if not self.slug and self.first_name:
            self.slug = slugify(f'{self.first_name}')
        return super().save(*args, **kwargs)