from django.urls import path, include

app_name = 'marketing_leads'

urlpatterns = [
    path('carts/', include('apps.marketing_leads.carts.urls')),
    path('checkout_flows/', include('apps.marketing_leads.checkout_flows.urls')),
    path('coupons_discounts/', include('apps.marketing_leads.coupons_discounts.urls')),
    path('customer_leads/', include('apps.marketing_leads.customer_leads.urls')),
    path('orders/', include('apps.marketing_leads.orders.urls')),
    path('push_notifications/', include('apps.marketing_leads.push_notifications.urls')),
    path('wishlists/', include('apps.marketing_leads.wishlists.urls')),
]
