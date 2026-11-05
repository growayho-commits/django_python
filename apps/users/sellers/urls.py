from django.urls import path
from apps.users.sellers.views import seller_views  # அல்லது உங்கள் வியூஸ் இம்போர்ட் முறைக்கேற்ப

app_name = 'sellers'

urlpatterns = [
    path('dashboard/', seller_views.seller_dashboard, name='dashboard'), # இங்கு name='dashboard' அவசியம்!
    path('profile/', seller_views.SellerProfileCreateOrUpdateView.as_view(), name='profile'),
]