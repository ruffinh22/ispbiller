# billing/serializers.py

from rest_framework import serializers
from .models import Client, HotspotCard, HotspotLog, HotspotMacLog, Subscription, Report, Payment, Sale, SMSHistory, Invoice

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class SMSHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSHistory
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class HotspotLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotLog
        fields = '__all__'

class HotspotMacLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotMacLog
        fields = '__all__'

class HotspotCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotCard
        fields = '__all__'