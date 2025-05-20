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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = BankSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = CardSerializer




class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
