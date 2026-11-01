from django.urls import path
from apps.users.merchant.views import MerchantProfileCreateOrUpdateView

urlpatterns = [
    path('profile/', MerchantProfileCreateOrUpdateView.as_view(), name='merchant-profile'),
]