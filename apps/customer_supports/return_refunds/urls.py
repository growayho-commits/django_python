from django.urls import path
from .views.refund_views import refund_list_view, refund_request_view

app_name = 'return_refunds'

urlpatterns = [
    path('refund-list/', refund_list_view, name='refund_list'),
    path('refund-request/', refund_request_view, name='refund_request'),
]
