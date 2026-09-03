from django.shortcuts import render
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import viewsets

from .models import  WishList, Merchandise, Leads, BrandDashboard, Gallery, BrandGallery

from .serializers import *
from accounts.models import CustomUser
 
@method_decorator(cache_page(300), name='list')      # 5 min cache
@method_decorator(cache_page(300), name='retrieve')
@method_decorator(vary_on_headers('Cookie', 'Authorization'), name='list')
class MerchandiseViewSet(viewsets.ModelViewSet):
    serializer_class = MerchandiseSerializer

    def get_queryset(self):
        qs = Merchandise.objects.all().order_by('-date_created')
        req = self.request
        brand = req.query_params.get('brand') or req.query_params.get('brand_name')
        if getattr(req.user, 'is_authenticated', False) and getattr(req.user, 'brand_name', None):
            brand = req.user.brand_name
        if brand:
            # `brand` is a brand-user id, while products store the brand name.
            if str(brand).isdigit():
                brand_user = CustomUser.objects.filter(id=int(brand)).first()
                qs = qs.filter(brand_name=brand_user.brand_name) if brand_user and brand_user.brand_name else qs.none()
            else:
                qs = qs.filter(brand_name__iexact=brand)
        return qs
    #order_by = ['date_created']

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-date_created')
    serializer_class = GallerySerializer
    #order_by = ['date_created']


class BrandGalleryViewSet(viewsets.ModelViewSet):
    queryset = BrandGallery.objects.all().order_by('-date_created')
    serializer_class = BrandGallerySerializer
    #order_by = ['date_created']
class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer




# Create your views here.
class BrandDashboardViewSet(viewsets.ModelViewSet):
    queryset = BrandDashboard.objects.all()
    serializer_class = BrandDashboardSerializer



def create_merchandise_list(request):

    return render(request, 'alteclan/index.html')