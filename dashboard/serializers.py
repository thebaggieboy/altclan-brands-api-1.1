from rest_framework import serializers

from .models import *
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customers
        fields = ['id', 'full_name', 'email']
