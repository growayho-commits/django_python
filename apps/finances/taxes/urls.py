from django.urls import path
from .views.tax_views import TaxViewSet

app_name = 'taxes'

urlpatterns = [
    path('tax/', TaxViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='tax'),
]
