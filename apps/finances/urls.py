from django.urls import path, include

app_name = 'finances'

urlpatterns = [
    path('bank_accounts/', include('apps.finances.bank_accounts.urls')),
    path('payment_gateways/', include('apps.finances.payment_gateways.urls')),
    path('payouts/', include('apps.finances.payouts.urls')),
    path('taxes/', include('apps.finances.taxes.urls')),
]
