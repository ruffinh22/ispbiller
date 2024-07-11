from django.urls import path
from . import views
from .views import login_view


# billing/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, SubscriptionViewSet, ReportViewSet, PaymentViewSet, SaleViewSet, SMSHistoryViewSet, InvoiceViewSet,
    login_view, client_list, subscription_list, client_accounts, client_accounts_active, client_accounts_today,
    client_accounts_expiring, client_accounts_expired, client_accounts_pending, client_accounts_suspended,
    client_accounts_left, report_list, report_detail, payment_list, sale_list, invoice_list,
    create_client, renew_client, migrate_plan, protocol_users, protocol_active_users,
    protocol_online_users, protocol_offline_users, protocol_specific_users, sales_analytics, client_analytics,
    hotspot_all_users, hotspot_active_users, hotspot_online_users, hotspot_offline_users,
    hotspot_log, hotspot_mac_log, hotspot_card_search
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'sms_histories', SMSHistoryViewSet)
router.register(r'invoices', InvoiceViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', login_view, name='login'),
    path('clients/', client_list, name='client_list'),
    path('subscriptions/', subscription_list, name='subscription_list'),
    path('api/client_accounts/', client_accounts, name='client_accounts'),
    path('api/client_accounts/active/', client_accounts_active, name='client_accounts_active'),
    path('api/client_accounts/today/', client_accounts_today, name='client_accounts_today'),
    path('api/client_accounts/expiring/<int:days>/', client_accounts_expiring, name='client_accounts_expiring_days'),
    path('api/client_accounts/expired/', client_accounts_expired, name='client_accounts_expired'),
    path('api/client_accounts/pending/', client_accounts_pending, name='client_accounts_pending'),
    path('api/client_accounts/suspended/', client_accounts_suspended, name='client_accounts_suspended'),
    path('api/client_accounts/left/', client_accounts_left, name='client_accounts_left'),
    path('api/reports/', report_list, name='report_list'),
    path('api/reports/<str:report_title>/', report_detail, name='report_detail'),
    path('api/payments/', payment_list, name='payment_list'),
    path('api/sales/', sale_list, name='sale_list'),
    path('api/invoices/', invoice_list, name='invoice_list'),
    path('api/clients/create/', create_client, name='create_client'),
    path('api/clients/renew/', renew_client, name='renew_client'),
    path('api/clients/migrate/', migrate_plan, name='migrate_plan'),
    path('api/protocol/<str:protocol_type>/', protocol_users, name='protocol_users'),
    path('api/protocol/<str:protocol_type>/active/', protocol_active_users, name='protocol_active_users'),
    path('api/protocol/<str:protocol_type>/online/', protocol_online_users, name='protocol_online_users'),
    path('api/protocol/<str:protocol_type>/offline/', protocol_offline_users, name='protocol_offline_users'),
    path('api/protocol/<str:protocol_type>/specific/', protocol_specific_users, name='protocol_specific_users'),
    path('api/analytics/sales/', sales_analytics, name='sales_analytics'),
    path('api/analytics/clients/', client_analytics, name='client_analytics'),
    path('api/hotspot/users/', hotspot_all_users, name='hotspot_all_users'),
    path('api/hotspot/users/active/', hotspot_active_users, name='hotspot_active_users'),
    path('api/hotspot/users/online/', hotspot_online_users, name='hotspot_online_users'),
    path('api/hotspot/users/offline/', hotspot_offline_users, name='hotspot_offline_users'),
    path('api/hotspot/log/', hotspot_log, name='hotspot_log'),
    path('api/hotspot/mac_log/', hotspot_mac_log, name='hotspot_mac_log'),
    path('api/hotspot/card_search/', hotspot_card_search, name='hotspot_card_search'),
]



