from rest_framework import serializers

from .models import *
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'item', 'total', 'ref_code', 'date_created'] 



class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'paystack_reference_number', 'amount', 'status', 'timestamp']


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'amount']



class RefundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'order', 'reason', 'accepted', 'email' ]



class SalesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sales
        fields = ['id', 'user', 'revenue']



class DepositSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deposit
