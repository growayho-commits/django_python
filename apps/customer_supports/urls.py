from django.urls import path, include

urlpatterns = [
    path('', include('apps.customer_supports.faqs.urls')),              # Default or root support
    path('faqs/', include('apps.customer_supports.faqs.urls')),
    path('helpdesk-tickets/', include('apps.customer_supports.helpdesk_tickets.urls')),
    path('live-chats/', include('apps.customer_supports.live_chats.urls')),
    path('return-refunds/', include('apps.customer_supports.return_refunds.urls')),
]