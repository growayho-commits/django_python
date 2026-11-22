from django.urls import path
from .views.bank_account_views import BankAccountViewSet

app_name = 'bank_accounts'

urlpatterns = [
    path('bank-account/', BankAccountViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='bank_account'),
]
