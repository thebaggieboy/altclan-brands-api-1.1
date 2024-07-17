from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *




class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


