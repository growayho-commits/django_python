from django.urls import path
from .views.lead_views import CustomerLeadViewSet

app_name = 'customer_leads'

urlpatterns = [
    path('customer-lead/', CustomerLeadViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='customer_lead'),
]
