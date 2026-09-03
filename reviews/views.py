from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import Reviews
from .serializers import ReviewsSerializer




@method_decorator(cache_page(300), name='list')      # 5 min cache
@method_decorator(cache_page(300), name='retrieve')
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    