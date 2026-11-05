from django.urls import path
from .views import merchant_views

app_name = 'merchant'

urlpatterns = [
    path('dashboard/', merchant_views.merchant_dashboard, name='dashboard'),  
    path('profile/', merchant_views.MerchantProfileCreateOrUpdateView.as_view(), name='profile'),  # .as_view() சேர்க்கப்பட்டுள்ளது
]