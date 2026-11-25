from django.urls import path
from .views.lead_views import CustomerLeadViewSet
from .views.lead_portal_views import rfq_leads_view

app_name = 'customer_leads'

urlpatterns = [
    path('customer-lead/', CustomerLeadViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='customer_lead'),
    path('portal/', rfq_leads_view, name='rfq_leads'),
]