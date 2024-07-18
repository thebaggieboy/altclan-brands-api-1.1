from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reviews

class ReviewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reviews
        fields = ['email', 'brand_name', 'slug', 'review']
