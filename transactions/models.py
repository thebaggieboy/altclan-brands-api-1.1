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

DEPOSIT_TYPE = (
    ('Transfer', 'Transfer'),
    ('Card', 'Card'),
    ('USSD', 'USSD'),
)

User = settings.AUTH_USER_MODEL
RANDOM_ORDER_ID = get_random_string(length=12)


class Accounts(models.Model):
    bank_name = models.CharField(max_length=15,  default='', null=True)
    bank_code = models.CharField(max_length=15, default='', null=True)
    account_name = models.CharField(max_length=15, default='', null=True)
    account_number = models.CharField(max_length=15, default='', null=True)

    def __str__(self):
        return self.bank_code

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
    user = models.CharField(max_length=15,  default='', null=True)
    item = ArrayField(models.JSONField(), default=list)  
    date_created = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f'{self.tracking_number}'


class Payment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='user_order')
    paystack_charge_id = models.CharField(max_length=50, default='', null=True, blank=True)
    paystack_reference_number = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=250, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

 
    def save(self, *args, **kwargs):

        
        print('[CREATED] - A new payment has been made')
        super(Payment, self).save(*args, **kwargs)
        
    def __str__(self): 
        return self.amount


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Sales(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='sales_order')
    amount = models.FloatField()
    revenue = models.FloatField()
    status = models.CharField(max_length=250, default='Sold')
    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.reason}"