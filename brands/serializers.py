from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Merchandise, Leads, BrandDashboard, Gallery, ShippingAddress, BrandGallery
from django.conf import settings
class GallerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'brand_name','images']
        
class BrandGallerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BrandGallery
        fields = ['id', 'brand_name', 'images', 'title', 'description']



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
            'id', 'brand_name', 'merchandise_name', 'available_sizes', 'available_colors', 'labels', 'delivery_cost',  'commission_fee', 'total_amount',  'merchandise_description', 'merchandise_details', 'price', 'display_image', 'reviews', "merchandise_type", "merchandise_gender", "images", 'date_created', 'size_type', 'color_type'
        ]
        

class ShippingAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id','user', 'street_address',  'city', 'state', 'zip']


