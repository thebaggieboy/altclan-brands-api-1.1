from django.shortcuts import render
from rest_framework import viewsets, permissions
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

from .models import SessionLog
from .serializers import SessionLogSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer


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
    



    


