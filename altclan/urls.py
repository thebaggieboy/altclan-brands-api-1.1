
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from core.views import *
from accounts.views import *
from brands.views import *
from blog.views import BlogViewSet as BlogsViewSet   
from communities.views import *
from reviews.views import *
from auctions.views import *





from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auctions', AuctionsViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'merchandises', MerchandiseViewSet)
router.register(r'gallery', GalleryViewSet)
#router.register(r'user_profile', ProfileViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'refund', RefundViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'blog', BlogsViewSet)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
   
  
  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   

