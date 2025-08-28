from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Articles

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'brand_name', 'title', 'subject', 'slug']

class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articles
        fields = ['id', 'brand_name', 'title', 'subject', 'slug']

