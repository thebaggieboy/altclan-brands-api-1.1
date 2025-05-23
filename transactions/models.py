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
)
PAYMENT_TYPE = (
    ('Paystack', 'Paystack'),
    ('Card', 'Card'),
    ('Paypal', 'Paypal'),
    ('Bank Transfer', 'Bank Transfer'),
)
User = settings.AUTH_USER_MODEL
RANDOM_ORDER_ID = get_random_string(length=12)


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_accounts')
    bank_name = models.CharField(max_length=15,  default='', null=True)
    bank_code = models.CharField(max_length=15, default='', null=True)
    account_name = models.CharField(max_length=15, default='', null=True)
    account_number = models.CharField(max_length=15, default='', null=True)

    def __str__(self):
        return self.bank_code
    
class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_cards')
    card_holder = models.CharField(max_length=250,  default='', null=True)
    card_number = models.CharField(max_length=20, default='', null=True)
    expiry_date = models.CharField(max_length=15, default='', null=True)
    cvv = models.CharField(max_length=15, default='', null=True)

    def __str__(self):
        return self.card_holder
class Deposit(models.Model):
    
    amount = models.FloatField()

    def __str__(self):
        return self.deposit_type

class Withdraw(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return self.amount


# Create your models here.
class Order(models.Model): 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    email = models.CharField(max_length=250,  default='', null=True)
    item = ArrayField(models.JSONField(), default=list)  
    total=models.IntegerField()
    quantity=models.IntegerField()
    ref_code=models.CharField(max_length=250,  default='', null=True)
    status=models.CharField(max_length=250,  default='', null=True)
    shipping_method = models.CharField(max_length=250,  default='Standard Delivery', null=True, choices=SHIPPING_METHODS)
    date_created = models.DateTimeField(default=timezone.now())


    def __str__(self):
        return f'{self.ref_code}'
class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_payment_method')
    name = models.CharField(max_length=250, null=True, blank=True)
  
    start_date = models.DateTimeField(default=timezone.now())
    

    def __str__(self):
        return self.code

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_payment')
    paystack_reference_number = models.CharField(max_length=250, blank=True, null=True)
    customer = models.CharField(max_length=250, blank=True, null=True)

    payment_method = models.CharField(max_length=250, blank=True, null=True)    
    amount = models.FloatField()
    status = models.CharField(max_length=250, null=True, blank=True)
    order_id = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

 
    def save(self, *args, **kwargs):

        
        print('[CREATED] - A new payment has been made')
        super(Payment, self).save(*args, **kwargs)
        
    def __str__(self): 
        return self.amount

class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_billing')
    billing_period = models.CharField(max_length=250, blank=True, null=True)
    payment_method = models.CharField(max_length=250, blank=True, null=True) 
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, null=True, blank=True)   
    invoice_id = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    renewal_date = models.DateTimeField()
 
    def save(self, *args, **kwargs):

        
        print('[CREATED] - A new billing information has been created')
        super(Payment, self).save(*args, **kwargs)
        
    def __str__(self): 
        return self.timestamp


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_coupon')
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=15)
    type = models.CharField(max_length=150, choices=COUPON_TYPE, default="Percentage")
    status = models.CharField(max_length=150)
    minimum_purchase = models.IntegerField()
    usage_limit = models.IntegerField()
    usage_limit_per_user = models.IntegerField()
    amount = models.FloatField()
    start_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.code

class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_sales')
    revenue = models.FloatField()
    
    def __str__(self):
        return self.code


class Refund(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_refund')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.reason}"
    
class Customers(models.Model):
    #id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='customers')
    brand = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True)
    brand_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    mobile_number = models.IntegerField()
    orders = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
    last_order = models.DateTimeField()
    date_created = models.DateTimeField(default=timezone.now())
    total_amount_spent = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
   
    
    
  
    slug = models.SlugField(null=True, blank=True, default='')
    
    def __str__(self):
        return f'Brands Customers'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name}')
        return super().save(*args, **kwargs)
# ProductOrder, these are the items that have been

