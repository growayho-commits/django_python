from django.urls import path
from apps.catalogs.pricing_tiers.views.pricing_views import PricingCreateOrUpdateAPIView

app_name = 'pricing_tiers'

urlpatterns = [
    path('configure/', PricingCreateOrUpdateAPIView.as_view(), name='pricing-configure'),
]
