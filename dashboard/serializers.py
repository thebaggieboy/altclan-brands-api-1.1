from rest_framework import serializers

from .models import *
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customers
        fields = [
            'id', 'full_name', 'first_name', 'last_name', 'email',
            'mobile_number', 'location', 'status', 'orders', 'last_order',
            'date_created', 'total_amount_spent', 'brand_name',
        ]
