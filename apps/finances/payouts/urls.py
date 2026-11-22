from django.urls import path
from .views.payout_views import PayoutViewSet

app_name = 'payouts'

urlpatterns = [
    path('payout/', PayoutViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='payout'),
]
