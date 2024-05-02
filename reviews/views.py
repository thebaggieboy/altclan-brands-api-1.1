from django.shortcuts import render
from rest_framework import viewsets
from .models import Reviews
from .serializers import ReviewSerializer




class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    