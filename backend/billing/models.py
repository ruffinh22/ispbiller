# billing/models.py

from django.db import models
from django.utils import timezone
import datetime

class Client(models.Model):
    SUBSCRIPTION_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Expired'),
        (3, 'Left'),
        (4, 'Pending'),
        (5, 'Suspended')
    ]

    PROTOCOL_TYPE_CHOICES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot')
    ]

    name = models.CharField(max_length=255)
    subscription_status = models.IntegerField(choices=SUBSCRIPTION_STATUS_CHOICES, default=1)  # Default to Active
    join_date = models.DateField(default=timezone.now)
    expire_date = models.DateField(default=timezone.now().date() + datetime.timedelta(days=365))  # Default to 1 year from now
    protocol_type = models.CharField(max_length=10, choices=PROTOCOL_TYPE_CHOICES, default='pppoe')  # Default to 'pppoe'
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.plan_name} - {self.client.name}"

class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f'{self.client.name} - {self.amount}'

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()

    def __str__(self):
        return f'{self.client.name} - {self.amount}'

class SMSHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField()

    def __str__(self):
        return f'{self.client.name} - {self.sent_at}'

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f'{self.client.name} - {self.amount}'

from django.db import models

class HotspotLog(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return f"{self.client} - {self.action} at {self.timestamp}"

class HotspotMacLog(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.client} - {self.mac_address} - {self.action} at {self.timestamp}"

class HotspotCard(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Card {self.card_number} - {self.client}"
