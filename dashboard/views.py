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
    serializer_class = CustomerSerializer

    def get_queryset(self):
        queryset = Customers.objects.all().order_by('-date_created')
        brand = self.request.query_params.get('brand') or self.request.query_params.get('brand_name')
        current_user = self.request.user
        if getattr(current_user, 'is_authenticated', False) and getattr(current_user, 'brand_name', None):
            brand = current_user.brand_name
        if not brand:
            return queryset.none()
        if str(brand).isdigit():
            queryset = queryset.filter(brand_id=brand)
        else:
            queryset = queryset.filter(brand_name__iexact=brand)
        return queryset


