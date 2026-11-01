# apps/marketing_leads/customer_leads/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.lead_views import CustomerLeadViewSet

router = DefaultRouter()
router.register(r'leads', CustomerLeadViewSet, basename='customer-leads')

urlpatterns = [
    path('', include(router.urls)),
]