from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Merchandise, Leads, BrandDashboard, Gallery, ShippingAddress
from django.conf import settings
from accounts.models import BrandProfile



BrandUser = settings.BRAND_USER_MODEL


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gallery
        fields = ['brand_name','images']
        
class BrandProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BrandProfile
        fields = ['id','user','date_created']

class BrandDashboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BrandDashboard
        fields = ['total_views', 'total_products', 'total_users', 'total_profit']



class LeadsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leads
        fields = ['id','brand_name', 'instagram_username', 'website_link']



class MerchandiseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merchandise
        fields = [
            'id', 'brand_name', 'merchandise_name', 'available_sizes', 'available_colors', 'labels', 'delivery_cost',  'merchandise_description', 'merchandise_details', 'price', 'display_image', 'reviews', "merchandise_type", "merchandise_gender"
        ]
        

class ShippingAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id','user', 'street_address',  'city', 'state', 'zip']


