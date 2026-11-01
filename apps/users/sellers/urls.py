from django.urls import path
from apps.users.sellers.views import SellerProfileCreateOrUpdateView

urlpatterns = [
    path('profile/', SellerProfileCreateOrUpdateView.as_view(), name='seller-profile'),
]