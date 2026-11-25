from django.urls import include, path

from apps.finances.views.finance_portal_views import (
    bank_accounts_portal_view,
    escrow_dashboard_view,
    gst_invoice_print_view,
    gst_invoices_view,
    loyalty_wallet_view,
    payouts_portal_view,
)

app_name = 'finances'

urlpatterns = [
    path('bank_accounts/', include('apps.finances.bank_accounts.urls')),
    path('payment_gateways/', include('apps.finances.payment_gateways.urls')),
    path('payouts/', include('apps.finances.payouts.urls')),
    path('taxes/', include('apps.finances.taxes.urls')),
    path('portal/escrow/', escrow_dashboard_view, name='escrow_dashboard'),
    path('portal/bank-accounts/', bank_accounts_portal_view, name='bank_portal'),
    path('portal/payouts/', payouts_portal_view, name='payout_portal'),
    path('portal/wallet/', loyalty_wallet_view, name='loyalty_wallet'),
    path('portal/gst-invoices/', gst_invoices_view, name='gst_invoices'),
    path('portal/gst-invoices/<int:pk>/print/', gst_invoice_print_view, name='gst_invoice_print'),
]