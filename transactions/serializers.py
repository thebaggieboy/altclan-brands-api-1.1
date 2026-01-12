from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class UserHyperlinkedField(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk is None:
            return None
        return super().get_url(obj, view_name, request, format)

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    
    class Meta:
        model = Order
        fields = [ 'id', 'email', 'item', 'total', 'ref_code', 'date_created', 'status', 'quantity']
      

class PaymentSerializer(serializers.HyperlinkedModelSerializer):

    
    class Meta:
        model = Payment
        fields = ['id', 'email', 'paystack_reference_number', 'customer', 'amount', 'payment_method', 'status', 'timestamp']
    
class CouponSerializer(serializers.HyperlinkedModelSerializer):

    
    class Meta:
        model = Coupon
        fields = ['id', 'email', 'code', 'amount', 'name', 'description', 
                 'minimum_purchase', 'usage_limit', 'usage_limit_per_user', 
                 'status', 'start_date', 'end_date']
    

class RefundSerializer(serializers.HyperlinkedModelSerializer):

    order = serializers.HyperlinkedRelatedField(
        view_name='order-detail',
        queryset=Order.objects.all()
    )
    
    class Meta:
        model = Refund
        fields = ['id', 'email', 'order', 'reason', 'accepted', 'email']
        

class SalesSerializer(serializers.HyperlinkedModelSerializer):

    
    class Meta:
        model = Sales
        fields = ['id', 'email', 'revenue']
        extra_kwargs = {
            'url': {'view_name': 'sales-detail'},
        }

class BankSerializer(serializers.HyperlinkedModelSerializer):

    
    class Meta:
        model = Accounts
        fields = ['id', 'email', 'bank_name', 'bank_code', 'account_name', 'account_number']
      

class CardSerializer(serializers.HyperlinkedModelSerializer):

    
    class Meta:
        model = Cards
        fields = ['id', 'email', 'card_holder', 'card_name', 'expiry_date', 'cvv']
      

 