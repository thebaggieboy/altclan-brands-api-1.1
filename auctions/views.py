from django.shortcuts import render
from .models import Auctions
from .serializers import AuctionsSerializer
from rest_framework import viewsets
# Create your views here.
class AuctionsViewSet(viewsets.ModelViewSet):
    queryset = Auctions.objects.all()
    serializer_class = AuctionsSerializer
    