from django.urls import path
from .views.pricing_tier_views import PricingTierListCreateAPIView

app_name = 'pricing_tiers'

urlpatterns = [
    path('pricing-tier-list-create-a-p-i/', PricingTierListCreateAPIView.as_view(), name='pricing_tier_list_create_a_p_i'),
]
