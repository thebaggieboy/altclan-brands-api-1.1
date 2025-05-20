from rest_framework import serializers

from .models import *
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'item', 'total', 'ref_code', 'date_created', 'status', 'quantity']   



class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'paystack_reference_number', 'amount', 'status', 'timestamp']


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'amount', 'name', 'description', 'minimum_purchase', 'usage_limit', 'usage_limit_per_user', 'status', 'start_date', 'end_date']



class RefundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'order', 'reason', 'accepted', 'email' ]



class SalesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sales
        fields = ['id', 'user', 'revenue']


class BankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id', 'bank_name' ]


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cards
        fields = ['id', 'card_holder' ]
class DepositSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deposit
