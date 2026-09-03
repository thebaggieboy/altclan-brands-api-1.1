from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from accounts.models import * 
from accounts.views import *
from accounts.serializers import *
from brands.models import *
from brands.serializers import *
from reviews.models import *
from reviews.serializers import *
from transactions.serializers import *
from transactions.models import *
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest, HttpResponse
from brands.models import Merchandise
from brands.serializers import MerchandiseSerializer
from .models import TrackingEvent, SessionLog
from .serializers import SessionLogSerializer
import json
from django.db.models import Q
import random
class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({"status": "healthy"})


class SessionLogViewSet(viewsets.ModelViewSet):
    queryset = SessionLog.objects.all().order_by('-created_at')
    serializer_class = SessionLogSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        payload = serializer.validated_data
        device_id = payload.get('device_id') or self.request.data.get('deviceId')
        session_id = payload.get('session_id') or self.request.data.get('sessionId')
        timestamp = payload.get('timestamp') or self.request.data.get('timestamp')
        user_agent = payload.get('user_agent') or self.request.data.get('userAgent')
        event_payload = {
            'deviceId': device_id,
            'sessionId': session_id,
            'timestamp': timestamp,
            'userAgent': user_agent,
            **self.request.data,
        }

        serializer.save(
            device_id=device_id,
            session_id=session_id,
            timestamp=timestamp,
            user_agent=user_agent,
            extra_data=event_payload,
        )


@method_decorator(cache_page(300), name='list')      # 5 min cache
@method_decorator(cache_page(300), name='retrieve')
@method_decorator(vary_on_headers('Cookie', 'Authorization'), name='list')
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@method_decorator(cache_page(300), name='list')      # 5 min cache
@method_decorator(cache_page(300), name='retrieve')
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


@method_decorator(cache_page(300), name='list')      # 5 min cache
@method_decorator(cache_page(300), name='retrieve')
@method_decorator(vary_on_headers('Cookie', 'Authorization'), name='list')
class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer


def personalized_feed(request):
    limit = int(request.GET.get('limit', '12'))
    # Simple heuristic: prefer newest items
    qs = Merchandise.objects.all().order_by('-date_created')[:limit]
    serializer = MerchandiseSerializer(qs, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


def flash_deals(request):
    limit = int(request.GET.get('limit', '8'))
    # Simple flash deal heuristic: discount > 0 OR labels contains 'flash'
    qs = Merchandise.objects.filter(Q(discount__gt=0) | Q(labels__icontains='flash')).order_by('-date_created')[:limit]
    serializer = MerchandiseSerializer(qs, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


def ai_recommendations(request):
    limit = int(request.GET.get('limit', '6'))
    # Simple random sample as a placeholder for an AI recommender
    ids = list(Merchandise.objects.values_list('id', flat=True))
    sample = random.sample(ids, min(len(ids), limit)) if ids else []
    qs = Merchandise.objects.filter(id__in=sample)
    serializer = MerchandiseSerializer(qs, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
def track_event(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('invalid-json')

    event_type = payload.get('event_type')
    item_id = payload.get('item_id')
    user_id = payload.get('user_id')
    metadata = payload.get('metadata')

    if event_type not in ('impression', 'click'):
        return HttpResponseBadRequest('invalid-event-type')

    user = None
    if user_id:
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.filter(id=user_id).first()
        except Exception:
            user = None

    TrackingEvent.objects.create(event_type=event_type, item_id=item_id, user=user, metadata=metadata or {})
    return JsonResponse({'ok': True})


class LeadsViewSet(viewsets.ModelViewSet):
    queryset = Leads.objects.all()
    serializer_class = LeadsSerializer



# Create your views here.

# Create your views here.
class BrandDashboardViewSet(viewsets.ModelViewSet):
    queryset = BrandDashboard.objects.all()
    serializer_class = BrandDashboardSerializer



# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    



    


