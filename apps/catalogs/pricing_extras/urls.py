from django.urls import path
from .views.pricing_extra_views import PricingExtraListCreateAPIView

app_name = 'pricing_extras'

urlpatterns = [
    path('pricing-extra-list-create-a-p-i/', PricingExtraListCreateAPIView.as_view(), name='pricing_extra_list_create_a_p_i'),
]
