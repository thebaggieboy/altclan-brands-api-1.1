from rest_framework import serializers
from django.conf import settings
from .models import Profile, CustomUser, BrandUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'brand_name', 'brand_logo',  'brand_bio', 'brand_type', 'mobile_number']

class BrandUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BrandUser
        fields = ['id', 'email', 'brand_name', 'brand_logo',  'brand_bio', 'brand_type', 'mobile_number']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='profile-detail',queryset=Profile.objects.all())
    class Meta:
        model = Profile
        fields = ['id', 'user', 'date_created']


