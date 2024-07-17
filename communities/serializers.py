from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Community

class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Community
        fields = ['community_name', 'community_bio', 'members']
