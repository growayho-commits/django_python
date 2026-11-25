from django.urls import include, path

from apps.customer_supports.views.support_portal_views import support_portal_view

app_name = 'customer_supports'

urlpatterns = [
    path('faqs/', include('apps.customer_supports.faqs.urls')),
    path('helpdesk_tickets/', include('apps.customer_supports.helpdesk_tickets.urls')),
    path('live_chats/', include('apps.customer_supports.live_chats.urls')),
    path('return_refunds/', include('apps.customer_supports.return_refunds.urls')),
    path('portal/', support_portal_view, name='support_portal'),
]