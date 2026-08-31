
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from core.views import *
from accounts.views import *
from brands.views import *
from blog.views import BlogViewSet as BlogsViewSet, ArticlesViewSet
from communities.views import *
from reviews.views import *
from auctions.views import *
from dashboard.views import *
from notifications import views
from notifications import consumers
 
from transactions.views import get_daily_orders, get_monthly_orders, BankViewSet, CardViewSet


from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'auctions', AuctionsViewSet, basename='auction')
router.register(r'communities', CommunityViewSet, basename='community')
router.register(r'merchandises', MerchandiseViewSet, basename='merchandise')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'bank', BankViewSet, basename='bank')
#router.register(r'cards', CardViewSet, basename='card')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'refund', RefundViewSet, basename='refund')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'blog', BlogsViewSet, basename='blog')
router.register(r'shipping_address', ShippingAddressViewSet, basename='shipping-address')
router.register(r'articles', ArticlesViewSet, basename='article')
router.register(r'brand_gallery', BrandGalleryViewSet, basename='brand-gallery')
urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/chat/', include('chats.urls')),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/daily-orders/', get_daily_orders, name='daily_orders'),
    path('api/monthly-orders/', get_monthly_orders, name='monthly_orders'),
  
    path('api/notifications/', views.NotificationListAPI.as_view(), name='notification-list'),
    path('api/notifications/unread_count/', views.UnreadNotificationCountAPI.as_view(), name='unread-count'),
    path('api/notifications/mark_as_read/', views.MarkAsReadAPI.as_view(), name='mark-as-read'),
    path('api/personalized/', personalized_feed, name='personalized-feed'),
    path('api/flash-deals/', flash_deals, name='flash-deals'),
    path('api/ai-recommendations/', ai_recommendations, name='ai-recommendations'),
    path('api/track-event/', track_event, name='track-event'),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
  
  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   

