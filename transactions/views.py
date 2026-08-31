from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from collections import defaultdict
from django.utils.dateparse import parse_date


@require_GET
def get_daily_orders(request):
    # Get start_date and end_date from query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        # Parse the dates from query parameters
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    else:
        # Default to the last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=30)
    
    # Fetch orders within the specified date range
    orders = Order.objects.filter(date_created__range=[start_date, end_date]).values('order_date')
    
    # Create a dictionary to store daily order counts
    daily_orders = defaultdict(int)
    
    # Populate the dictionary with order counts
    for order in orders:
        order_date = order['order_date'].strftime('%Y-%m-%d')  # Format date as string
        daily_orders[order_date] += 1
    
    # Generate a list of dates for the specified range
    date_range = [start_date + timezone.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    # Fill in missing dates with 0
    formatted_data = {
        'labels': [],
        'data': []
    }
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        formatted_data['labels'].append(date_str)
        formatted_data['data'].append(daily_orders.get(date_str, 0))
    
    # Return JSON response
    return JsonResponse(formatted_data)

@require_GET
def get_monthly_orders(request):
    # Get start_date and end_date from query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        # Parse the dates from query parameters
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    else:
        # Default to the last 12 months
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=365)  # Approximately 12 months
    
    # Fetch orders within the specified date range
    orders = Order.objects.filter(order_date__range=[start_date, end_date]).values('order_date')
    
    # Create a dictionary to store monthly order counts
    monthly_orders = defaultdict(int)
    
    # Populate the dictionary with order counts, grouped by month
    for order in orders:
        order_month = order['order_date'].strftime('%Y-%m')  # Format date as 'YYYY-MM'
        monthly_orders[order_month] += 1
    
    # Generate a list of months for the specified range
    current_date = start_date
    month_range = []
    while current_date <= end_date:
        month_range.append(current_date.strftime('%Y-%m'))
        # Move to the next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Fill in missing months with 0
    formatted_data = {
        'labels': [],
        'data': []
    }
    for month in month_range:
        formatted_data['labels'].append(month)
        formatted_data['data'].append(monthly_orders.get(month, 0))
    
    # Return JSON response
    return JsonResponse(formatted_data)
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = Order.objects.all().order_by('-date_created')
        req = self.request
        if getattr(req.user, 'is_authenticated', False) and getattr(req.user, 'brand_name', None):
            req_brand = req.user.brand_name
        else:
            req_brand = None
        user_id = req.query_params.get('user')
        if req_brand:
            user_id = None
            brand = req_brand
        if user_id:
            return qs.filter(user_id=user_id)

        brand = req.query_params.get('brand') or req.query_params.get('brand_name')
        if brand:
            # find merchandise ids for brand_name
            try:
                from brands.models import Merchandise
                from accounts.models import CustomUser
                if str(brand).isdigit():
                    brand_user = CustomUser.objects.filter(id=int(brand)).first()
                    brand_name = brand_user.brand_name if brand_user else None
                    if not brand_name:
                        return qs.none()
                    merch_qs = Merchandise.objects.filter(brand_name=brand_name)
                else:
                    merch_qs = Merchandise.objects.filter(brand_name__iexact=brand)
                merch_ids = list(merch_qs.values_list('id', flat=True))
                if merch_ids:
                    filtered = []
                    for o in qs:
                        items = o.item or []
                        for it in items:
                            # robustly check various id fields
                            pid = None
                            if isinstance(it, dict):
                                if str(it.get('brandName', '')).strip().lower() == str(brand_name).strip().lower():
                                    filtered.append(o)
                                    break
                                pid = it.get('itemId') or it.get('id') or it.get('merchandise_id') or it.get('product_id')
                            else:
                                # if stored as JSON string
                                try:
                                    import json
                                    parsed = json.loads(it)
                                    if str(parsed.get('brandName', '')).strip().lower() == str(brand_name).strip().lower():
                                        filtered.append(o)
                                        break
                                    pid = parsed.get('itemId') or parsed.get('id') or parsed.get('merchandise_id') or parsed.get('product_id')
                                except Exception:
                                    pid = None
                            try:
                                if pid and int(pid) in merch_ids:
                                    filtered.append(o)
                                    break
                            except Exception:
                                continue
                    return filtered
            except Exception:
                return qs.none()
            return qs.none()
        return qs


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = BankSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardSerializer




class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer

    def get_queryset(self):
        queryset = Coupon.objects.all().order_by('-start_date')
        current_user = self.request.user
        brand_id = self.request.query_params.get('brand')
        if getattr(current_user, 'is_authenticated', False) and getattr(current_user, 'brand_name', None):
            brand_id = current_user.id
        if brand_id:
            return queryset.filter(user_id=brand_id)
        return queryset.none()


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
