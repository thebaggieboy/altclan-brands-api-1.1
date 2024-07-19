from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Auctions

class AuctionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auctions
        fields = ['user', 'merchandise_name', 'minimum_bid', 'asking_price', 'current_top_bid', 'description', 'deadline', 'date_posted' ,'auctioners', 'all_bids']
