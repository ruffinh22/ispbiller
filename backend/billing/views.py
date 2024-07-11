from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from rest_framework.views import APIView

from .models import Client, Subscription, Report, Payment, Sale, SMSHistory, Invoice, HotspotLog, HotspotMacLog, HotspotCard
from .serializers import (
    ClientSerializer, HotspotCardSerializer, HotspotLogSerializer, HotspotMacLogSerializer, SubscriptionSerializer, ReportSerializer,
    PaymentSerializer, SaleSerializer, SMSHistorySerializer, InvoiceSerializer
)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SMSHistoryViewSet(viewsets.ModelViewSet):
    queryset = SMSHistory.objects.all()
    serializer_class = SMSHistorySerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

# Authentication
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.POST.get('next', 'home'))
    else:
        form = AuthenticationForm()
    return render(request, 'billing/login.html', {'form': form})

# Client ViewSet
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# Client views (legacy function-based views)
@api_view(['GET'])
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_active(request):
    clients = Client.objects.filter(subscription_status=1)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_today(request):
    today = date.today()
    clients = Client.objects.filter(join_date=today)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_expiring(request, days):
    today = date.today()
    end_date = today + timedelta(days=days)
    clients = Client.objects.filter(expire_date__range=[today, end_date])
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_expired(request):
    clients = Client.objects.filter(subscription_status=2)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_pending(request):
    clients = Client.objects.filter(subscription_status=4)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_suspended(request):
    clients = Client.objects.filter(subscription_status=5)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_accounts_left(request):
    clients = Client.objects.filter(subscription_status=3)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

# Report views
@api_view(['GET'])
def report_list(request):
    reports = Report.objects.all()
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def report_detail(request, report_title):
    reports = Report.objects.filter(title=report_title)
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)

# Payment and sales reports
@api_view(['GET'])
def payment_list(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sale_list(request):
    sales = Sale.objects.all()
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)

# Invoice reports
@api_view(['GET'])
def invoice_list(request):
    invoices = Invoice.objects.all()
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

# Client operations
@api_view(['POST'])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def renew_client(request):
    client_id = request.data.get('client_id')
    client = get_object_or_404(Client, pk=client_id)
    # Handle client renewal logic here
    return Response({"detail": "Client renewed successfully"})

@api_view(['POST'])
def migrate_plan(request):
    client_id = request.data.get('client_id')
    client = get_object_or_404(Client, pk=client_id)
    # Handle plan migration logic here
    return Response({"detail": "Client plan migrated successfully"})

# Protocol (PPPoE and Hotspot) views
@api_view(['GET'])
def protocol_users(request, protocol_type):
    clients = Client.objects.filter(protocol_type=protocol_type)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def protocol_active_users(request, protocol_type):
    clients = Client.objects.filter(protocol_type=protocol_type, subscription_status=1)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def protocol_online_users(request, protocol_type):
    clients = Client.objects.filter(protocol_type=protocol_type, is_online=True)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def protocol_offline_users(request, protocol_type):
    clients = Client.objects.filter(protocol_type=protocol_type, is_online=False)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def protocol_specific_users(request, protocol_type):
    # Placeholder for specific protocol-related view
    return Response({"detail": f"{protocol_type} specific users data"})

# Analytics views
@api_view(['GET'])
def sales_analytics(request):
    sales = Sale.objects.all()
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_analytics(request):
    avg_subscription_length = Client.objects.annotate(
        subscription_duration=ExpressionWrapper(F('expire_date') - F('join_date'), output_field=DurationField())
    ).aggregate(avg_duration=Avg('subscription_duration'))
    
    return Response({"average_subscription_length": avg_subscription_length['avg_duration']})

# Subscription views
@api_view(['GET'])
def subscription_list(request):
    subscriptions = Subscription.objects.all()
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)

# Dynamic views for hotspot logs
@api_view(['GET'])
def hotspot_log(request):
    logs = HotspotLog.objects.all()
    serializer = HotspotLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hotspot_mac_log(request):
    mac_logs = HotspotMacLog.objects.all()
    serializer = HotspotMacLogSerializer(mac_logs, many=True)
    return Response(serializer.data)

# Dynamic view for hotspot card search
@api_view(['GET'])
def hotspot_card_search(request, card_number):
    card = HotspotCard.objects.filter(card_number=card_number).first()
    if card:
        serializer = HotspotCardSerializer(card)
        return Response(serializer.data)
    else:
        return Response({"detail": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

# Hotspot user views
@api_view(['GET'])
def hotspot_all_users(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hotspot_active_users(request):
    clients = Client.objects.filter(subscription_status=1)  # Assuming 1 indicates active status
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hotspot_online_users(request):
    clients = Client.objects.filter(is_online=True)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hotspot_offline_users(request):
    clients = Client.objects.filter(is_online=False)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)
