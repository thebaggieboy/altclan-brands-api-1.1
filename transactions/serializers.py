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
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Order
        fields = ['url', 'id', 'email', 'item', 'total', 'ref_code', 'date_created', 'status', 'quantity']
        extra_kwargs = {
            'url': {'view_name': 'order-detail'},
        }

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Payment
        fields = ['url', 'id', 'email', 'paystack_reference_number', 'amount', 'status', 'timestamp']
        extra_kwargs = {
            'url': {'view_name': 'payment-detail'},
        }

class CouponSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Coupon
        fields = ['url', 'id', 'email', 'code', 'amount', 'name', 'description', 
                 'minimum_purchase', 'usage_limit', 'usage_limit_per_user', 
                 'status', 'start_date', 'end_date']
        extra_kwargs = {
            'url': {'view_name': 'coupon-detail'},
        }

class RefundSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    order = serializers.HyperlinkedRelatedField(
        view_name='order-detail',
        queryset=Order.objects.all()
    )
    
    class Meta:
        model = Refund
        fields = ['url', 'id', 'email', 'order', 'reason', 'accepted', 'email']
        extra_kwargs = {
            'url': {'view_name': 'refund-detail'},
        }

class SalesSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Sales
        fields = ['url', 'id', 'email', 'revenue']
        extra_kwargs = {
            'url': {'view_name': 'sales-detail'},
        }

class BankSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Accounts
        fields = ['url', 'id', 'email', 'bank_name']
        extra_kwargs = {
            'url': {'view_name': 'accounts-detail'},
        }

class CardSerializer(serializers.HyperlinkedModelSerializer):
    user = UserHyperlinkedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Cards
        fields = ['url', 'id', 'email', 'card_holder']
        extra_kwargs = {
            'url': {'view_name': 'cards-detail'},
        }

 