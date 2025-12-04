from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reviews

class ReviewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'email', 'review', 'merchandise_id', 'merchandise_slug', 'merchandise_name', 'individual_rating', 'max_rating', 'cummulative_rating',  'created_at']
        
