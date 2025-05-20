from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Merchandise, Leads, BrandDashboard, Gallery
from django.conf import settings
from .models import ChatRoom, Message
BrandUser = settings.BRAND_USER_MODEL



class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['name', 'participants']
        

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['room', 'sender']
        

