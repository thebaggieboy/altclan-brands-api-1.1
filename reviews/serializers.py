from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reviews

class ReviewsSerializer(serializers.ModelSerializer):
    individual_rating = serializers.IntegerField(min_value=1, required=True)
    max_rating = serializers.IntegerField(default=5, min_value=1, required=False)
    cummulative_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Reviews
        fields = ['id', 'email', 'review', 'merchandise_id', 'merchandise_slug', 'merchandise_name', 'individual_rating', 'max_rating', 'cummulative_rating',  'created_at']
        read_only_fields = ('id', 'created_at', 'cummulative_rating')

    def validate(self, attrs):
        ind = attrs.get('individual_rating')
        max_r = attrs.get('max_rating', 5)
        if ind is None:
            raise serializers.ValidationError({'individual_rating': 'This field is required.'})
        if ind > max_r:
            raise serializers.ValidationError({'individual_rating': f'Must be <= max_rating ({max_r}).'})
        return attrs

    def create(self, validated_data):
        # Ensure max_rating default
        max_r = validated_data.pop('max_rating', 5)
        ind = validated_data.get('individual_rating')
        # Compute cummulative as fraction (server authoritative)
        validated_data['max_rating'] = max_r
        validated_data['cummulative_rating'] = float(ind) / float(max_r) if max_r else 0.0
        return super().create(validated_data)
