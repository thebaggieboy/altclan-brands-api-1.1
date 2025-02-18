from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from collections import defaultdict
from django.utils.dateparse import parse_date


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer


