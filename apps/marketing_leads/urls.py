from django.urls import path, include

app_name = 'marketing_leads'

urlpatterns = [
    path('carts/', include('apps.marketing_leads.carts.urls')),
    path('orders/', include('apps.marketing_leads.orders.urls')),
    path('checkout/', include('apps.marketing_leads.checkout_flows.urls')),
    path('coupons/', include('apps.marketing_leads.coupons_discounts.urls')),
    path('wishlist/', include('apps.marketing_leads.wishlists.urls')), # இப்போது இயக்கப்பட்டுவிட்டது
    path('notifications/', include('apps.marketing_leads.push_notifications.urls')),
]