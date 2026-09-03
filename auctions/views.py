from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Auctions
from .serializers import AuctionsSerializer
from rest_framework import viewsets
# Create your views here.
@method_decorator(cache_page(120), name='list')      # 2 min cache (auctions are time-sensitive)
@method_decorator(cache_page(120), name='retrieve')
class AuctionsViewSet(viewsets.ModelViewSet):
    queryset = Auctions.objects.all()
    serializer_class = AuctionsSerializer
    