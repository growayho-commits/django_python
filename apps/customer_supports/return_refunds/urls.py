from django.urls import path
from apps.customer_supports.return_refunds.views.refund_views import refund_list_view, refund_request_view

urlpatterns = [
    path('', refund_list_view, name='refund_list'),
    path('request/', refund_request_view, name='refund_request'),
]