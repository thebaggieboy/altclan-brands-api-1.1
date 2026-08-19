from rest_framework import serializers

from .models import *
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customers
        fields = ['id', 'brand_name', 'full_name', 'email', 'first_name', 'last_name', 'location', 'status', 'mobile_number', 'orders', 'last_order', 'date_created', 'total_amount_spent']
