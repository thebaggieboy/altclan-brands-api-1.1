from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from accounts.models import BrandProfile, BrandUser
from .models import  WishList, Merchandise, Leads, BrandDashboard, Gallery

from .serializers import *
 
class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = Merchandise.objects.all().order_by('-date_created').values()
    serializer_class = MerchandiseSerializer
    #order_by = ['date_created']

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-date_created').values()
    serializer_class = GallerySerializer
    #order_by = ['date_created']

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-date_created').values()
    serializer_class = GallerySerializer
    #order_by = ['date_created']
class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer




# Create your views here.
class BrandDashboardViewSet(viewsets.ModelViewSet):
    queryset = BrandDashboard.objects.all()
    serializer_class = BrandDashboardSerializer

# Create your views here.
class BrandProfileViewSet(viewsets.ModelViewSet):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer




def create_merchandise_list(request):

    return render(request, 'alteclan/index.html')